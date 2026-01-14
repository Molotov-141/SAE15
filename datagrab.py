import requests
import time
overpass_url = "http://overpass-api.de/api/interpreter"

def get_dataset(query):
    response = requests.get(overpass_url, params={'data': query})
    json_data = response.json()
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        return(json_data)
    query = f"""
    [out:json][timeout:25];
    {{geocodeArea:{query}}}->.searchArea;
    node["amenity"="]
    """