SELECT s.nom -- On sélectionne les colonnes qui nous intéressent
FROM medecin m -- On sélectionne la table qui nous intéresse
INNER JOIN prescription p ON m.inami = p.inami_medecin -- On joint la table prescription
INNER JOIN specialite s ON m.id_specialite = s.id_specialite -- On joint la table specialite
GROUP BY s.nom -- On groupe par nom
ORDER BY COUNT(*) DESC -- On trie par nombre de prescriptions décroissant
LIMIT 1; -- On limite à 1 résultat
