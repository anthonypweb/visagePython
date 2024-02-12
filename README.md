# Instructions pour l'installation et l'utilisation du projet

Ce guide fournit des instructions étape par étape pour installer l'environnement virtuel et les dépendances pour ce projet, ainsi que pour configurer l'extension Python dans Visual Studio Code.

## Installation de l'environnement virtuel

1. Assurez-vous que Python est installé sur votre système. Si ce n'est pas le cas, téléchargez et installez Python à partir de [python.org](https://www.python.org/downloads/).

2. Ouvrez un terminal ou une invite de commande.

3. Accédez au répertoire où vous souhaitez créer l'environnement virtuel.

4. Utilisez la commande suivante pour créer l'environnement virtuel en remplaçant le chemin vers Python par celui de votre installation :
    ```
    C:\Users\2052146\AppData\Local\Programs\Python\Python312\python.exe -m venv mon_env
    ```
   Cela créera un nouvel environnement virtuel appelé `mon_env` dans votre dossier local.

## Activation de l'environnement virtuel

1. Dans le même terminal ou invite de commande, utilisez la commande suivante pour activer l'environnement virtuel :
    ```
    mon_env\Scripts\activate
    ```

## Installation de l'extension Python dans Visual Studio Code

1. Ouvrez Visual Studio Code.

2. Dans le menu  recherchez "Python".

3. Sélectionnez "Python" dans la liste des extensions et cliquez sur "Installer".

## Configuration de l'environnement virtuel dans Visual Studio Code

1. Ouvrez le dossier de votre projet dans Visual Studio Code.

2. Si vous n'avez pas déjà sélectionné l'environnement virtuel pour le projet, ouvrez la palette de commandes et recherchez "Python: Sélectionner l'environnement interpréteur".

3. Choisissez l'environnement virtuel `mon_env` que vous avez créé précédemment.

## Installation des dépendances

1. Assurez-vous que vous êtes dans l'environnement virtuel.

2. Utilisez la commande suivante pour installer les dépendances à partir du fichier requirements.txt :
    ```
    pip install -r requirements.txt
    ```

## Désactivation de l'environnement virtuel

1. Lorsque vous avez terminé de travailler, vous pouvez désactiver l'environnement virtuel en exécutant la commande suivante :
    ```
    deactivate
    ```

## Faire fonctionner la page web

4. Lancez le script Python server.py

5. Une fois le script exécuté, ouvrez votre navigateur web et accédez à l'adresse suivante ou autre le port sera indiqué dans le terminal :
    ```
    http://localhost:5000
    ```

6. Dans les paramètres de votre navigateur, assurez-vous de sélectionner la bonne webcam à utiliser.

7. Lorsque la page web est ouverte pour la première fois, vous devrez  accepter l'accès à la webcam.

# Modifier le répertoire de stockage des photos dans le fichier server.py
UPLOAD_FOLDER = 'chemin/vers/votre/nouveau/dossier/photos'

# Accès au port série 
Cliquer sur le bouton dans la page web et choisissez le port ou arduino es connecté à faire à chaque rafraichissement de la page 