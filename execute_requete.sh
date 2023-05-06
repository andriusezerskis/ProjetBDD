#!/bin/bash

# Variables
DATABASE="dossier_medical"
SQL_FILE="dossier_medical.sql"
REQUETE_FILE="requete1.sql"
DB_PATH="/Users/matias/vmcode/ProjetBDD"

# Importation du fichier SQL
cd $DB_PATH
sudo -u postgres psql -d $DATABASE -f $REQUETE_FILE
