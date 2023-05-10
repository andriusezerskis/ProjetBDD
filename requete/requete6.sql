SELECT
  medecin.nom AS medecin_nom,
  medecin.specialite AS medecin_specialite,
  medicament.nom_commercial AS medicament_nom,
  specialite.name AS medicament_specialite
FROM prescription
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami
INNER JOIN medicament ON prescription.medicament_id = medicament.id
INNER JOIN specialite ON medicament.systeme_anatomique = specialite.medicament_systeme_anatomique
WHERE medecin.specialite <> specialite.name
ORDER BY medecin.nom, medicament.nom_commercial;
