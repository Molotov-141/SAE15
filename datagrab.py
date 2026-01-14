import requests
import time
import os
import markdown
overpass_url0 = "http://overpass-api.de/api/interpreter"
overpass_url1 = "https://lz4.overpass-api.de/api/interpreter"

def get_dataset(query):
    print(query)
    request = f"""
    [out:json][timeout:25];
    area["name"="{query}"][admin_level=8]->.searchArea;
    (
    node["amenity"="bakery"](area.searchArea);
    node["shop"="bakery"](area.searchArea);
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
    