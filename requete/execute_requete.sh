#!/bin/bash

# Variables
DATABASE="dossier_medical"
SQL_FILE="dossier_medical.sql"

if [ $# -lt 1 ]; then
    echo "Usage: $0 [nom_fichier_requete] [date (optional)] [nom_medicament (optional)]"
    exit 1
fi

REQUETE_FILE=$1
if [ "$REQUETE_FILE" == "requete10.sql" ]; then
    if [ $# -ne 2 ]; then
        echo "Usage: $0 requete10.sql [date]"
        exit 1
    fi
    DATA_INPUT=$2
    ### GPT qui m'a dit ca et ca fonctionne : )
    ESCAPED_DATA_INPUT=$(echo "$DATA_INPUT" | sed 's/\//\\\//g')
    QUOTED_ESCAPED_DATA_INPUT="'$ESCAPED_DATA_INPUT'"
    sed "s/'YOUR_DATE'/$QUOTED_ESCAPED_DATA_INPUT/g" $REQUETE_FILE > temp_requete10.sql
    sudo -u postgres psql -d $DATABASE -f temp_requete10.sql
    rm temp_requete10.sql
elif [ "$REQUETE_FILE" == "requete4.sql" ]; then
    if [ $# -ne 3 ]; then
        echo "Usage: $0 requete4.sql [date] [medicament]"
        exit 1
    fi
    DATE_INPUT=$2
    MEDICAMENT_NAME=$3
    #### pareil GPT qui ma dit ça
    ESCAPED_DATE_INPUT=$(echo "$DATE_INPUT" | sed 's/\//\\\//g')
    QUOTED_ESCAPED_DATE_INPUT="'$ESCAPED_DATE_INPUT'"
    QUOTED_MEDICAMENT_NAME="'$MEDICAMENT_NAME'"
    sed "s/'YOUR_DATE'/$QUOTED_ESCAPED_DATE_INPUT/g; s/'YOUR_MEDICAMENT'/$QUOTED_MEDICAMENT_NAME/g" $REQUETE_FILE > temp_requete4.sql
    sudo -u postgres psql -d $DATABASE -f temp_requete4.sql
    rm temp_requete4.sql
else
    sudo -u postgres psql -d $DATABASE -f $REQUETE_FILE
fi
