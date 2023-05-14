SELECT p.NISS, p.nom, p.prenom, p.date_de_naissance, p.mail, p.telephone
FROM patient p
JOIN prescription pr ON p.NISS = pr.NISS_patient
JOIN medicament m ON pr.id_medicament = m.id_medicament
WHERE m.dci = 'BEVACIZUMAB'
AND pr.date_vente + pr.duree_traitement * INTERVAL '1 day' < CURRENT_DATE -- * 1 day pour transformer int en date
GROUP BY p.NISS, p.nom, p.prenom, p.date_de_naissance, p.mail, p.telephone;
