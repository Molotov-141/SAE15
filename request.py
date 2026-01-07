import requests
import markdown as md
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

def get_node_name(id):
    '''Récupère le nom d'un noeud OSM à partir de son ID et renvoie "Sans nom" s'il n'en a pas.'''
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
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
    with open(filename, 'w') as f:
        f.write(md.markdown(f"# Informations sur le noeud {data['id']}\n"))
        f.write(md.markdown("## Attributs\n"))
        for key, value in data['tags'].items():
            f.write(md.markdown(f"- **{key}**: {value}\n"))