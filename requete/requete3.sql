SELECT m.specialite
FROM medecin m
INNER JOIN prescription p ON m.inami = p.inami_medecin
INNER JOIN medicament med ON p.id_medicament = med.id_medicament
INNER JOIN specialite s ON m.id_specialite = s.id_specialite AND med.systeme_anatomique = s.medicament_systeme_anatomique
GROUP BY m.specialite
ORDER BY COUNT(*) DESC
LIMIT 1;
