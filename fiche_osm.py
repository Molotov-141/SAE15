import markdown
import sys
import requests
import os
import markdown
from convertisseur3000 import convertion
from request import get_node
from request import node_to_md

json_data = {}


url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")




id = input("Entrez l'ID du noeud OSM : ")
api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
response = requests.get(api_url)
json_data = response.json() 
if response.status_code == 404:
    print("Erreur 404 : Ressource non trouvée")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")
#else:
#    print(json_data)
    
dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_dossier = os.path.join(dossier_script, "resultats")

node_to_md(id, f"fiche_node_{id}.md")
convertion(os.path.join(chemin_dossier, f"fiche_node_{id}.md"), os.path.join(chemin_dossier, f"fiche_node_{id}.html"))

