import time

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests

from api.job_offers_api import JobOffersAPI
from chatbot import SuggestionMetier

app = Flask(__name__)
CORS(app)

chat = SuggestionMetier()
job_offers_api = JobOffersAPI()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/query', methods=['POST'])
def query():
    # Récupérer le nombre depuis la requête
    query = request.form.get('query')

    # Vérifier si le nombre est fourni
    if query is None:
        return jsonify({"error": "Requête invalide"}), 400

    # Traiter la requête
    result = chat.get_suggestions(query)
    message = chat.suggérer_message(result, query)

    # Retourner la réponse
    return jsonify({"message": message, "result": result})

@app.route('/api/metiers/<id>', methods=['GET', 'POST'])
def metier_detail(id):
    # Vérifier si l'identifiant est fourni
    if id is None:
        return jsonify({"error": "Requête invalide"}), 400

    # Traiter la requête
    result = chat.get_metiers().get(id)
    if result is None:
        return jsonify({"error": "Aucun métier trouvé"}), 404

    # Retourner la réponse
    return jsonify({
        "result": result.to_dict()
    })

@app.route('/api/metiers', methods=['GET', 'POST'])
def metiers():
    # Traiter la requête
    metiers = chat.get_metiers().get_all()
    result = {key: metier.to_dict() for key, metier in metiers.items()}

    # Retourner la réponse
    return jsonify({
        "result": result,
        "count": len(result),
    })

@app.route('/api/emplois/<id>', methods=['GET', 'POST'])
def metier_offres_emploi(id):
    try:
        # Traiter la requête
        result = job_offers_api.get_job_offers(job_id=id, max_offers=10)

        if len(result) == 0:
            return jsonify({"error": "Aucun métier trouvé"}), 404

        # Retourner la réponse
        return jsonify({
            "result": result,
            "count": len(result)
        })

    except requests.RequestException:
        return jsonify({"error": "Erreur lors de la communication avec l'API d'emploi."}), 500

if __name__ == '__main__':
    app.run(debug=True)