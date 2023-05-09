SELECT
  medicament.nom_commercial,
  COUNT(medicament.nom_commercial) AS value_occurrence 

FROM prescription
INNER JOIN patient ON NISS_patient = patient.NISS
INNER JOIN medicament ON medicament_id = medicament.id

WHERE patient.date_de_naissance IN (BETWEEN DATE '01-01-1950' AND DATE '1959-01-01', BETWEEN DATE '01-01-1960' AND DATE '1969-01-01' )

GROUP BY 
  medicament.nom_commercial

ORDER BY 
  value_occurrence DESC

LIMIT 1;