
-- Création de la table 'patient'
CREATE TABLE patient (
    NISS VARCHAR(15) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    genre INT NOT NULL,
    date_de_naissance DATE NOT NULL,
    mail VARCHAR(100),
    telephone VARCHAR(15),
    inami_medecin VARCHAR(15) NOT NULL,
    inami_pharmacien VARCHAR(15) NOT NULL
);


-- Création de la table 'medecin'
CREATE TABLE medecin (
    inami VARCHAR(15) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    mail VARCHAR(100),
    specialite VARCHAR(50) NOT NULL,
    telephone VARCHAR(15)
);

-- Création de la table 'pharmacien'
CREATE TABLE pharmacien (
    inami VARCHAR(15) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    mail VARCHAR(100),
    telephone VARCHAR(15)
);

-- Création de la table 'pathologie'
CREATE TABLE pathologie (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    systeme_anatomique VARCHAR(100) NOT NULL
);

-- Création de la table 'medicament'
CREATE TABLE medicament (
    id SERIAL PRIMARY KEY,
    dci VARCHAR(100) NOT NULL,
    nom_commercial VARCHAR(100) NOT NULL,
    systeme_anatomique VARCHAR(100) NOT NULL,
    conditionnement INT NOT NULL
);

-- Création de la table 'diagnostic'
CREATE TABLE diagnostic (
    id SERIAL PRIMARY KEY,
    NISS_patient VARCHAR(15) NOT NULL,
    date_diagnostic DATE NOT NULL,
    pathologie_id INT NOT NULL,
    FOREIGN KEY (NISS_patient) REFERENCES patient(NISS),
    FOREIGN KEY (pathologie_id) REFERENCES pathologie(id)
);

-- Création de la table 'prescription'
CREATE TABLE prescription (
    id SERIAL PRIMARY KEY,
    inami_medecin VARCHAR(15) NOT NULL,
    inami_pharmacien VARCHAR(15) NOT NULL,
    medicament_id INT NOT NULL,
    NISS_patient VARCHAR(15) NOT NULL,
    date_prescription DATE NOT NULL,
    duree_traitement INT NOT NULL,
    FOREIGN KEY (inami_medecin) REFERENCES medecin(inami),
    FOREIGN KEY (inami_pharmacien) REFERENCES pharmacien(inami),
    FOREIGN KEY (medicament_id) REFERENCES medicament(id),
    FOREIGN KEY (NISS_patient) REFERENCES patient(NISS)
);

-- Création de la table 'specialite'
CREATE TABLE specialite (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    medicament_systeme_anatomique VARCHAR(100) NOT NULL
);
