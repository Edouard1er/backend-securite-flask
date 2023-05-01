# forum_etudiant_backend
## Backend de l'application de forum etudiant

## Configuration de l'environnement

### Avant de pouvoir utiliser le backend, vous devez vous assurer que votre environnement dispose  des éléments suivants :

    Git : vous pouvez l'installer depuis le lien suivant : https://git-scm.com/downloads
    Python 3 ou supérieur installé sur votre machine
    Un serveur MySQL : vous pouvez utiliser WAMP Server qui contient MySQL. Si vous préférez installer MySQL directement, 
    vous pouvez le télécharger depuis le lien suivant : https://dev.mysql.com/downloads/

Vous aurez également besoin d'un éditeur de texte ou d'un IDE comme Visual Studio Code. Vous pouvez l'installer depuis le lien 
suivant : https://code.visualstudio.com/download

## Installation

### Voici les étapes à suivre pour installer et exécuter le backend :

    Clonez le projet en utilisant la commande suivante : git clone https://github.com/Edouard1er/backend-securite-flask
    Lancez le serveur MySQL
    Exécutez le script SQL attaché au projet pour créer la base de données en local
    Ouvrez le dossier du projet dans Visual Studio Code
    Si vous voulez creer un environnment virtuel pour installer les dependance, lancez ces deux commandes avant d'installer les dependances:

    pip install virtualenv
    env\Scripts\activate

    Installez les dépendances de l'application en exécutant : pip install -r requirements.txt
    Créez un fichier .env à la racine du projet et y ajouter les variables d'environnement suivantes :

    DB_USER=<Votre user> ex: root
    DB_PASSWORD=<Votre password> 
    DB_HOST=<Votre host> ex: localhost
    DB_NAME=forum_univ
    SECRET_KEY=<votre cle secrete pour le JWT token> (32 caracteres)


**Lancement**

    Lancer l'application en exécutant : flask run
    Accéder à l'application en utilisant l'URL http://localhost:5000.

## API Endpoints

### Voici les endpoints disponibles dans l'API de ce projet :

**Authentification**

**Admin**

**Utlisateur**

**Messages**

**Forums**

**Categories de forum**

**Commentaires de forum**

**Temoignages**

**Amis**




### Bonne utilisation !