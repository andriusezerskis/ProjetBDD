SELECT m.specialite
FROM medecin m
INNER JOIN prescription p ON m.inami = p.inami_medecin
INNER JOIN medicament med ON p.medicament_id = med.id
INNER JOIN specialite s ON m.specialite = s.name AND med.systeme_anatomique = s.medicament_systeme_anatomique
GROUP BY m.specialite
ORDER BY COUNT(*) DESC
LIMIT 1;
