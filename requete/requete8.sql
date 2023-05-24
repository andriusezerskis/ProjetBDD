SELECT nom, COUNT(nom) AS value_occurrence -- On compte le nombre de fois que le nom de la pathologie apparait
FROM diagnostique -- On selectionne la table diagnostique
INNER JOIN pathologie ON diagnostique.id_pathologie = pathologie.id_pathologie -- On fait une jointure avec la table pathologie
GROUP BY nom -- On groupe par nom
ORDER BY value_occurrence DESC -- On trie par ordre décroissant
LIMIT 1; -- On limite à 1
