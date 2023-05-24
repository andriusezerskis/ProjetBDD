SELECT nom -- On sélectionne les colonnes qui nous intéressent
FROM pathologie -- On sélectionne la table qui nous intéresse
WHERE id_pathologie IN ( -- On filtre sur les pathologies qui nous intéressent
    SELECT id_pathologie -- On sélectionne la colonne qui nous intéresse
    FROM pathologie_specialite -- On sélectionne la table qui nous intéresse
    GROUP BY id_pathologie -- On groupe par id_pathologie
    HAVING COUNT(*) = 1 -- On filtre sur les pathologies qui n'ont qu'une seule spécialité
);
