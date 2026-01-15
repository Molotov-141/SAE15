import requests
import os
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
    '''Crée un score et une note à une ville'''
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
    return note

def dataset_to_md(data, filename: str):
    '''Convertit les données d'une ville en format Markdown.'''
    data = compute_statistics(data)
    if not data or len(data['elements']) == 0:
        print("Erreur : Pas de données valides pour cette ville.")
        return
    tags = data['elements'][0]['tags']
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(dossier_script, "resultats")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_final = os.path.join(chemin_dossier, filename)
    with open(chemin_final, 'w', encoding="utf-8") as f:
        f.write(f"# Est ce que votre ville est pigeon friendly ?\n")
        f.write("## Statistiques\n\n")
        f.write(f"## Votre ville : {query}\n")
        f.write(f"- Note : {note}/20\n")
        f.write(f"- Nombre de boulangeries : {data['boulangeries']}\n")
        f.write(f"- Nombre de fast-foods : {data['fast_foods']}\n")
        f.write(f"- Nombre de routes principales : {data['routes_principales']}\n")