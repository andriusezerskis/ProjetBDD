SELECT medecin.inami AS medecin_inami, medecin.nom AS medecin_nom, -- On sélectionne les colonnes qui nous intéressent
  STRING_AGG(DISTINCT medicament.nom_commercial, ', ') AS medicament_noms
FROM prescription -- On sélectionne les tables qui nous intéressent
INNER JOIN medecin ON prescription.inami_medecin = medecin.inami -- On joint la table medecin
INNER JOIN medicament ON prescription.id_medicament = medicament.id_medicament -- On joint la table medicament
WHERE NOT EXISTS ( -- On fait une sous-requête pour exclure les médecins qui prescrivent des médicaments de leur spécialité
  SELECT NULL
  FROM specialite_systeme_anatomique ssa 
  WHERE ssa.id_systeme_anatomique = medicament.id_systeme_anatomique
  AND ssa.id_specialite = medecin.id_specialite
)
GROUP BY medecin.inami, medecin.nom;
