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

## id = "3649697385"
## print("https://www.openstreetmap.org/api/0.6/node/3649697385.json")
## print(response.json)

## response = requests.get("https://www.openstreetmap.org/api/0.6/node/"+id+".json")
## print("https://www.openstreetmap.org/api/0.6/node/"+id+".json")
## print(request.json)
## if response.status_code == 404:
    ## print("Erreur 404 : Ressource non trouvée")
## print(response.json)
id = "3649697385"
api_url = "https://www.openstreetmap.org/api/0.6/node/3649697385.json"
response = requests.get(api_url)
donnees = response.json()
print(donnees)