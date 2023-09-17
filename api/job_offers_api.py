import requests


class JobOffersAPI:
    """
    Client API pour interroger les offres d'emploi.

    Cette classe permet de récupérer les offres d'emploi à partir d'une API.
    Elle peut être étendue pour intégrer d'autres endpoints liés aux emplois.

    Dépendances:
        - requests: nécessaire pour effectuer des requêtes HTTP.

    Exemple d'utilisation:

        >>> api = JobOffersAPI()
        >>> offers = api.get_job_offers('M1805', 10)
        >>> print(offers)

    :param base_url: L'URL de base de l'API. Par défaut, il s'agit de 'https://localhost:5000'.
    :type base_url: str
    """

    def __init__(self, base_url='https://candidat.pole-emploi.fr/gw-metierscope'):
        self.base_url = base_url

    def get_job_offers(self, job_id, max_offers):
        """
        Récupère les offres d'emploi pour un identifiant de job spécifié.

        :param job_id: L'identifiant du job pour lequel récupérer les offres.
        :type job_id: str

        :param max_offers: Le nombre maximal d'offres à récupérer.
        :type max_offers: int

        :return: Une liste des offres d'emploi.
        :rtype: list[dict]

        :raises requests.RequestException: Si la requête échoue.

        Exemple d'utilisation:

            >>> api = JobOffersAPI()
            >>> offers = api.get_job_offers('M1805', 10)
            >>> print(offers[0]['title'])  # Affiche le titre de la première offre
        """

        url = f'{self.base_url}/job/{job_id}/offers?max={max_offers}'
        response = requests.get(url)

        # Gérer les éventuelles erreurs
        response.raise_for_status()

        return response.json()
