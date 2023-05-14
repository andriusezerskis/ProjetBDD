SELECT s.nom
FROM medecin m
INNER JOIN prescription p ON m.inami = p.inami_medecin
INNER JOIN medicament med ON p.id_medicament = med.id_medicament
INNER JOIN specialite s ON m.id_specialite = s.id_specialite 
INNER JOIN systeme_anatomique sa ON med.id_systeme_anatomique = sa.id_systeme_anatomique
INNER JOIN specialite_systeme_anatomique ssa ON ssa.id_specialite = s.id_specialite AND med.id_systeme_anatomique = ssa.id_systeme_anatomique
GROUP BY s.nom
ORDER BY COUNT(*) DESC
LIMIT 1;
