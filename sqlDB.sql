-- public."Médecin" definition
-- Drop table
-- DROP TABLE public."Médecin";
CREATE TABLE public."Médecin" (
    inami varchar NULL,
    mail varchar NULL,
    nom varchar NULL,
    specialite varchar NULL,
    telephone varchar NULL,
    CONSTRAINT médecin_pk PRIMARY KEY (inami)
);
-- Permissions
ALTER TABLE public."Médecin" OWNER TO emily;
GRANT ALL ON TABLE public."Médecin" TO emily;
-- public.médicament definition
-- Drop table
-- DROP TABLE public.médicament;
CREATE TABLE public.médicament (
    dci varchar(50) NULL,
    "nom Commercial" varchar(50) NULL,
    "système anatomique" varchar(50) NULL,
    conditionnement int4 NULL,
    CONSTRAINT médicament_pk PRIMARY KEY (dci)
);
-- Permissions
ALTER TABLE public.médicament OWNER TO emily;
GRANT ALL ON TABLE public.médicament TO emily;
-- public.pathologie definition
-- Drop table
-- DROP TABLE public.pathologie;
CREATE TABLE public.pathologie (
    nom varchar(50) NULL,
    systeme_anatomique varchar(50) NULL,
    CONSTRAINT pathologie_pk PRIMARY KEY (nom)
);
-- Permissions
ALTER TABLE public.pathologie OWNER TO emily;
GRANT ALL ON TABLE public.pathologie TO emily;
-- public.dossier_patient definition
-- Drop table
-- DROP TABLE public.dossier_patient;
CREATE TABLE public.dossier_patient (
    niss_patient int4 NULL,
    medecin varchar(50) NULL,
    inami_medecin int4 NULL,
    pharmacien varchar(50) NULL,
    inami_pharmacien int4 NULL,
    medicament_nom_commercial varchar(50) NULL,
    dci varchar(50) NULL,
    date_prescription varchar(50) NULL,
    date_vente varchar(50) NULL,
    duree_traitement int4 NULL,
    CONSTRAINT patient_pk PRIMARY KEY (niss_patient)
);
-- Permissions
ALTER TABLE public.dossier_patient OWNER TO emily;
GRANT ALL ON TABLE public.dossier_patient TO emily;
-- public.pharmacien definition
-- Drop table
-- DROP TABLE public.pharmacien;
CREATE TABLE public.pharmacien (
    inami varchar NULL,
    mail varchar NULL,
    nom varchar NULL,
    telephone varchar NULL,
    CONSTRAINT pharmacien_pk PRIMARY KEY (inami)
);
-- Permissions
ALTER TABLE public.pharmacien OWNER TO emily;
GRANT ALL ON TABLE public.pharmacien TO emily;
-- public.diagnostique definition
CREATE TABLE public.diagnostique (
    niss varchar NULL,
    date_diagnostic varchar NULL,
    naissance varchar NULL,
    pathology varchar NULL,
    specialite varchar NULL,
    serial_number varchar NULL,
    CONSTRAINT diagnostique_pk PRIMARY KEY (serial_number)
);
-- public.specialites definition
CREATE TABLE public.specialites (
    nom varchar NULL,
    medicament1 varchar NULL,
    medicament2 varchar NULL,
    medicament3 varchar NULL,
    CONSTRAINT specialites_pk PRIMARY KEY (nom)
);
-- public.patient definition
CREATE TABLE public.patient (
    niss varchar NULL,
    date_de_naissance varchar NULL,
    genre varchar NULL,
    inami_medecin varchar NULL,
    inami_pharmacien varchar NULL,
    mail varchar NULL,
    nom varchar NULL,
    prenom varchar NULL,
    telephone varchar NULL,
    CONSTRAINT patient_pk PRIMARY KEY (niss)
);