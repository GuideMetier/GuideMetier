# Système de Suggestion de métiers

Ce projet sert à suggérer des métiers en fonction des compétences et intérêts des utilisateurs.

## Configuration initiale

### Prérequis


- `Flask 2.2.0` : Python >=3.5
- `Flask-CORS` : Python >=2.7
- `Spacy 3.6.1` : Python >=3.6,<3.10
- `Requests 2.31.0` : Python >=3.6
- `unidecode` 

---

### Installation

1. Installez les dépendances à l'aide de pip:

```bash
pip install -r requirements.txt
```

2. Téléchargez le modèle `fr_core_news_sm` pour Spacy :

```bash
python -m spacy download fr_core_news_sm
```

## Utilisation

### Lancement du serveur

Pour démarrer le serveur, exécutez :

```bash
python server.py
```

Le serveur démarrera en mode debug et le site web sera accessible via l'URL `http://127.0.0.1:5000/`.

### Test du Chatbot

Pour tester les fonctionnalités du Chatbot sans passer par le site web, exécutez :

```bash
python chatbot.py
```

Suivez ensuite les instructions à l'écran.

## Contribution

Les contributions sont les bienvenues! Veuillez créer une "pull request" avec vos modifications.

---