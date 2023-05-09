


SELECT
  nom,
  COUNT(nom) AS value_occurrence 

FROM diagnostic
INNER JOIN pathologie ON pathologie_id = pathologie.id

GROUP BY 
  nom

ORDER BY 
  value_occurrence DESC

LIMIT 1;