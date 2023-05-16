WITH decenie_medications AS (
  SELECT
    CASE
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1950 AND 1959 THEN '1950-1959'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1960 AND 1969 THEN '1960-1969'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1970 AND 1979 THEN '1970-1979'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1980 AND 1989 THEN '1980-1989'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1990 AND 1999 THEN '1990-1999'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 2000 AND 2009 THEN '2000-2009'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 2010 AND 2019 THEN '2010-2019'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 2020 AND 2029 THEN '2020-2029'
    END AS decenie,
    medicament_conditionnement.nom_commercial
  FROM prescription
  INNER JOIN patient ON NISS_patient = patient.NISS
  INNER JOIN medicament ON prescription.id_medicament = medicament.id_medicament
  INNER JOIN medicament_conditionnement ON medicament_conditionnement.id_medicament = medicament.id_medicament
),
decenie_medications_count AS (
  SELECT
    decenie,
    nom_commercial,
    COUNT(*) AS value_occurrence
  FROM decenie_medications
  GROUP BY decenie, nom_commercial
),
max_medications_per_decenie AS (
  SELECT
    decenie,
    MAX(value_occurrence) AS max_value_occurrence
  FROM decenie_medications_count
  GROUP BY decenie
)
SELECT
  d_m.decenie,
  string_agg(d_m.nom_commercial, ', ') AS medecin_list,
  d_m.value_occurrence
FROM decenie_medications_count d_m
JOIN max_medications_per_decenie m_m_p_d ON d_m.decenie = m_m_p_d.decenie AND d_m.value_occurrence = m_m_p_d.max_value_occurrence
GROUP BY d_m.decenie, d_m.value_occurrence
ORDER BY d_m.decenie;
