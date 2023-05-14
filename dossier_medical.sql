
-- Création de la table 'specialite'
CREATE TABLE specialite (
    id_specialite SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL
);

create unique index uk_specialite on specialite(nom);


CREATE TABLE systeme_anatomique
(
    id_systeme_anatomique serial PRIMARY key,
    nom varchar(50) NOT NULL
);


create unique index uk_systeme_anatomique on systeme_anatomique (nom);



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
    id_specialite int,
    telephone VARCHAR(15),
    FOREIGN KEY (id_specialite) REFERENCES specialite(id_specialite)
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
    id_pathologie SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
   );


create unique index uk_pathologie on pathologie (nom);


CREATE TABLE pathologie_specialite (
    id_pathologie int NOT NULL,
    id_specialite int NOT NULL,
    FOREIGN KEY (id_pathologie) REFERENCES pathologie(id_pathologie),
    FOREIGN KEY (id_specialite) REFERENCES specialite(id_specialite)
);



create unique index uk_pathologie_specialite on pathologie_specialite (id_pathologie, id_specialite);






-- Création de la table 'medicament'
CREATE TABLE medicament (
    id_medicament SERIAL PRIMARY KEY,
    dci VARCHAR(100) NOT NULL,
    id_systeme_anatomique int NOT NULL,
    FOREIGN KEY (id_systeme_anatomique) REFERENCES systeme_anatomique(id_systeme_anatomique)
);


create unique index uk_medicament on medicament (dci);


CREATE TABLE medicament_conditionnement (
    id_medicament INT NOT NULL,
    nom_commercial VARCHAR(100) NOT NULL,
    conditionnement INT NOT NULL,
    FOREIGN KEY (id_medicament) REFERENCES medicament(id_medicament)
);


create unique index uk_medicament_conditionnement on medicament_conditionnement (id_medicament, nom_commercial, conditionnement);


-- Création de la table 'diagnostic'
CREATE TABLE diagnostique (
    id_diagnostique SERIAL PRIMARY KEY,
    NISS_patient VARCHAR(15) NOT NULL,
    date_diagnostic DATE NOT NULL,
    id_pathologie INT NOT NULL,
    FOREIGN KEY (NISS_patient) REFERENCES patient(NISS),
    FOREIGN KEY (id_pathologie) REFERENCES pathologie(id_pathologie)
);

-- Création de la table 'prescription'
CREATE TABLE prescription (
    id SERIAL PRIMARY KEY,
    inami_medecin VARCHAR(15) NOT NULL,
    inami_pharmacien VARCHAR(15) NOT NULL,
    id_medicament INT NOT NULL,
    NISS_patient VARCHAR(15) NOT NULL,
    date_prescription DATE NOT NULL,
    date_vente DATE NOT NULL,
    duree_traitement INT NOT NULL,
    FOREIGN KEY (inami_medecin) REFERENCES medecin(inami),
    FOREIGN KEY (inami_pharmacien) REFERENCES pharmacien(inami),
    FOREIGN KEY (id_medicament) REFERENCES medicament(id_medicament),
    FOREIGN KEY (NISS_patient) REFERENCES patient(NISS)
);



CREATE TABLE specialite_systeme_anatomique
(
    id_specialite int not null,
    id_systeme_anatomique int not null,
    FOREIGN KEY (id_specialite) REFERENCES specialite(id_specialite),
    FOREIGN KEY (id_systeme_anatomique) REFERENCES systeme_anatomique(id_systeme_anatomique)
);



create unique index on specialite_systeme_anatomique (id_specialite, id_systeme_anatomique);





