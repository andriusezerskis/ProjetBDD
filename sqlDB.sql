-- public."Médecin" definition
-- Drop table
-- DROP TABLE public."Médecin";
CREATE TABLE public."Médecin" (
    medecin varchar(50) NULL,
    inami int4 NULL,
    mail varchar(50) NULL,
    nom varchar(50) NULL,
    specialite varchar(50) NULL,
    telephone int4 NULL
);
-- public.médicament definition
-- Drop table
-- DROP TABLE public.médicament;
CREATE TABLE public.médicament (
    dci varchar(50) NULL,
    "nom Commercial" varchar(50) NULL,
    "système anatomique" varchar(50) NULL,
    conditionnement int4 NULL
);
-- public.pathologie definition
-- Drop table
-- DROP TABLE public.pathologie;
CREATE TABLE public.pathologie (
    "Dépendance à la caféine" varchar(50) NULL,
    addictologie varchar(50) NULL
);
-- public.patient definition
-- Drop table
-- DROP TABLE public.patient;
CREATE TABLE public.patient (
    niss_patient int4 NULL,
    medecin varchar(50) NULL,
    inami_medecin int4 NULL,
    pharmacien varchar(50) NULL,
    inami_pharmacien int4 NULL,
    medicament_nom_commercial varchar(50) NULL,
    dci varchar(50) NULL,
    date_prescription varchar(50) NULL,
    date_vente varchar(50) NULL,
    duree_traitement int4 NULL
);
-- public.pharmacien definition
-- Drop table
-- DROP TABLE public.pharmacien;
CREATE TABLE public.pharmacien (
    pharmacien varchar(50) NULL,
    inami int4 NULL,
    mail varchar(50) NULL,
    nom varchar(50) NULL,
    tel int4 NULL,
);
-- public.prescription definition
-- Drop table
-- DROP TABLE public.prescription;
CREATE TABLE public.prescription ();
-- public.traitement definition
-- Drop table
-- DROP TABLE public.traitement;
CREATE TABLE public.traitement ();