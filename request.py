import requests
import markdown
url = "https://api.openstreetmap.org/"
connexion = requests.get(url)
if connexion.status_code == 200:
    print("Connexion réussie avec le serveur")
elif connexion.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
elif connexion.status_code == 204:
    print("Aucune donnée à retourner")

# id = "3649697385"
id = "456710077"
api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
response = requests.get(api_url)
json_data = response.json()
if response.status_code == 404:
    print("Erreur 404 : Ressource non trouvée")
else:
    print(json_data)

def get_node_name(id):
    api_url = "https://www.openstreetmap.org/api/0.6/node/"+str(id)+".json"
    response = requests.get(api_url)
    json_data = response.json()
    if response.status_code == 404:
        print("Erreur 404 : Ressource non trouvée")
    else:
        print(json_data['elements'][0]['tags']['name'])