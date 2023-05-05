# Projet Dossier Patient Informatisé

## Librairies à installer

Pour installer PostgreSQL et la librairie psycopg2, exécutez les commandes suivantes :

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
pip install psycopg2
```

## Création de la base de données

Suivez les étapes ci-dessous pour créer la base de données :

1. Faites un git clone du projet.

2. Ouvrez le terminal et exécutez les commandes suivantes :
   ```
   1. sudo -u postgres -i
   2. psql
   3. DROP DATABASE IF EXISTS dossier_medical; # si elle est déjà cree
   4. CREATE DATABASE dossier_medical; 
   5. \q   # Pour quitter
   6. cd chemin/dossier/du/dossier
   7. psql -d dossier_medical -f dossier_medical.sql
   8. psql -d dossier_medical
   9. \d   # Vérifie que la base de données est bien créée
   10. \q
   11. exit  # Revenir au terminal normal
   ```

## Gestion de la base de données

-Pour initialiser la base de données, exécutez les commandes suivantes : ```make init```

- Pour effacer les données de la base de données, exécutez les commandes suivantes : ```make clean```

- Pour afficher les données de la base de données, exécutez les commandes suivantes : ```make print```

## Lancement de l'application

Pour lancer l'application, exécutez les commandes suivantes : ```make```

## Liens utiles

Lien Rapport : https://www.overleaf.com/2575596781dzpzqywnxrbz

Lien diagramme : https://lucid.app/lucidchart/674c140e-a4a1-4947-941c-0604ebc53ed2/edit?docId=674c140e-a4a1-4947-941c-0604ebc53ed2&shared=true&invitationId=inv_792710c9-f42c-4286-b3d7-2cd81bf38ae3&page=0_0#
