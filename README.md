# EpicEventsCRM

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## Résumé

Solution CRM permettant la gestion d'évènements dans une base de données composée d'**utilisateurs**, séparés en deux 
groupes :

- Equipe de vente ("SalesTeam")
- Equipe de support ("SupportTeam")

Ainsi que de **clients**, **contrats** et **évènements**.

Chaque contrat est lié à **un et un seul** évènement.
Chaque client, contrat est associé à un seul membre de l'équipe de vente.
Chaque évènement est associé à un seul membre de l'équipe de support.

Seul un **administrateur** peut créer un nouvel utilisateur et **définir son groupe**. 
De plus il possède un **accès complet** 
en modification/suppression sur toute la base.<br>
Un utilisateur n'a accès en **lecture** aux objets de la base avec lesquels il possède un lien **direct/indirect**.<br>
Un utilisateur n'a accès en **modification** qu'aux objets de la base avec lesquels il possède in lien **direct**.<br>


(Exemple: Un membre de l'équipe de support peut voir le client A pour lequel il est attribué comme contact d'un 
évènement du client A.
Un membre de l'équiê de vente peut voir les contrats du client B s'il est le contact de vente du client B. 
Cependant, s'il n'est pas le contact associé aux contrats, ceux-ci seront en lecture seule.)

L'application possède un version **API** avec des **endpoints** pour chaque object qui compose la solution CRM <br> 
(**/clients/, /contracts/, /events/**).

L'ensemble de ses règles s'applique au front-end (django-admin) qu'à l'API gérer pa DRF 
([django-rest-framework](https://www.django-rest-framework.org/topics/documenting-your-api/)).<br>


Par défaut, à la création d'un client/contrat, c'est l'utilisateur authentifié qui est attribué comme contact de vente.
Il faut faire appel à un administrateur pour changer l'utilisateur rattaché à un client/contrat (les évènements 
étant pris en charge par l'équipe de vente, ils, peuvent modifier l'utilisateur associé comme contact du support 
en plus des administrateurs).

Un serveur PostgreSQL est nécéssaire pour héberger la base de donnée utilisé par défaut dans les settings du projet. 
([PostgreSQL docs](https://www.postgresql.org/docs/current/runtime.html), 
[Création d'une base de donnée](https://www.postgresql.org/docs/14/sql-createdatabase.html))

Les logs d'exceptions sont gérés par le package Sentry. ([Sentry-python](https://github.com/getsentry/sentry-python))


## Démarrage

Une fois l'appliction télécharger, pour mettre en place :

1. A partir de votre terminal, se mettre au niveau du répertoire "EpicEventsCRM".


2. Créer un environnement virtuel avec la commande:

   `py -m venv venv`


3. Activer l'environnement virtuel:

   `venv\Scripts\activate`


4. Installer les bibliothèques nécessaires depuis le répertoire "EpicEventsCRM":

   `pip install -r requirements.txt`

5. Configurer votre base de donnée (PostgreSQL par défaut) dans le fichier settings:
   <pre>
   DATABASES = {
      'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_postgres_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   </pre>
   
6. Lancer le serveur Django:
   - Pour initialiser une base de donnée :
   

      `py manage.py migrate client` 
      `py manage.py migrate contract` 
      `py manage.py migrate event`
      `py manage.py migrate authentication` 
      `py manage.py migrate`
       # L'ORDRE DES MIGRATIONS EST IMPORTANT
       # POUR LE DEPLOIEMENT DES GROUPES/DROITS
      `py manage.py runserver` 

7. Créer un administrateur:
   
   `py manage.py createsuperuser`
   
   Utiliser ensuite ces identifiants pour utiliser la plateforme front-end (endpoint: /admin/) ou tester les 
   différents endpoints.
