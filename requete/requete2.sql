SELECT nom
FROM pathologie
WHERE id_pathologie IN (
    SELECT id_pathologie 
    FROM pathologie_specialite 
    GROUP BY id_pathologie 
    HAVING COUNT(*) = 1
);

