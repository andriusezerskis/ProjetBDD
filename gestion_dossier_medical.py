import psycopg2

from controller import Controller
from view import View


# Modèle
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')

    def add_patient(self, niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien):
        with self.conn.cursor() as cursor:
            # Vérifie si un patient avec le même NISS existe déjà
            cursor.execute("SELECT NISS FROM patient WHERE NISS = %s", (niss,))
            if cursor.fetchone():
                return False  # Le patient existe déjà

            sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                     VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), %s, %s, %s, %s)"""
            cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance,
                           mail, telephone, inami_medecin, inami_pharmacien))
            self.conn.commit()
            return True  # Le patient a été ajouté avec succès

    def add_medecin(self, inami, nom, mail, specialite, telephone):
        with self.conn.cursor() as cursor:
            # Vérifie si un médecin avec le même numéro INAMI existe déjà
            cursor.execute(
                "SELECT inami FROM medecin WHERE inami = %s", (inami,))
            if cursor.fetchone():
                return False  # Le médecin existe déjà

            sql = """INSERT INTO medecin (inami, nom, mail, specialite, telephone)
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (inami, nom, mail, specialite, telephone))
            self.conn.commit()
            return True  # Le médecin a été ajouté avec succès

    def add_pharmacien(self, inami, nom, mail, telephone):
        with self.conn.cursor() as cursor:
            # Vérifie si un pharmacien avec le même numéro INAMI existe déjà
            cursor.execute(
                "SELECT inami FROM pharmacien WHERE inami = %s", (inami,))
            if cursor.fetchone():
                return False  # Le pharmacien existe déjà

            sql = """INSERT INTO pharmacien (inami, nom, mail, telephone)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (inami, nom, mail, telephone))
            self.conn.commit()
            return True  # Le pharmacien a été ajouté avec succès

    def get_patient(self, niss, date_de_naissance):
        sql = "SELECT * FROM patient WHERE NISS = %s AND date_de_naissance = TO_DATE(%s, 'MM/DD/YYYY')"
        cursor = self.conn.cursor()
        cursor.execute(sql, (niss, date_de_naissance))
        result = cursor.fetchone()

        if result:
            keys = ["NISS", "nom", "prenom", "genre", "date_de_naissance",
                    "mail", "telephone", "inami_medecin", "inami_pharmacien"]
            return dict(zip(keys, result))
        else:
            return None

    def update_patient_medecin(self, niss, inami_medecin):
        print(niss)
        print(inami_medecin)
        with self.conn.cursor() as cursor:
            sql = """UPDATE patient SET inami_medecin = %s WHERE NISS = %s"""
            cursor.execute(sql, (inami_medecin, niss))
            self.conn.commit()

    def update_patient_pharmacien(self, niss, inami_pharmacien):
        with self.conn.cursor() as cursor:
            sql = """UPDATE patient SET inami_pharmacien = %s WHERE NISS = %s"""
            cursor.execute(sql, (inami_pharmacien, niss))
            self.conn.commit()

    def get_medical_info(self, NISS_patient):
        with self.conn.cursor() as cursor:
            # informations du patient
            cursor.execute(
                "SELECT * FROM patient WHERE NISS=%s", (NISS_patient,))
            patient_info = cursor.fetchone()

            # diagnostics du patient
            cursor.execute(
                "SELECT * FROM diagnostic WHERE NISS_patient=%s", (NISS_patient,))
            diagnostics = cursor.fetchall()

            # prescriptions du patient
            cursor.execute(
                "SELECT * FROM prescription WHERE NISS_patient=%s", (NISS_patient,))
            prescriptions = cursor.fetchall()

            # informations des médecins ayant prescrit les médicaments au patient
            doctors = set([prescription[1] for prescription in prescriptions])
            doctor_info = []
            for inami in doctors:
                cursor.execute(
                    "SELECT * FROM medecin WHERE inami=%s", (inami,))
                doctor_info.append(cursor.fetchone())

            # informations des pharmaciens ayant délivré les médicaments au patient
            pharmacists = set([prescription[2]
                              for prescription in prescriptions])
            pharmacist_info = []
            for inami in pharmacists:
                cursor.execute(
                    "SELECT * FROM pharmacien WHERE inami=%s", (inami,))
                pharmacist_info.append(cursor.fetchone())

            # informations sur les médicaments prescrits au patient
            medicaments = set([prescription[3]
                              for prescription in prescriptions])
            medicament_info = []
            for medicament_id in medicaments:
                cursor.execute(
                    "SELECT * FROM medicament WHERE id=%s", (medicament_id,))
                medicament_info.append(cursor.fetchone())

        return {
            'patient_info': patient_info,
            'diagnostics': diagnostics,
            'prescriptions': prescriptions,
            'doctor_info': doctor_info,
            'pharmacist_info': pharmacist_info,
            'medicament_info': medicament_info
        }

    def clear_database(self):
        tables = ['patient', 'medecin', 'pharmacien', 'pathologie',
                  'medicament', 'diagnostic', 'prescription', 'specialite']
        with self.conn.cursor() as cursor:
            for table_name in tables:
                cursor.execute(f'TRUNCATE {table_name} CASCADE')
            self.conn.commit()


if __name__ == "__main__":
    # db = Database()
    # db.clear_database()

    controller = Controller()
    view = View(controller)

    while True:
        view.main_menu()
