import requests
import markdown
url = "https://api.openstreetmap.org/"
response = requests.get(url)
if response.status_code == 200:
    print("Connexion réussie avec le serveur")
elif response.status_code == 500:
    print("Erreur 500 : Erreur interne du serveur")
elif response.status_code == 204:
    print("Aucune donnée à retourner")
## print(response.json)
request = requests.get("https://api.openstreetmap.org/3649697385")
## print(request.json)
if request.status_code == 404:
    print("Erreur 404 : Ressource non trouvée")
    