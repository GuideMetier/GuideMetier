"""
TestSuggestionMetier

Module de test pour la classe SuggestionMetier.

Usage:
    python3 -m unittest -v test_suggérer_message.py


"""

import unittest
from chatbot import SuggestionMetier

class TestSuggestionMetier(unittest.TestCase):
    def setUp(self):
        # Créez une instance de SuggestionMetier pour les tests
        self.suggestion_metier = SuggestionMetier()
    
    def test_suggest_message(self):
        """
        Teste la méthode suggérer_message de la classe SuggestionMetier.

        Vérifie si la méthode génère le message attendu en fonction des suggestions fournies et du texte d'entrée.
        """
        # Supposons que vous ayez des suggestions connues, par exemple, deux suggestions pour un métier donné
        suggestions = [{'code': 'L1510', 'label': 'Développeur / Développeuse'}, {'code': 'M1805', 'label': 'Animateur / Animatrice 3D'}]
    
        # Appelez la méthode suggérer_message avec ces suggestions et un texte d'entrée
        message = self.suggestion_metier.suggérer_message(suggestions, "Votre texte d'entrée")
    
        # Définissez votre message de référence attendu
        message_attendu = "Vous pourriez envisager les métiers suivants : Développeur / Développeuse, Animateur / Animatrice 3D (code: L1510, M1805)"

        # Vérifiez si le message généré correspond au message attendu
        self.assertEqual(message, message_attendu)

if __name__ == '__main__':
    unittest.main()








   
    


