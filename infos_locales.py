from datagrab import get_dataset, compute_statistics, dataset_to_md
from convertisseur3000 import convertion
import requests
import os
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
        

query = str(sys.argv[1])  # Méthode avec argument en ligne de commande
# query = input("Entrez le nom de la ville : ") # Méthode avec input
get_dataset(query)
compute_statistics(json_data)

dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_dossier = os.path.join(dossier_script, "resultats")
os.makedirs(chemin_dossier, exist_ok=True)
chemin_fichier_md = os.path.join(chemin_dossier, f"fiche_{query}.md")
chemin_fichier_html = os.path.join(chemin_dossier, f"fiche_{query}.html")
print(f"Création du fichier : {chemin_fichier_md}...")
dataset_to_md(json_data, query, f"{chemin_dossier}/fiche_{query}.md")
convertion(os.path.join(chemin_dossier, f"fiche_{query}.md"), os.path.join(chemin_dossier, f"fiche_{query}.html"))

