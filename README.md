# SAE15

## Nos modifications :
- Nous avons ajouté un script de calcul de score pour calculer si une ville est un bon endroit habitable pour les pigeons. Nous l'avons fait avec la fonction compute_statistics du fichier datagrab.py.

## Les difficultées rencontrées
- Equilibrer le score n'a pas été facile, mais nous avons réussi avec suffisament de tests.
- Nous n'avons pas réussi à séparer les tags utilisés des tags non utilisés lors de la conversion en markdown.

## Lien utiles 
docu API :  https://wiki.openstreetmap.org/wiki/API_v0.6 

Adresse API : https://api.openstreetmap.org 

— La documentation de l’API :
https://wiki.openstreetmap.org/wiki/Overpass_API 

— La documentation du langage « Overpass QL » utilisé par l’API :
https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL 

— Une interface web permettant de jouer avec l’API :
https://overpass-api.de/api/interpreter 

## Utilisation du code : 
# Lancement d'une fiche OSM d'un noeud
```python fiche_osm.py [ID du noeud]```
# Lancement d'une fiche d'une ville
```python infos_locales.py [VILLE]```