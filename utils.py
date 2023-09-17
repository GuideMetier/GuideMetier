# utils.py contient des fonctions utilitaires pour le projet
import time

# Décorateur pour mesurer le temps d'exécution des fonctions
def timer(func):
    def wrapper(*args, **kwargs):
        print(f'Chargement de la fonction {func.__name__} en cours...')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'La fonction {func.__name__} a été chargée en {round(end_time - start_time, 2)} seconde(s)\n')
        return result
    return wrapper