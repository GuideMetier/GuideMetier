"""
TestSuggestionMetier

Module de test pour la classe SuggestionMetier.

Usage:
    python3 test_clean.py
"""

import unittest
from chatbot import SuggestionMetier

class TestSuggestionMetier(unittest.TestCase):
    def setUp(self):
        # Créez une instance de SuggestionMetier pour les tests
        self.suggestion_metier = SuggestionMetier()
        
    def test_clean(self):
        """
        Teste la méthode clean de SuggestionMetier en vérifiant si elle nettoie correctement la chaîne d'entrée.
        
        La méthode clean doit supprimer les accents et mettre en minuscules les mots.
        """
        # Appelez la méthode clean avec une chaîne d'entrée
        input_text = "Développer de logiciel"
        cleaned_text = self.suggestion_metier.clean(input_text)
        
        print("Texte nettoyé:", cleaned_text)
        
        # Vérifiez si la sortie correspond à ce qui est attendu
        expected_output = "developper logiciel"
        self.assertEqual(cleaned_text, expected_output)

if __name__ == '__main__':
    unittest.main()




