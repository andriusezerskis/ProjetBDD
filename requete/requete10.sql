SELECT
  medicament.nom_commercial,
  medicament.dci,
  MAX(prescription.date_prescription) AS derniere_prescription
FROM medicament
LEFT JOIN prescription ON medicament.id = prescription.medicament_id
WHERE medicament.id NOT IN (
  SELECT DISTINCT medicament_id
  FROM prescription
  WHERE date_prescription >= DATE 'YOUR_DATE'
)
GROUP BY  medicament.nom_commercial, medicament.dci
HAVING MAX(prescription.date_prescription) IS NOT NULL
ORDER BY medicament.nom_commercial;
