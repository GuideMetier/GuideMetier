import json
import os
from models.metier import Metier

class Metiers:
    """
    Classe représentant une collection de métiers chargés à partir d'une source de données spécifiée.

    Attributes:
        data_source (str): Chemin relatif vers le fichier JSON contenant les données des métiers.
        metiers_data (dict): Données brutes des métiers chargées à partir du fichier JSON.
        metiers (dict): Dictionnaire des objets Metier, clé étant un identifiant et la valeur étant un objet Metier.
    """

    def __init__(self, data_source: str):
        """
        Initialise la classe Metiers.

        Args:
            data_source (str): Chemin relatif vers le fichier JSON contenant les données des métiers.
        """
        self.data_source = data_source
        self.metiers_data = self.load_metiers()
        self.metiers = {key: Metier(data) for key, data in self.metiers_data.items()}

    def load_metiers(self) -> dict:
        """
        Charge les données des métiers à partir du fichier JSON.

        Returns:
            dict: Données des métiers chargées.
        """
        file_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(file_path)
        with open(os.path.join(dir_path, '..', self.data_source), 'r') as json_file:
            return json.load(json_file)

    def get_all(self) -> dict:
        """
        Renvoie un dictionnaire contenant tous les objets Metier.

        Returns:
            dict: Dictionnaire des objets Metier.
        """
        return self.metiers

    def get(self, id: str) -> Metier:
        """
        Renvoie un objet Metier basé sur un identifiant donné.

        Args:
            id (str): Identifiant du métier.

        Returns:
            Metier: Objet Metier si l'identifiant est valide, sinon None.
        """
        return self.metiers.get(id, None)

    def get_metier_by_label(self, label: str) -> Metier:
        """
        Renvoie un objet Metier basé sur un label donné.

        Args:
            label (str): Label du métier.

        Returns:
            Metier: Objet Metier si le label est valide, sinon None.
        """
        for metier in self.metiers.values():
            if metier.label == label:
                return metier
        return None

    def get_metier_by_id(self, id: str) -> Metier:
        """
        Renvoie un objet Metier basé sur un identifiant donné.

        Args:
            id (str): Identifiant du métier.

        Returns:
            Metier: Objet Metier si l'identifiant est valide, sinon None.
        """
        return self.metiers.get(id, None)
    def get_metiers_with_high_demand(self):
        """
        Récupère les métiers où la demande (offres d'emploi) est supérieure à l'offre (chercheurs d'emploi).

        Returns:
            list[Metier]: Liste des objets Metier où le nombre d'offres d'emploi est supérieur au nombre de chercheurs d'emploi.
        """
        return [metier for metier in self.metiers.values() if metier.job_offers > metier.job_seekers]

    def get_metiers_by_domain(self, domain_label):
        """
        Récupère les métiers appartenant à un domaine spécifique.

        Args:
            domain_label (str): Le label du domaine à filtrer.

        Returns:
            list[Metier]: Liste des objets Metier qui correspondent au domaine spécifié.
        """
        return [metier for metier in self.metiers.values() if metier.domain_label == domain_label]

    def get_most_common_work_conditions(self, top_n=5):
        """
        Récupère les conditions de travail les plus courantes parmi tous les métiers.

        Args:
            top_n (int, optional): Nombre de conditions de travail les plus courantes à retourner. Par défaut à 5.

        Returns:
            list[tuple]: Liste des tuples où le premier élément est la condition de travail et le second est le nombre d'occurrences, triée par ordre décroissant d'occurrences.
        """
        conditions_count = {}
        for metier in self.metiers.values():
            for condition in metier.work_conditions:
                conditions_count[condition] = conditions_count.get(condition, 0) + 1

        return sorted(conditions_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_metiers_with_videos(self):
        """
        Récupère les métiers qui ont une URL vidéo associée.

        Returns:
            list[Metier]: Liste des objets Metier ayant une URL vidéo.
        """
        return [metier for metier in self.metiers.values() if metier.video_url]
