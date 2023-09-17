"""
TestSuggestionMetier

Module de test pour la classe SuggestionMetier.

Usage:
    python3 test_suggérer_message.py
"""

import unittest
from chatbot import SuggestionMetier

class TestSuggestionMetier(unittest.TestCase):
    def setUp(self):
        # Créez une instance de SuggestionMetier pour les tests
        self.suggestion_metier = SuggestionMetier()

    def test_extract_data_with_dict(self):
        """
        Teste la méthode extract_data avec une liste contenant des dictionnaires.

        La méthode devrait extraire les valeurs 'label' des dictionnaires et les convertir en minuscules.
        """
        data_list = [{'label': 'ExampleLabel'}, 'AnotherLabel']
        metier_id = 'example_id'
        extracted = self.suggestion_metier.extract_data(data_list, metier_id)
        self.assertEqual(extracted, ['examplelabel', 'anotherlabel']) # résultat en minuscule pour avoir un style uniforme

    def test_extract_data_without_dict(self):
        """
        Teste la méthode extract_data avec une liste ne contenant pas de dictionnaires.

        La méthode devrait convertir les éléments de la liste en minuscules.
        """
        data_list = ['Label1', 'Label2']
        metier_id = 'example_id'

        extracted = self.suggestion_metier.extract_data(data_list, metier_id)
        self.assertEqual(extracted, ['label1', 'label2']) # résultat en minuscule pour avoir un style uniforme

if __name__ == '__main__':
    unittest.main()




