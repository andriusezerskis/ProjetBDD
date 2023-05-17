SELECT dci, nom_commercial, conditionnement
FROM medicament
WHERE dci = 'YOUR_DCI'
ORDER BY nom_commercial ASC, conditionnement ASC;
