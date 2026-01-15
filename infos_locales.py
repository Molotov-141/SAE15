from datagrab import get_dataset, compute_statistics, dataset_to_md
from convertisseur3000 import convertion
import requests
import os
import markdown
import sys

json_data = {}
overpass_url0 = "http://overpass-api.de/api/interpreter"
overpass_url1 = "https://lz4.overpass-api.de/api/interpreter"
connexion = requests.get(overpass_url0)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
    connexion1 = requests.get(overpass_url1)
    if connexion1.status_code == 200:
        print("Connexion réussie avec le serveur de secours")
    else:
        print("Erreur lors de la connexion au serveur de secours")
        
query = input("Entrez le nom de la ville : ")
get_dataset(query)
compute_statistics(json_data)
dataset_to_md(json_data, f"resultats/fiche_{query}.md")
convertion(f"resultats/fiche_{query}.md", f"resultats/fiche_{query}.html")