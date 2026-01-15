import requests
import os

overpass_url0 = "http://overpass-api.de/api/interpreter"
overpass_url1 = "https://lz4.overpass-api.de/api/interpreter"

def get_dataset(query):
    request = f"""
    [out:json][timeout:300];
    area["wikipedia"="fr:{query}"]->.searchArea;
    (
    way["highway"="trunk"](area.searchArea);
    node["shop"="bakery"](area.searchArea);
    node["amenity"="fast_food"](area.searchArea);
    );
    out body;
    """
    response = requests.get(overpass_url0, params={'data': request})
    if response.status_code == 200:
        print("Connexion au serveur établie, données récupérées.")
        return response.json()
    elif response.status_code == 504:
        response = requests.get(overpass_url1, params={'data': request})
        if response.status_code == 200:
            print("Connexion au serveur de secours établie, données récupérées.")
            return response.json()


def compute_statistics(data):
    if not data or "elements" not in data:
        return None


    stats = {"bakery": 0, "fast_food": 0, "trunk": 0, "score": 0,}
    # Construction du score
    for element in data['elements']:
        t = element.get('tags', {})
        if t.get('shop') == 'bakery' or t.get('amenity') == 'bakery':
            stats["bakery"] += 1
            stats["score"] += 2.5
        elif t.get('amenity') == 'fast_food':
            stats["fast_food"] += 1
            stats["score"] += 1
        elif t.get('highway') == 'trunk':
            stats["trunk"] += 1
            stats["score"] -= 3.5

    # Calcul de la note
    s = stats["score"]
    if s > 100: s = 100
    if s < 0: s = 0
    stats["note"] = s / 5
    note = stats["note"]
    if note > 20:
        note = 20
    if note < 0:
        note = 0
    return stats

def dataset_to_md(data_json, query, filename):
    data_json = get_dataset(query)
    stats = compute_statistics(data_json)
    if not stats:
        print("Erreur : Pas de données valides.")
        return
    
    if note == 0:
        message = "Ville pas du tout pigeon-friendly. Risque élévé de finir en rôtisserie !"
    if 0 < note < 5:
        message = "Ville peu pigeon-friendly. ATTENTION TORTUE CARNIVORE !"
    elif 5 <= note < 10:
        message = "Ville moyennement pigeon-friendly. Ouais, pas mal pas mal"
    elif 10 <= note < 15:
        message = "Ville très pigeon-friendly. SAFE PLACE ( Ya même des psys )"
    elif note == 20:
        message = "Ville entièrement pigeon-friendly. NEC PLUS ULTRA des emplacement où vivre"
        print(f"{note}/20")

    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(dossier_script, "resultats")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_final = os.path.join(chemin_dossier, filename)

    with open(chemin_final, 'w', encoding="utf-8") as f:
        f.write(f"# Est ce que votre ville est pigeon friendly ?\n\n")
        f.write(f"## Votre ville : {query}\n")
        f.write(f"## Statistiques\n")
        f.write(f"- Note : {stats['note']}/20\n")
        f.write(f"- Nombre de boulangeries : {stats['bakery']}\n")
        f.write(f"- Nombre de fast-foods : {stats['fast_food']}\n")
        f.write(f"- Nombre de routes principales : {stats['trunk']}\n")
        f.write(f"## Conclusion\n")
        f.write(f"{message}\n")