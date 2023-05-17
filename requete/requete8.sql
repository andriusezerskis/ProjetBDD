SELECT
  nom,
  COUNT(nom) AS value_occurrence 
FROM diagnostique
INNER JOIN pathologie ON diagnostique.id_pathologie = pathologie.id_pathologie
GROUP BY nom
ORDER BY value_occurrence DESC
LIMIT 1;