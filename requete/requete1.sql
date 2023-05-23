SELECT dci, nom_commercial, conditionnement -- On sélectionne les colonnes qui nous intéressent
FROM medicament -- On sélectionne la table qui nous intéresse
WHERE dci = 'YOUR_DCI' -- On filtre sur la DCI qui nous intéresse
ORDER BY nom_commercial ASC, conditionnement ASC; -- On trie par nom commercial puis par conditionnement

