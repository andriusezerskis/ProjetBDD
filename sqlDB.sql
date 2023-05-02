-- public."Médecin" definition
-- Drop table
-- DROP TABLE public."Médecin";
CREATE TABLE public."Médecin" (
    totoid int4 NULL,
    dci varchar(50) NULL,
    "nom Commercial" varchar(50) NULL,
    "système anatomique" varchar(50) NULL,
    conditionnement int4 NULL,
    niss_patient int4 NULL,
    medecin varchar(50) NULL,
    inami_medecin int4 NULL,
    pharmacien varchar(50) NULL,
    inami_pharmacien int4 NULL,
    medicament_nom_commercial varchar(50) NULL,
    date_prescription varchar(50) NULL,
    date_vente varchar(50) NULL,
    duree_traitement int4 NULL
);
-- public.pathologie definition
-- Drop table
-- DROP TABLE public.pathologie;
CREATE TABLE public.pathologie ();
-- public.prescription definition
-- Drop table
-- DROP TABLE public.prescription;
CREATE TABLE public.prescription ();
-- public.traitement definition
-- Drop table
-- DROP TABLE public.traitement;
CREATE TABLE public.traitement ();
-- public.médicament definition
-- Drop table
-- DROP TABLE public.médicament;
CREATE TABLE public.médicament ();
-- public.pharmacien definition
-- Drop table
-- DROP TABLE public.pharmacien;
CREATE TABLE public.pharmacien ();
-- public.patient definition
-- Drop table
-- DROP TABLE public.patient;
CREATE TABLE public.patient ();