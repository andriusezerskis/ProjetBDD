SELECT
  medecin.nom AS medecin_nom,
  medicament.nom_commercial AS medicament_nom,
  medecin.specialite AS medecin_specialite,
  specialite.medicament_systeme_anatomique AS medicament_specialite
FROM prescription
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami
INNER JOIN medicament ON prescription.medicament_id = medicament.id
INNER JOIN specialite ON medecin.specialite = specialite.name
WHERE medicament.systeme_anatomique <> specialite.medicament_systeme_anatomique
ORDER BY medecin.nom, medicament.nom_commercial;
