SELECT p.NISS, p.nom, p.prenom, p.date_de_naissance, p.mail, p.telephone
FROM patient p
JOIN prescription pr ON p.NISS = pr.NISS_patient
JOIN medicament m ON pr.id_medicament = m.id_medicament
WHERE m.dci = 'YOUR_DCI'
AND pr.date_vente + pr.duree_traitement * INTERVAL '1 day' < CURRENT_DATE -- * 1 day pour transformer int en date
AND NOT EXISTS (
    SELECT 1
    FROM prescription pr2
    JOIN medicament m2 ON pr2.id_medicament = m2.id_medicament
    WHERE pr2.NISS_patient = p.NISS
    AND m2.dci = 'YOUR_DCI'
    AND pr2.date_vente > pr.date_vente
);
