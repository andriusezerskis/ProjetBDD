SELECT medicament.nom_commercial, medicament.dci,MAX(prescription.date_prescription) AS derniere_prescription
FROM medicament -- On selectionne la table medicament
LEFT JOIN prescription ON medicament.id_medicament = prescription.id_medicament -- On fait une jointure avec la table prescription
GROUP BY  medicament.nom_commercial, medicament.dci -- On groupe par nom_commercial et dci
HAVING MAX(prescription.date_prescription) < DATE 'YOUR_DATE' OR MAX(prescription.date_prescription) IS NULL -- On filtre par date
ORDER BY medicament.nom_commercial; -- On trie par ordre croissant

