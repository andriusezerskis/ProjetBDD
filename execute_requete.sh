#!/bin/bash

# Variables
DATABASE="dossier_medical"
SQL_FILE="dossier_medical.sql"
DB_PATH="/Users/matias/vmcode/ProjetBDD"

if [ $# -ne 1 ]; then
    echo "Usage: $0 [nom_fichier_requete]"
    exit 1
fi

REQUETE_FILE=$1

cd $DB_PATH
sudo -u postgres psql -d $DATABASE -f $REQUETE_FILE