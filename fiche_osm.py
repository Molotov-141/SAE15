import markdown
import sys
import requests
import os
import markdown
from md_vers_html import convert
from request import get_node
from request import get_node_name
from request import node_to_md
json_data = {}


url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")


id = input("Entrez l'ID du noeud OSM : ")
get_node(id)
get_node_name(id)
node_to_md(json_data, f"fiche_node_{id}.md")
convert(f"./resultats/fiche_node_{id}.md", f"./resultats/fiche_node_{id}.html")
