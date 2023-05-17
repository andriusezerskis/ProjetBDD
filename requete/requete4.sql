SELECT DISTINCT p.NISS, p.nom, p.prenom, p.date_de_naissance, p.mail, p.telephone, pr.date_vente
FROM patient p
JOIN prescription pr ON p.NISS = pr.NISS_patient
JOIN medicament m ON pr.id_medicament = m.id_medicament
WHERE m.nom_commercial = 'YOUR_MEDICAMENT'
AND pr.date_vente >= 'YOUR_DATE';
