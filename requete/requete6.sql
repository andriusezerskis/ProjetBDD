SELECT
  medecin.nom AS medecin_nom,
  medecin.specialite AS medecin_specialite,
  medicament_conditionnement.nom_commercial AS medicament_nom,
  specialite.name AS medicament_specialite
FROM prescription
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami
INNER JOIN medicament_conditionnement ON prescription.id_medicament = medicament_conditionnement.id_medicament
INNER JOIN medicament ON prescription.id_medicament = medicament.id_medicament
INNER JOIN specialite ON medicament.id_systeme_anatomique = specialite.id_medicament_systeme_anatomique
WHERE medecin.specialite <> specialite.name
ORDER BY medecin.nom, medicament_conditionnement.nom_commercial;
