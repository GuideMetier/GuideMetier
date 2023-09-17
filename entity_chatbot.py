"""
EntityChatbot
=============
Ce module propose une implémentation simple d'un chatbot qui détecte et répond en fonction des entités (e-mail, téléphone, nom) présentes dans un texte. Il peut également reconnaître et répondre à des motifs de phrases spécifiques grâce à un ensemble de conditions préalablement définies.

Classes
-------
EntityChatbot
    Classe principale pour la détection des entités et la génération de réponses.
"""

import json
import os
import random
import re

class EntityChatbot:
    def __init__(self):
        """
        Initialise le chatbot en chargeant les conditions de réponse depuis un fichier JSON et initialise le dernier index de réponse.
        """
        self.conditions_responses = self.load_conditions_responses("dataset/entity-patterns.json")
        self.last_response_index = {}

    def load_conditions_responses(self, filename):
        """
        Charge les conditions de réponse depuis un fichier JSON.

        Parameters:
        - filename (str) : Le chemin du fichier à charger.

        Returns:
        - dict : Un dictionnaire contenant les conditions de réponse.
        """
        file_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(file_path)

        with open(dir_path + '/' + filename, 'r') as file:
            data = json.load(file)
        return data["conditions"]

    def detect_entities(self, text):
        """
        Détecte les entités (e-mail, téléphone, nom) dans un texte donné.

        Parameters:
        - text (str) : Le texte à analyser.

        Returns:
        - dict : Un dictionnaire contenant les entités détectées.
        """
        entities = {}
        email_pattern = r'\S+@\S+'
        phone_pattern = r'\d{10}'
        name_pattern = r'mon nom est ([A-Za-z\s]+)'
        
        entities["EMAIL"] = re.findall(email_pattern, text)
        entities["PHONE"] = re.findall(phone_pattern, text)
        entities["NAME"] = re.findall(name_pattern, text)
        
        return entities

    def process_text(self, text):
        """
        Analyse un texte pour détecter des entités et générer une réponse appropriée.

        Parameters:
        - text (str) : Le texte à analyser.

        Returns:
        - str : La réponse générée.
        """
        entities = self.detect_entities(text)
        
        email_message = ""
        if "EMAIL" in entities and entities["EMAIL"]:
            email_message = f"J'ai bien noté votre mail, mais je n'ai pas été entraîné pour vous envoyer des informations à votre adresse de mail : {', '.join(entities['EMAIL'])}"
            return email_message
        
        phone_message = ""
        if "PHONE" in entities and entities["PHONE"]:
            phone_message = f"J'ai bien noté votre téléphone, mais je n'ai pas été entraîné pour vous appeler ou envoyer des informations à votre numéro : {', '.join(entities['PHONE'])}"
            return phone_message
        
        name_message = ""
        if "NAME" in entities and entities["NAME"]:
            name_message = f"Bonjour {', '.join(entities['NAME'])}!"
            return name_message

        response = None
        
        for condition in self.conditions_responses:
            if condition["type"] == "et" or condition["type"] == "et":
                patterns = condition["patterns"]
                if all(pattern in text for pattern in patterns):
                    responses = condition["responses"]
                    last_index = self.last_response_index.get(tuple(patterns), -1)
                    response_index = (last_index + 1) % len(responses)
                    self.last_response_index[tuple(patterns)] = response_index
                    response = responses[response_index]
                    break
            elif condition["type"] == "ou" or condition["type"] == "ou":
                patterns = condition["patterns"]
                if any(pattern in text for pattern in patterns):
                    responses = condition["responses"]
                    response = random.choice(responses)
                    break
        
        if response:
            return f"{name_message} {email_message} {phone_message} {response}"
        else:
            return f"{name_message} {email_message} {phone_message} Bot: Je n'ai pas compris votre demande, pouvez-vous préciser quel métier vous aimeriez que je vous explique en détail ?"

if __name__ == "__main__":
    """
    Point d'entrée du programme. Lance une boucle de conversation avec le chatbot.
    """
    entity_chatbot = EntityChatbot()

    while True:
        user_input = input("Vous: ")
        if user_input.lower() in ["exit", "quitter"]:
            print("Bot: Au revoir!")
            break
        response = entity_chatbot.process_text(user_input)
        print(response)
