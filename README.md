# GameForge

**GameForge** est une application web Django qui permet de générer, explorer et gérer des concepts de jeux vidéo grâce à l'intelligence artificielle (OpenAI, Hugging Face).  
L'interface est moderne, sombre, et propose une expérience utilisateur avancée : recherche, gestion de profil, favoris, suppression, etc.

## Fonctionnalités principales

- **Génération de concepts de jeux vidéo** via l'IA (OpenAI/Hugging Face)
- **Exploration** et recherche avancée de jeux (par nom, genre, ambiance, etc.)
- **Gestion de profil** : modification, avatar, bio
- **Inscription/connexion** avec validation moderne
- **Favoris** et gestion de la visibilité (public/privé) des jeux
- **Suppression** de jeux avec confirmation
- **Thème sombre** uniforme et interface responsive

## Prérequis

- Python 3.10+
- PostgreSQL (ou adapter la base de données dans `settings.py`)
- Clés API OpenAI et Hugging Face (optionnel mais recommandé)
- [pip](https://pip.pypa.io/en/stable/)

## Installation

1. **Cloner le dépôt**

```bash
git clone <url_du_repo>
cd GameForge
```

2. **Créer et activer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. **Installer les dépendances**

Crée un fichier `requirements.txt` avec au minimum :

```
Django>=5.2
psycopg2-binary
python-dotenv
crispy-bootstrap5
openai
requests
```

Puis installe :

```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Crée un fichier `.env` à la racine :

```
DJANGO_SECRET_KEY=ta_cle_secrete
DB_NAME=gameforge
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_HOST=localhost
DB_PORT=5432

OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...
```

5. **Initialiser la base de données**

```bash
python manage.py migrate
```

6. **Créer un superutilisateur (admin)**

```bash
python manage.py createsuperuser
```

7. **Lancer le serveur**

```bash
python manage.py runserver
```

Accède à l'application sur [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Structure du projet

- `accounts/` : gestion des utilisateurs, profils, favoris
- `games/` : modèles, vues et gestion des jeux
- `core/` : pages principales (accueil, explorer, etc.)
- `templates/` : templates HTML (thème sombre, responsive)
- `static/css/gameforge_theme.css` : styles personnalisés

## Personnalisation

- **Thème** : modifiable dans `static/css/gameforge_theme.css`
- **Limite d'IA** : modifiable dans `GameForge/settings.py` (`MAX_AI_REQUESTS_PER_DAY`)
- **Langue** : français par défaut (`LANGUAGE_CODE = 'fr-fr'`)

## Déploiement

- Adapter `DEBUG`, `ALLOWED_HOSTS` et la base de données pour la production.
- Configurer un serveur web (ex : Gunicorn + Nginx).
- Collecter les fichiers statiques :  
  ```bash
  python manage.py collectstatic
  ```

## Sécurité

- Ne jamais versionner le fichier `.env` ni les clés API.
- Utiliser des mots de passe forts pour les comptes admin.

## Crédits

- Icônes : [FontAwesome](https://fontawesome.com/)
- UI : Bootstrap 5 + thème personnalisé
- IA : OpenAI, Hugging Face

---

N'hésite pas à demander si tu veux une section supplémentaire (ex : FAQ, contribution, screenshots, etc.) ou une version en anglais ! 