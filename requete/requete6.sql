SELECT
  medecin.inami AS medecin_inami,
  medecin.nom AS medecin_nom,
  STRING_AGG(DISTINCT medicament.nom_commercial, ', ') AS medicament_noms
FROM prescription
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami
INNER JOIN medicament ON prescription.id_medicament = medicament.id_medicament
WHERE NOT EXISTS (
  SELECT NULL 
  FROM specialite_systeme_anatomique ssa 
  WHERE ssa.id_systeme_anatomique = medicament.id_systeme_anatomique 
  AND ssa.id_specialite = medecin.id_specialite
)
GROUP BY medecin.inami, medecin.nom;
