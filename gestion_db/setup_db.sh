#!/bin/bash

# Variables
DATABASE="dossier_medical"
SQL_FILE="dossier_medical.sql"

# Suppression et création de la base de données
sudo -u postgres -i bash -c "psql -c \"DROP DATABASE IF EXISTS $DATABASE;\""
sudo -u postgres -i bash -c "psql -c \"CREATE DATABASE $DATABASE;\""

# Importation du fichier SQL
sudo -u postgres psql -d $DATABASE -f $SQL_FILE

# Vérification de la base de données
sudo -u postgres psql -d $DATABASE -c "\d"

echo "Script terminé."
