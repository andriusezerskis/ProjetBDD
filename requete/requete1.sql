SELECT dci, nom_commercial, conditionnement
FROM medicament
INNER JOIN medicament_conditionnement ON medicament_conditionnement.id_medicament = medicament.id_medicament
ORDER BY dci ASC, conditionnement ASC;

--- SI il faut faire par rapport a un DCI donner en parametre
-- SELECT dci, nom_commercial, conditionnement
-- FROM medicament
-- INNER JOIN medicament_conditionnement ON medicament_conditionnement.id_medicament = medicament.id_medicament
-- WHERE dci = 'YOUR_DCI'
-- ORDER BY nom_commercial ASC, conditionnement ASC;
