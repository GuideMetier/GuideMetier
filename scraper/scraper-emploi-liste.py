"""
API Scraping de Pôle emploi

Ce script effectue un scraping des offres d'emploi depuis l'API de Pôle Emploi.
"""
import requests
import json
import time

# Récupération de la liste des métiers au format JSON depuis l'API de Pôle Emploi
response = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/jobs/groupByFirstLetter')
metiers = {}  # Dictionnaire pour stocker les métiers et les offres associées
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
        # Récupération des métiers associés
        metier['relatedJobs'] = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/job/' + metier['romeCode'] + '/relatedJobs').json()
        # Récupération des offres d'emploi associées au métier (max 150 offres)
        metier['jobs'] = requests.get('https://candidat.pole-emploi.fr/gw-metierscope/job/' + metier['romeCode'] + '/offers?max=150').json()

        # Stockage du métier et des offres associées dans le dictionnaire
        metiers[metier['romeCode']] = metier

        # Mise à jour et affichage du compteur
        i += 1
        print(str(i) + "/" + str(total_metiers))
        print(str(round(i/total_metiers*100, 2)) + '%')
        print(metier['label'])
        print('-------------------------')

        # Pause pour éviter de surcharger l'API
        time.sleep(0.3)

# Sauvegarde des métiers et des offres associées dans un fichier JSON
with open('dataset/metiers-offres-emploi.json', 'w') as outfile:
    json.dump(metiers, outfile)

print('THE END')