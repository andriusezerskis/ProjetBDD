"""
Projet de BDD : réaliser une base de données en SQL.
Date : 26/05/2023
Auteurs : Matias Nieto Navarrete, Andrius Ezerskis, Moïra Vanderslagmolen
Matricules : 502920, 542698, 547486
Section : B-INFO
"""

import psycopg2
from psycopg2 import Error

class Database:
    def __init__(self):
        self.db_config = {
            'host':'localhost',
            'user':'postgres',
            'password':'azertyuiop',
            'dbname':'dossier_medical'
        }

    def _connect(self):
        return psycopg2.connect(**self.db_config)

    def add_patient(self, niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                try:
                    sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien))
                    conn.commit()
                    return True
                except Error:
                    return False

    def add_medecin(self, inami, nom, mail, specialite, telephone):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_specialite FROM specialite WHERE nom = %s", (specialite,))
                result = cursor.fetchone()

                if result is None:
                    print(f"La spécialité {specialite} n'existe pas.")
                    return False

                id_specialite = result[0]

                try:
                    sql = """INSERT INTO medecin (inami, nom, mail, id_specialite, telephone)
                            VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (inami, nom, mail, id_specialite, telephone))
                    conn.commit()
                    return True
                except Error :
                    return False


    def add_pharmacien(self, inami, nom, mail, telephone):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                try:
                    sql = """INSERT INTO pharmacien (inami, nom, mail, telephone)
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (inami, nom, mail, telephone))
                    conn.commit()
                    return True
                except Error :
                    return False

    def get_patient(self, niss, date_de_naissance):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM patient WHERE NISS = %s AND date_de_naissance = %s"
                cursor.execute(sql, (niss, date_de_naissance))
                result = cursor.fetchone()
                if result:
                    keys = ["NISS", "nom", "prenom", "genre", "date_de_naissance", "mail", "telephone", "inami_medecin", "inami_pharmacien"]
                    return dict(zip(keys, result))
                return None

    def update_patient_medecin(self, niss, inami_medecin):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE patient SET inami_medecin = %s WHERE NISS = %s"""
                cursor.execute(sql, (inami_medecin, niss))
                conn.commit()

    def update_patient_pharmacien(self, niss, inami_pharmacien):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                sql = """UPDATE patient SET inami_pharmacien = %s WHERE NISS = %s"""
                cursor.execute(sql, (inami_pharmacien, niss))
                conn.commit()

    def get_medical_info(self, NISS_patient):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                        SELECT
                            diagnostique.date_diagnostic,
                            pathologie.nom AS nom_pathologie
                        FROM diagnostique
                        JOIN pathologie ON diagnostique.id_pathologie = pathologie.id_pathologie
                        WHERE diagnostique.NISS_patient = %s
                    """, (NISS_patient,))
                diagnostics_info = cursor.fetchall()
        
        return diagnostics_info
    
    def get_traitements(self, NISS_patient):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        prescription.date_vente,
                        medicament.nom_commercial,
                        prescription.duree_traitement
                    FROM prescription
                    JOIN medicament ON prescription.id_medicament = medicament.id_medicament
                    WHERE prescription.NISS_patient = %s;
                """, (NISS_patient,))
                traitements_info = cursor.fetchall()
        
        return traitements_info

    
    def get_contact_ref(self, NISS_patient):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        medecin.nom,
                        medecin.mail,
                        medecin.telephone,
                        pharmacien.nom,
                        pharmacien.mail,
                        pharmacien.telephone
                    FROM patient
                    JOIN medecin ON patient.inami_medecin = medecin.inami
                    JOIN pharmacien ON patient.inami_pharmacien = pharmacien.inami
                    WHERE patient.NISS = %s;
                """ , (NISS_patient,))
                contact_info = cursor.fetchone()

        return contact_info

