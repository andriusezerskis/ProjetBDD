SELECT
  medicament_conditionnement.nom_commercial,
  medicament.dci,
  MAX(prescription.date_prescription) AS derniere_prescription
FROM medicament
LEFT JOIN prescription ON medicament.id_medicament = prescription.id_medicament
INNER JOIN medicament_conditionnement ON medicament_conditionnement.id_medicament = medicament.id_medicament


WHERE medicament.id_medicament NOT IN (
  SELECT DISTINCT id_medicament
  FROM prescription
  WHERE date_prescription >= DATE 'YOUR_DATE'
)
GROUP BY  medicament_conditionnement.nom_commercial, medicament.dci
HAVING MAX(prescription.date_prescription) IS NOT NULL
ORDER BY medicament_conditionnement.nom_commercial;
