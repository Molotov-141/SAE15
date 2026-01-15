import requests
import time
import os
import markdown
import math
overpass_url0 = "http://overpass-api.de/api/interpreter"
overpass_url1 = "https://lz4.overpass-api.de/api/interpreter"

def get_dataset(query):
    print(query)
    request = f"""
    [out:json][timeout:25];
    area["name"="{query}"]->.searchArea;
    (
    way["type"="trunk"](area.searchArea);
    node["shop"="bakery"](area.searchArea);
    node["amenity"="fast_food"](area.searchArea);
    );
    out body;
    """
    response = requests.get(overpass_url0, params={'data': request})
    if response.status_code == 200:
        print("Connexion au serveur établie, données récupérées.")
        json_data = response.json()
        return json_data
    elif response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    elif response.status_code == 500:
        print("Erreur 500 : Erreur interne du serveur")
    elif response.status_code == 204:
        print("Aucune donnée disponible pour cette requête.")
    elif response.status_code == 400:
        print("Erreur 400 : Requête invalide") 
    elif response.status_code == 504:
        response = requests.get(overpass_url1, params={'data': request})
        if response.status_code == 200:
            print("Connexion au serveur de secours établie, données récupérées.")
            json_data = response.json()
            return response.json()
        else:
            print(f"Erreur {response.status_code} : {response.text}")
            return None
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None

def compute_statistics(data):
    score = 0
    bakery_count = 0
    fast_food_count = 0
    route_count = 0
    note = 0
    if not data or "elements" not in data:
        print("Aucune donnée valide disponible pour le calcul des statistiques.")
        return None
    else:
        for element in data['elements']:
            if element['type'] == 'node' and 'tags' in element:
                if 'amenity' in element['tags'] and element['tags']['amenity'] == 'bakery':
                    score += 3
                    bakery_count += 1
            elif element['type'] == 'way' and 'tags' in element:
                if 'type' in element['tags'] and element['tags']['type'] == 'trunk':
                    score += -2
                    route_count += 1
            elif element['type'] == 'node' and 'tags' in element:
                if 'type' in element['tags'] and element['tags']['amenity'] == 'fast_food':
                    score += 1
                    fast_food_count += 1
    if score > 100:
        score = 100
    elif score < 0:
        score = 0
    note = score / 5
    if note > 20:
        note = 20
    if note == 0:
        print("Ville pas du tout pigeon-friendly.")
    if 0 < note < 5:
        print("Ville peu pigeon-friendly.")
    elif 5 <= note < 10:
        print("Ville moyennement pigeon-friendly.")
    elif 10 <= note < 15:
        print("Ville très pigeon-friendly.")
    elif note == 20:
        print("Ville entièrement pigeon-friendly.")
    print(f"{note}/20")
    return note

def dataset_to_md(data, filename):