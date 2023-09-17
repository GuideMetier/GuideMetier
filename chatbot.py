import json
import os

import spacy
from spacy.matcher import Matcher
from spacy import displacy
from unidecode import unidecode
from models.metiers import Metiers
from utils import timer
from entity_chatbot import EntityChatbot


class SuggestionMetier:
    """
    Classe qui permet de suggérer un métier en fonction de différentes données.

    Attributs:
        nlp (spacy object): Modèle NLP.
        metiers (Metiers object): Objets de métiers.
        entity_chatbot (EntityChatbot object): Bot de chat pour les entités.
        matcher (Matcher object): Outil de correspondance pour les compétences.
        preprocessed_texts (dict): Textes prétraités.
        pattern_list (list): Liste de motifs.
    """
    def __init__(self):
        """
        Constructeur de la classe.
        Initialise le jeu de données, le modèle NLP, le chatbot des entités, les motifs et le matcher.
        """
        self.init_dataset()
        self.init_nlp_model()
        self.init_entity_chatbot()
        self.init_patterns()
        self.init_matcher()

    @timer
    def init_dataset(self):
        """Initialise le jeu de données des métiers."""
        self.metiers = Metiers('dataset/metiers.json')

    @timer
    def init_entity_chatbot(self):
        """Initialise le chatbot des entités."""
        self.entity_chatbot = EntityChatbot()

    @timer
    def init_nlp_model(self):
        """Initialise le chatbot des entités."""
        self.nlp = spacy.load("fr_core_news_sm")

    @timer
    def init_patterns(self):
        """
        Initialise les motifs.
        Si le cache est activé, utilisez les données en cache sinon génère des motifs.
        """
        file_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(file_path)
        cache_file = dir_path + "/dataset/patterns_cache.json"

        # Si le cache est activé et que le fichier de cache existe, chargez les données du cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                self.preprocessed_texts = cache_data['preprocessed_texts']
                self.pattern_list = cache_data['pattern_list']
            return

        # On récupére la liste de compétences prétraitées par métier
        self.preprocessed_texts = {}
        self.pattern_list = self.get_pattern_list()

        # Si le cache est activé, on enregistre les données dans le cache
        if not os.path.exists(cache_file):
            cache_data = {
                'preprocessed_texts': self.preprocessed_texts,
                'pattern_list': self.pattern_list
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=4)

    @timer
    def init_matcher(self):
        """Initialise le matcher pour les compétences."""
        self.matcher = self.create_skill_matcher(self.pattern_list)

    def get_metiers(self) -> Metiers:
        """Retourne l'objet des métiers."""
        return self.metiers

    def extract_data(self, data_list, metier_id):
        """
        Extrait les données à partir d'une liste donnée.

        Args:
            data_list (list): Liste des données à extraire.
            metier_id (str): ID du métier pour lequel extraire les données.

        Returns:
            list: Liste des données extraites.
        """
        extracted = []
        for item in data_list:
            label = item.get('label', None) if isinstance(item, dict) else item
            original_label = label
            if label:
                label = self.clean(label)
                if not label:
                    extracted.append(original_label)
                else:
                    extracted.append(label)
        return extracted

    def get_pattern_list(self):
        """
        Obtient une liste de motifs pour tous les métiers.

        Returns:
            list: Liste de motifs.
        """
        pattern_list = []

        for id, metier in self.metiers.get_all().items():
            extracted_texts = []
            extracted_texts.extend(self.extract_data([metier.name], id))
            extracted_texts.extend(self.extract_data(metier.appellations, id))
            extracted_texts.extend(self.extract_data(metier.work_conditions, id))
            extracted_texts.extend(self.extract_data([k for category in metier.knowledge_categories for k in category.get('knowledges', [])], id))
            extracted_texts.extend(self.extract_data(metier.professional_soft_skills, id))

            # Combinez les textes extraits en un seul texte prétraité pour ce métier
            combined_text = " ".join(extracted_texts)
            self.preprocessed_texts[id] = combined_text  # Stockez le texte prétraité

            pattern_list.extend([(combined_text, id)])  # Ajoutez le texte prétraité

        pattern_list = list(set(pattern_list))
        return pattern_list

    def create_skill_matcher(self, pattern_list):
        """
        Crée un matcher pour les compétences.

        Args:
            pattern_list (list): Liste de motifs pour les compétences.

        Returns:
            Matcher object: Matcher pour les compétences.
        """
        matcher = Matcher(self.nlp.vocab)

        for metier_code, preprocessed_text in self.preprocessed_texts.items():
            doc = self.nlp(preprocessed_text)  # Utiliser le texte prétraité
            exact_pattern = [{"LEMMA": token.lemma_} for token in doc]
            matcher.add(metier_code + "_EXACT", [exact_pattern])

            for token in doc:
                word_pattern = [{"LEMMA": token.lemma_}]
                matcher.add(metier_code, [word_pattern])

        return matcher

    def clean(self, skill):
        """
        Nettoie et pré-traite une compétence ou un mot.

        Args:
            skill (str): La compétence ou le mot à nettoyer.

        Returns:
            str: Compétence ou mot nettoyé.
        """
        # Stoplist personnalisée avec les mots fréquents non significatifs
        custom_stoplist = [
            "au", "aux", "avec", "ce", "ces", "comme", "dans", "de", "des", "du", "en", "et",
            "le", "les", "la", "pour", "qui", "quoi", "sur", "sous", "un", "une", "par",
            "à", "après", "avant", "pendant", "tout", "tous", "toute", "toutes", "mon", "ma", "mes",
            "ton", "ta", "tes", "son", "sa", "ses", "notre", "nos", "votre", "vos", "leur", "leurs",
            "je", "tu", "il", "elle", "nous", "revoir","vous", "ils", "elles", "ceci", "cela", "ça", "mien",
            "tien", "sien", "nôtre", "vôtre", "leur", "laquelle", "lequel", "lesquels", "lesquelles",
            "dont", "quel", "quelle", "quelles", "quels", "si", "sans", "chez", "depuis", "vers", "dans",
            "entre", "hors", "jusque", "jusqu", "lors", "malgré", "parmi", "pendant", "selon", "sans",
            "sauf", "soit", "suivant", "suivant", "voilà", "vos", "votre", "toutes", "tout", "tous",
            "notre", "nos", "notre", "lesquelles", "lesquels", "lequel", "laquelle", "lesquelles",
            "lesquels", "laquelle", "laquelle", "lequel", "lesquelles", "lesquels", "laquelle", "permettre",
            "possibilité", "travailler", "faire", "u","revoir","non"
        ]

        # 1. Suppression des accents
        skill = unidecode(skill)

        # 2. Tokenisation
        tokens = [token for token in self.nlp(skill.lower())]

        # 3. Suppression des stop words, des ponctuations et des mots de la stoplist personnalisée
        tokens = [token for token in tokens if not token.is_stop and not token.is_punct and token.text not in custom_stoplist]

        # 4. Utiliser la lemmatisation pour uniformiser les tokens
        lemmatized_tokens = [token.lemma_ for token in tokens]
        return " ".join(lemmatized_tokens)

    def get_suggestions(self, texte, visualiser=False):
        """
        Obtient des suggestions basées sur le texte entré.

        Args:
            texte (str): Le texte pour lequel obtenir des suggestions.
            visualiser (bool, facultatif): Si vrai, visualise les résultats. Par défaut à False.

        Returns:
            list: Liste de suggestions.
        """
        doc = self.nlp(self.clean(texte))
        print(f"[debug] saisie après nettoyage : {doc}\n")
        exact_matches = [match for match in self.matcher(doc) if "_EXACT" in self.nlp.vocab.strings[match[0]]]

        if exact_matches:
            return self.process_matches(exact_matches, doc, visualiser)
        else:
            # Si aucune correspondance exacte n'est trouvée, recherchez des correspondances mot par mot
            word_matches = self.matcher(doc)
            return self.process_matches(word_matches, doc, visualiser)

    def process_matches(self, matches, doc, visualiser=False):
        """
        Traite les correspondances trouvées dans le document.

        Args:
            matches (list): Liste des correspondances trouvées.
            doc (Doc object): Document SpaCy analysé.
            visualiser (bool, facultatif): Si vrai, visualise les entités trouvées. Par défaut à False.

        Returns:
            list: Liste des résultats traités.
        """
        result_list = set()
        for match_id, start, end in matches:
            rule_id = self.nlp.vocab.strings[match_id].replace("_EXACT", "")  # nettoyage de l'identifiant
            span = doc[start:end]
            print(f"Compétence détectée: {span.text}, Label: {rule_id}")
            if rule_id not in result_list:
                doc.ents = list(doc.ents) + [span]
                result_list.add(rule_id)

        if visualiser:
            displacy.serve(doc, style='ent')

        results = []
        for metier_id in result_list:
            metier = self.metiers.get_metier_by_id(metier_id)
            results.append({
                "code": metier_id,
                "label": metier.name,
            })

        return results

    def suggérer_message(self, suggestions, input):
        """
        Formule un message basé sur les suggestions trouvées.

        Args:
            suggestions (list): Liste des suggestions.
            input (str): Le texte d'entrée de l'utilisateur.

        Returns:
            str: Message suggéré basé sur les suggestions.
        """
        if not suggestions:
            # Aucune suggestion de métier pour l'instant, on fallback sur le chatbot d'entité
            return self.entity_chatbot.process_text(input)
        else:
            metiers_suggested = ", ".join([s["label"] for s in suggestions])
            return "Vous pourriez envisager les métiers suivants : " + metiers_suggested + " (code: " + ", ".join([s["code"] for s in suggestions]) + ")"

if __name__ == '__main__':
    """
    Point d'entrée principal du programme.
    Initialise le chatbot de suggestion de métier et attend une saisie utilisateur.
    """
    print('Démarrage du chatbot...\n')
    chat = SuggestionMetier()

    while True:
        texte = input("Entrez votre texte: ")
        suggestions = chat.get_suggestions(texte)
        print(chat.suggérer_message(suggestions, texte))
