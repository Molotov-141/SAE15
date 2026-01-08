import requests
import os
import markdown as md
json_data = {}
url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")

def get_node(id):
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json() 
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data)
    return json_data

def get_node_name(id):
    '''Récupère le nom d'un noeud OSM à partir de son ID et renvoie "Sans nom" s'il n'en a pas.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
    print(json_data)
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data['elements'][0]['tags'].get('name', 'SANS NOM'))

def print_node_attributes(id):
    '''Affiche les attributs d'un noeud OSM à partir de son ID.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json() 
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data['elements'][0]['tags'])

def node_to_md(data: dict, filename: str):
    '''Convertit les données d'un noeud OSM en format Markdown et les enregistre dans un fichier.'''
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(dossier_script, "resultats")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_final = os.path.join(chemin_dossier, filename)
    with open(chemin_final, 'w', encoding="utf-8") as f:
        f.write(f"# Informations sur le noeud {data['elements'][0]['id']}\n\n")
        f.write("## Attributs\n\n")
        for key, value in data['elements'][0].items():
            f.write(f"- **{key}**: {value}\n")
            
