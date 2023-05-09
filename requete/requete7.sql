WITH decade_medications AS (
  SELECT
    CASE
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1950 AND 1959 THEN '1950-1959'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1960 AND 1969 THEN '1960-1969'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1970 AND 1979 THEN '1970-1979'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1980 AND 1989 THEN '1980-1989'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 1990 AND 1999 THEN '1990-1999'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 2000 AND 2009 THEN '2000-2009'
      WHEN EXTRACT(YEAR FROM patient.date_de_naissance) BETWEEN 2010 AND 2020 THEN '2010-2020'
    END AS decade,
    medicament.nom_commercial
  FROM prescription
  INNER JOIN patient ON NISS_patient = patient.NISS
  INNER JOIN medicament ON medicament_id = medicament.id
),

decade_medications_count AS (
  SELECT
    decade,
    nom_commercial,
    COUNT(*) AS value_occurrence
  FROM decade_medications
  GROUP BY decade, nom_commercial
)

SELECT
  dm1.decade,
  dm1.nom_commercial,
  dm1.value_occurrence
FROM decade_medications_count dm1
WHERE dm1.value_occurrence = (
  SELECT MAX(dm2.value_occurrence)
  FROM decade_medications_count dm2
  WHERE dm2.decade = dm1.decade
)
ORDER BY dm1.decade;
