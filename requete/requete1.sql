SELECT dci, nom_commercial, conditionnement
FROM medicament
INNER JOIN medicament_conditionnement ON medicament_conditionnement.id_medicament = medicament.id_medicament
ORDER BY dci ASC, conditionnement ASC;
