SELECT s.nom
FROM medecin m
INNER JOIN prescription p ON m.inami = p.inami_medecin
INNER JOIN specialite s ON m.id_specialite = s.id_specialite 
GROUP BY s.nom
ORDER BY COUNT(*) DESC
LIMIT 1;
