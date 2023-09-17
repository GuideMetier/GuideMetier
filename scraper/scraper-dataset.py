"""
API Scraping de Pôle emploi

Ce script effectue un scraping des métiers depuis l'API de Pôle Emploi.
Il récupère pour chaque métier :
- Les détails du métier,
- Les compétences associées,
- Les conditions de travail associées.
Ces données sont ensuite sauvegardées dans un fichier JSON pour un usage ultérieur.
"""
import requests
import json
import time

# Récupération de la liste des métiers au format JSON depuis l'API de Pôle Emploi
response = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/jobs/groupByFirstLetter')
metiers = {}  # Dictionnaire pour stocker les métiers
i = 0  # Compteur pour suivre le nombre de métiers traités

# Conversion de la réponse en JSON
response_json = response.json()

# Calcul du nombre total de métiers
total_metiers = 0
for key, items in response_json.items():
    total_metiers += len(items)

# Affichage du nombre total de métiers
print("Nombre de metiers: " + str(total_metiers))

# Parcours et traitement des métiers
for key, items in response_json.items():
    for metier in items:
        # Récupération des détails du métier
        metier['metier'] = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/job/' + metier['romeCode']).json()
        # Récupération des compétences associées au métier
        metier['skills'] = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/job/' + metier['romeCode'] + '/skills').json()
        # Récupération des conditions de travail associées au métier
        metier['workConditionsCategories'] = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/job/' + metier['romeCode'] + '/workConditionsCategories').json()

        # Stockage du métier dans le dictionnaire
        metiers[metier['romeCode']] = metier

        # Mise à jour et affichage du compteur
        i += 1
        print(str(i) + "/" + str(total_metiers))
        print(str(round(i/total_metiers*100, 2)) + '%')
        print(metier['label'])
        print('-------------------------')

        # Pause pour éviter de surcharger l'API
        time.sleep(0.3)

# Sauvegarde des métiers dans un fichier JSON
with open('dataset/metiers.json', 'w') as outfile:
    json.dump(metiers, outfile)

print('THE END')
