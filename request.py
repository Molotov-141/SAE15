import requests
import os
import markdown as md
from getmap import getimgcoord
from PIL import Image
url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")

def get_node(id):
    '''Récupère les données d'un noeud OSM à partir de son ID.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        return(json_data)

def get_node_name(id):
    '''Récupère le nom d'un noeud OSM à partir de son ID et renvoie "SANS NOM" s'il n'en a pas.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data['elements'][0]['tags'].get('name', 'SANS NOM'))
    return(json_data)

def print_node_attributes(id):
    '''Affiche les attributs d'un noeud OSM à partir de son ID.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json() 
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data['elements'][0]['tags'])

def node_to_md(id, filename: str):
    '''Convertit les données d'un noeud OSM en format Markdown.'''
    data = get_node(id)
    if not data or len(data['elements']) == 0:
        print("Erreur : Pas de données valides pour cet ID.")
        return
    tags = data['elements'][0]['tags']
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(dossier_script, "resultats")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_final = os.path.join(chemin_dossier, filename)
    with open(chemin_final, 'w', encoding="utf-8") as f:
        f.write(f"# Informations sur le noeud {id}\n\n")
        f.write("## Attributs\n\n")
        numero = tags.get('addr:housenumber', '')
        rue = tags.get('addr:street', '')
        ville = tags.get('addr:city', '')
        if numero or rue or ville:
            adresse_complete = f"{numero} {rue}, {ville}".strip() # Evite espaces inutiles si pas de numéro de rue
            f.write(f"- **Adresse** : {adresse_complete}\n")   
        f.write(f"- **Nom** : {tags.get('name', 'Non spécifié')}\n")
        f.write(f"- **Type** : {tags.get('shop', tags.get('amenity', 'Non spécifié'))}\n") # Cherche shop, sinon amenity
        f.write(f"- **Téléphone** : {tags.get('phone', 'Non spécifié')}\n")
        f.write(f"- **Livraison** : {tags.get('delivery', 'Non spécifié')}\n")
        f.write(f"- **Horaires** : {tags.get('opening_hours', 'Non spécifié')}\n")
        carte = tags.get('payment:cards', 'Non spécifié')
        cash = tags.get('payment:cash', 'Non spécifié')
        f.write(f"- **Paiement Carte** : {carte}\n")
        f.write(f"- **Paiement Espèces** : {cash}\n")
        
        f.write(f"- **Vente à emporter** : {tags.get('takeaway', 'Non spécifié')}\n")
        f.write(f"- **Site Web** : {tags.get('website', 'Non spécifié')}\n")
        f.write(f"- **Accès PMR** : {tags.get('wheelchair', 'Non spécifié')}\n")
        getimgcoord(data['elements'][0]['lat'], data['elements'][0]['lon'], 18)
        f.write(f"![Emplacement sur la carte](../neufXneufIMG.png)\n")

def get_way(id):
    '''Récupère les données d'une voie OSM à partir de son ID.'''
    api_url = "https://www.openstreetmap.org/api/0.6/way/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        return(json_data)

def way_to_md(id, filename: str):   
    '''Convertit les données d'une voie OSM en format Markdown.'''
    data = get_way(id)
    if not data or len(data['elements']) == 0:
        print("Erreur : Pas de données valides pour cet ID.")
        return
    tags = data['elements'][0]['tags']
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(dossier_script, "resultats")
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_final = os.path.join(chemin_dossier, filename)

    image_path = "../neufXneufIMG.png"
    alt_text = "Emplacement sur la carte"
    markdown_contenu = f"![{alt_text}]({image_path})"

    with open(chemin_final, 'w', encoding="utf-8") as f:
        f.write(f"# Informations sur la voie {id}\n\n")
        f.write("## Attributs\n\n")
        f.write(f"- **Nom** : {tags.get('name', 'Non spécifié')}\n")
        f.write(f"- **Type** : {tags.get('highway', 'Non spécifié')}\n")
        f.write(f"- **Surface** : {tags.get('surface', 'Non spécifié')}\n")
        f.write(f"- **Largeur** : {tags.get('width', 'Non spécifié')}\n")
        f.write(f"- **Accès PMR** : {tags.get('wheelchair', 'Non spécifié')}\n")
        f.write(markdown_contenu)