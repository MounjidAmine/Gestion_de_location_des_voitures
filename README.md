# 🚗 CarServ - Système de Gestion de Flotte de Véhicules

## 📌 Description

**CarServ** est une application Django conçue pour gérer une flotte de véhicules, incluant l'administration des clients, des employés et des véhicules, ainsi que le suivi des demandes de remplacement.

## 🎯 Fonctionnalités

- 🔑 **Gestion des utilisateurs**  
  - Inscription et authentification des clients et des employés  
  - Rôles et permissions administratives  

- 🚘 **Gestion des véhicules**  
  - Ajout, modification et suppression de véhicules  
  - Attribution des véhicules aux clients  
  - Suivi des véhicules disponibles  

- 🔄 **Gestion des remplacements de véhicules**  
  - Demandes de remplacement en cas de panne ou d'accident  
  - Attribution des véhicules de remplacement  

- 📊 **Tableaux de bord et suivi**  
  - Tableau de bord administrateur  
  - Historique des véhicules et des remplacements  

## 🏗️ Installation

### 📦 Prérequis

- Python 3.x
- Django 4.2+
- SQLite (base de données par défaut)

### 🛠️ Configuration et exécution

1. **Cloner le projet**  
   ```bash
   git clone https://github.com/votre-repo/carserv.git
   cd carserv
   ```

2. **Créer et activer un environnement virtuel**  
   ```bash
   python -m venv env
   source env/bin/activate  # Pour macOS/Linux
   env\Scripts\activate  # Pour Windows
   ```

3. **Installer les dépendances**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**  
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur Django**  
   ```bash
   python manage.py runserver
   ```

Accédez à l'application sur **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

## 📂 Structure du Projet

```
carserv/
│── pfm/                  # Application principale
│   ├── models.py         # Modèles de base de données
│   ├── views.py          # Logique métier (contrôleurs)
│   ├── urls.py           # Routage des URL
│   ├── templates/        # Fichiers HTML des interfaces
│   └── static/           # Fichiers CSS, JS et images
│
│── carserv/              # Configuration principale du projet Django
│   ├── settings.py       # Paramètres du projet
│   ├── urls.py           # Routage global
│   ├── wsgi.py           # Configuration WSGI
│   └── asgi.py           # Configuration ASGI
│
│── db.sqlite3            # Base de données SQLite
│── manage.py             # Outil de gestion Django
│── requirements.txt      # Dépendances du projet
```

## 🔐 Authentification et Permissions

- **Administrateurs** : Accès complet à la gestion des utilisateurs, véhicules et remplacements.  
- **Employés** : Gestion des demandes de remplacement.  
- **Clients** : Consultation de leurs véhicules et soumission des demandes de remplacement.  

## 🛠️ Déploiement (Production)

Pour exécuter l’application sur un serveur de production :

1. **Appliquer les migrations**  
   ```bash
   python manage.py migrate
   ```

2. **Collecter les fichiers statiques**  
   ```bash
   python manage.py collectstatic
   ```

3. **Exécuter avec Gunicorn (si déployé sur Linux)**  
   ```bash
   gunicorn carserv.wsgi:application --bind 0.0.0.0:8000
   ```

## 🤝 Contributions

Les contributions sont les bienvenues ! Merci de forker ce projet et de soumettre vos améliorations via une pull request.
