"""
TestSuggestionMetier

Module de test pour la classe SuggestionMetier.

Usage:
    python3 test_get_suggestions.py
"""

import unittest
from chatbot import SuggestionMetier

class TestSuggestionMetier(unittest.TestCase):

    def setUp(self):
        # Créez une instance de SuggestionMetier pour les tests
        self.suggestion_metier = SuggestionMetier()

    def test_get_suggestions(self):
        """
        Teste la méthode get_suggestions de la classe SuggestionMetier.

        Vérifie si la méthode renvoie une liste de suggestions lorsqu'un texte d'entrée spécifique est fourni.
        Vérifie également que chaque suggestion est représentée sous la forme d'un dictionnaire avec les clés "code" et "label".
        """
        # Testez la méthode get_suggestions avec un texte d'entrée spécifique
        input_text = "Je suis intéressé par médecine"
        suggestions = self.suggestion_metier.get_suggestions(input_text)

        # Assurer le résultat est une liste de suggestions
        self.assertIsInstance(suggestions, list)

        # Assurer les suggestions contiennent des dictionnaires avec les clés attendues
        for suggestion in suggestions:
            self.assertIn("code", suggestion)
            self.assertIn("label", suggestion)


if __name__ == '__main__':
    unittest.main()




   
    


