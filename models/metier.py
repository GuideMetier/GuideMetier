class Metier:
    """
    Classe représentant un métier. Elle offre des méthodes pour extraire des informations
    spécifiques à partir des données du métier fournies lors de son initialisation.
    """

    def __init__(self, data):
        """
        Initialise l'objet Métier avec les données fournies.

        :param data: dict, Données relatives à un métier.
        """
        self.data = data

    def to_dict(self):
        """
        Renvoie les données du métier sous forme de dictionnaire.

        :return: dict, Données du métier.
        """
        return self.data

    @property
    def id(self):
        """Renvoie le code ROME du métier."""
        return self.data.get('romeCode', '')

    @property
    def label(self):
        """Renvoie le libellé du métier."""
        return self.data.get('label', '')

    @property
    def name(self):
        """Renvoie le nom principal du métier."""
        return self.data.get('mainName', '')

    @property
    def job_offers(self) -> int:
        """
        Renvoie le nombre d'offres d'emploi disponibles pour ce métier.

        :return: int, Nombre d'offres d'emploi.
        """
        return self.data.get('labourMarket', {}).get('jobOffers', 0)

    @property
    def job_seekers(self) -> int:
        """
        Renvoie le nombre de demandeurs d'emploi pour ce métier.

        :return: int, Nombre de demandeurs d'emploi.
        """
        return self.data.get('labourMarket', {}).get('jobSeekers', 0)

    @property
    def metier(self):
        """Renvoie les informations détaillées du métier."""
        return self.data.get('metier', {})

    @property
    def description(self):
        """Renvoie la description du domaine du métier."""
        return self.metier.get('description', '')

    @property
    def access_text(self) -> str:
        """
        Renvoie le texte d'accès pour ce métier.

        :return: str, Texte d'accès.
        """
        return self.metier.get('accessText', '')

    @property
    def appellations(self) -> list:
        """
        Renvoie la liste des appellations associées à ce métier.

        :return: list, Liste des appellations.
        """
        return [appellation.get('label', '') for appellation in self.appellations_list]

    @property
    def appellations_list(self) -> list:
        """
        Renvoie la liste complète des appellations associées à ce métier sous forme de dictionnaire.

        :return: list, Liste détaillée des appellations.
        """
        return self.metier.get('appellations', [])
    @property
    def video_url(self) -> str:
        """
        Renvoie l'URL de la vidéo associée à ce métier.

        :return: str, URL de la vidéo.
        """
        return self.metier.get('videoUrl', '')

    @property
    def domain(self) -> dict:
        """
        Renvoie le domaine associé à ce métier sous forme de dictionnaire.

        :return: dict, Domaine du métier.
        """
        return self.metier.get('domain', {})

    @property
    def domain_label(self) -> str:
        """
        Renvoie le label du domaine associé à ce métier.

        :return: str, Label du domaine.
        """
        return self.domain.get('label', '')

    @property
    def domain_url(self) -> str:
        """
        Renvoie l'URL du label du domaine associé à ce métier.

        :return: str, URL du label du domaine.
        """
        return self.domain.get('labelUrl', '')

    @property
    def domain_title(self) -> str:
        """
        Renvoie le titre du domaine associé à ce métier.

        :return: str, Titre du domaine.
        """
        return self.domain.get('title', '')

    @property
    def domain_description(self) -> str:
        """
        Renvoie la description du domaine associé à ce métier.

        :return: str, Description du domaine.
        """
        return self.domain.get('meta', '')

    @property
    def related_jobs(self) -> list:
        """
        Renvoie la liste des métiers associés à ce métier.

        :return: list, Métiers associés.
        """
        return [job.get('label', '') for job in self.related_jobs_list]

    @property
    def related_jobs_list(self) -> list:
        """
        Renvoie la liste complète des métiers associés à ce métier sous forme de dictionnaire.

        :return: list, Liste détaillée des métiers associés.
        """
        return self.data.get('relatedJobs', [])

    @property
    def skills(self) -> dict:
        """
        Renvoie les compétences associées à ce métier sous forme de dictionnaire.

        :return: dict, Compétences du métier.
        """
        return self.data.get('skills', {})

    @property
    def domains_skills(self) -> list:
        """
        Renvoie la liste des compétences de domaine associées à ce métier.

        :return: list, Compétences de domaine.
        """
        return self.skills.get('domainsSkills', [])

    @property
    def knowledge_categories(self) -> list:
        """
        Renvoie la liste des catégories de connaissances associées à ce métier.

        :return: list, Catégories de connaissances.
        """
        return self.skills.get('knowledgeCategories', [])

    @property
    def professional_soft_skills(self) -> list:
        """
        Renvoie la liste des compétences professionnelles douces associées à ce métier.

        :return: list, Compétences professionnelles douces.
        """
        return self.skills.get('professionalSoftSkills', [])

    @property
    def work_conditions(self) -> list:
        """
        Renvoie la liste des conditions de travail associées à ce métier.

        :return: list, Conditions de travail.
        """
        return [cond.get('label', '') for category in self.work_conditions_categories for cond in category.get('workConditions', [])]

    @property
    def work_conditions_categories_label(self) -> list:
        """
        Renvoie la liste des labels des catégories de conditions de travail associées à ce métier.

        :return: list, Labels des catégories de conditions de travail.
        """
        return [category.get('label', '') for category in self.work_conditions_categories]

    @property
    def work_conditions_categories(self) -> list:
        """
        Renvoie la liste des catégories de conditions de travail associées à ce métier.

        :return: list, Catégories de conditions de travail.
        """
        return self.data.get('workConditionsCategories', [])