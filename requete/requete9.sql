SELECT patient.NISS, patient.nom, COUNT(DISTINCT prescription.inami_medecin) AS value_occurrence
FROM prescription -- On selectionne la table prescription
INNER JOIN patient ON prescription.NISS_patient = patient.NISS -- On fait une jointure avec la table patient
GROUP BY patient.NISS, patient.nom -- On groupe par NISS et nom
ORDER BY value_occurrence ASC; -- On trie par ordre croissant
