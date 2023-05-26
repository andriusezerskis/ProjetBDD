# Projet Dossier Patient Informatisé

## Librairies à installer

Pour installer PostgreSQL et la librairie psycopg2, exécutez les commandes suivantes :

```
sudo apt-get install postgresql
pip install psycopg2  
pip install tabulate
```

## Création de la base de données

- Pour la création de la base de données, exécutez la commande suivante : ```make setup```


## Gestion de la base de données

- Pour initialiser la base de données, exécutez la commande suivante : ```make init```

- Pour effacer les données de la base de données, exécutez la commande suivante : ```make clean```

- Pour afficher les données de la base de données, exécutez la commande suivante : ```make print```

## Lancement de l'application

Pour lancer l'application, exécutez la commande suivante : ```make```

