SELECT
patient.nom,
  COUNT( DISTINCT prescription.inami_medecin) AS value_occurrence 

FROM prescription
INNER JOIN patient ON prescription.NISS_patient = patient.NISS

GROUP BY 
  patient.nom


