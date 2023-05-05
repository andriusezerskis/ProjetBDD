import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')

    def add_patient(self, niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien):
        with self.conn.cursor() as cursor:
            # Vérifie si un patient avec le même NISS existe déjà
            cursor.execute("SELECT NISS FROM patient WHERE NISS = %s", (niss,))
            if cursor.fetchone():
                return False  # Le patient existe déjà
            
            sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien))
            self.conn.commit()
            return True  # Le patient a été ajouté avec succès

    def add_medecin(self, inami, nom, mail, specialite, telephone):
        with self.conn.cursor() as cursor:
            # Vérifie si un médecin avec le même numéro INAMI existe déjà
            cursor.execute("SELECT inami FROM medecin WHERE inami = %s", (inami,))
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
            cursor.execute("SELECT inami FROM pharmacien WHERE inami = %s", (inami,))
            if cursor.fetchone():
                return False  # Le pharmacien existe déjà
            
            sql = """INSERT INTO pharmacien (inami, nom, mail, telephone)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (inami, nom, mail, telephone))
            self.conn.commit()
            return True  # Le pharmacien a été ajouté avec succès
    
    def get_patient(self, niss, date_de_naissance):
        sql = "SELECT * FROM patient WHERE NISS = %s AND date_de_naissance = %s"
        cursor = self.conn.cursor()
        
        cursor.execute(sql, (niss, date_de_naissance))
        result = cursor.fetchone()
        if result:
            keys = ["NISS", "nom", "prenom", "genre", "date_de_naissance", "mail", "telephone", "inami_medecin", "inami_pharmacien"]
            return dict(zip(keys, result))
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
            cursor.execute("""
                    SELECT
                        diagnostic.date_diagnostic,
                        pathologie.nom AS nom_pathologie
                    FROM diagnostic
                    JOIN pathologie ON diagnostic.pathologie_id = pathologie.id
                    WHERE diagnostic.NISS_patient = %s
                """, (NISS_patient,))
            diagnostics_info = cursor .fetchall()
        
        return diagnostics_info
    
    def get_traitements(self, NISS_patient):
        # a implementer plus le temps aha 
       # traitements_info = cursor.fetchall()
        return traitements_info

        