import markdown
import sys
import requests
import os
import markdown
from convertisseur3000 import convertion
from request import get_node
from request import node_to_md
# import pip
# pip.main(['install', 'Pillow']) ---> Il faudrait pouvoir l'utiliser sur n'importe quelle machine, donc installer pillow automatiquement peut être ?

json_data = {}
dossier_script = os.path.dirname(os.path.abspath(__file__))
chemin_dossier = os.path.join(dossier_script, "resultats")

node_to_md(id, f"fiche_node_{id}.md")
convertion(os.path.join(chemin_dossier, f"fiche_node_{id}.md"), os.path.join(chemin_dossier, f"fiche_node_{id}.html"))

