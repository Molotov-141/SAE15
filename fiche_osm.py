import sys
import requests
import os
import markdown
from md_to_html import convert


# Récupération de la carte

import math
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom):
  '''recupération des coordonnées pour avoir la tuile'''
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return xtile, ytile

def getimg(xtile, ytile, zoom):
    '''recupération d'image'''
    url = f"https://tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
    headers = {
    "User-Agent": "Sae n*15"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        print("Image téléchargée")
    else:
        print("Erreur :", response.status_code)

def defimg(lat, lon, zoom):
    '''définition des 9 images'''
    coord = {
        "lat": [lat-1, lat, lat+1],
        "lon": [lon-1, lon, lon+1],
    }
    headers = {
        "User-Agent": "Sae n*15"
    }

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageCG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageCD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)


def assemblimg():
    '''assemblage des 9 images'''
    images_paths = [
        "imageHG.jpg", "imageHC.jpg", "imageHD.jpg",
        "imageCG.jpg", "imageC.jpg", "imageCD.jpg",
        "imageBG.jpg", "imageBC.jpg", "imageBD.jpg"
    ]
    images = [Image.open(img) for img in images_paths]
    w, h = images[0].size
    final_img = Image.new("RGB", (w * 3, h * 3))
    for i, img in enumerate(images):
        x = (i % 3) * w
        y = (i // 3) * h
        final_img.paste(img, (x, y))
    final_img.save("neufXneufIMG.png")

def getimgcoord(lat_deg, lon_deg, zoom):
    '''récupération des images en fonction des coordonnées'''
    xtile,ytile = deg2num(lat_deg,lon_deg,zoom)
    defimg(xtile, ytile,zoom)
    assemblimg()

if __name__ == '__main__' :
    if len(sys.argv) == 4:
        lat = float(sys.argv[1]) # Conversion texte -> nombre
        lon = float(sys.argv[2])
        zoom = int(sys.argv[3])
        getimgcoord(lat, lon, zoom)


# ==================================================================================================================================================
# Requête et traitement des données

import requests
import os
import markdown
from PIL import Image
import sys
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
    elements = data['elements'][0]
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
        f.write(f"- **Autres informations** : {elements.get('tags', 'Aucune autre information')}\n")
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


# ==================================================================================================================================================
# Lancement du script
url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")



id = str(sys.argv[1])  # --> Méthode avec argument en ligne de commande
# id = input("Entrez l'ID du noeud OSM : ") # --> Méthode avec input
api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
response = requests.get(api_url)
json_data = response.json() 
if response.status_code == 404:
    print("Erreur 404 : Ressource non trouvée")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")
json_data = {}
dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_dossier = os.path.join(dossier_script, "resultats")

node_to_md(id, f"fiche_node_{id}.md")
convert(os.path.join(chemin_dossier, f"fiche_node_{id}.md"), os.path.join(chemin_dossier, f"fiche_node_{id}.html"))

