
SELECT
  medecin.nom AS medecin_nom,
  medecin.id_specialite AS medecin_id_specialite,
  medicament_conditionnement.nom_commercial AS medicament_nom,
  medicament.id_systeme_anatomique AS medicament_systeme_anatomique

FROM prescription
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami
INNER JOIN medicament_conditionnement ON prescription.id_medicament = medicament_conditionnement.id_medicament
INNER JOIN medicament ON prescription.id_medicament = medicament.id_medicament
where not exists(select null from specialite_systeme_anatomique ssa where ssa.id_systeme_anatomique = medicament.id_systeme_anatomique and ssa.id_specialite = medecin.id_specialite)
ORDER BY medecin.nom, medicament_conditionnement.nom_commercial;

