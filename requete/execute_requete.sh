#!/bin/bash

# Variables
DATABASE="dossier_medical"
SQL_FILE="dossier_medical.sql"

if [ $# -lt 1 ]; then
    echo "Usage: $0 [nom_fichier_requete] [date (optional)]"
    exit 1
fi

REQUETE_FILE=$1
if [ "$REQUETE_FILE" == "requete10.sql" ]; then
    if [ $# -ne 2 ]; then
        echo "Usage: $0 requete10.sql [date]"
        exit 1
    fi
    DATA_INPUT=$2
    ##### GPT qui m'a dit ça ######
    ESCAPED_DATA_INPUT=$(echo "$DATA_INPUT" | sed 's/\//\\\//g')
    QUOTED_ESCAPED_DATA_INPUT="'$ESCAPED_DATA_INPUT'"
    sed "s/'YOUR_DATE'/$QUOTED_ESCAPED_DATA_INPUT/g" $REQUETE_FILE > temp_requete10.sql
    sudo -u postgres psql -d $DATABASE -f temp_requete10.sql
    rm temp_requete10.sql
    #############################
else
    sudo -u postgres psql -d $DATABASE -f $REQUETE_FILE
fi
