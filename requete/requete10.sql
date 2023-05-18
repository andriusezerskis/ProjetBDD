SELECT
  medicament.nom_commercial,
  medicament.dci,
  MAX(prescription.date_prescription) AS derniere_prescription
FROM medicament
LEFT JOIN prescription ON medicament.id_medicament = prescription.id_medicament
GROUP BY  medicament.nom_commercial, medicament.dci
HAVING MAX(prescription.date_prescription) < DATE 'YOUR_DATE' OR MAX(prescription.date_prescription) IS NULL
ORDER BY medicament.nom_commercial;
