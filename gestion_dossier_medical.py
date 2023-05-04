import psycopg2
import re
import os


# Modèle
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
            cursor.execute("SELECT * FROM patient WHERE NISS=%s", (NISS_patient,))
            patient_info = cursor.fetchone()

            # diagnostics du patient
            cursor.execute("SELECT * FROM diagnostic WHERE NISS_patient=%s", (NISS_patient,))
            diagnostics = cursor.fetchall()

            # prescriptions du patient
            cursor.execute("SELECT * FROM prescription WHERE NISS_patient=%s", (NISS_patient,))
            prescriptions = cursor.fetchall()

            # informations des médecins ayant prescrit les médicaments au patient
            doctors = set([prescription[1] for prescription in prescriptions])
            doctor_info = []
            for inami in doctors:
                cursor.execute("SELECT * FROM medecin WHERE inami=%s", (inami,))
                doctor_info.append(cursor.fetchone())

            # informations des pharmaciens ayant délivré les médicaments au patient
            pharmacists = set([prescription[2] for prescription in prescriptions])
            pharmacist_info = []
            for inami in pharmacists:
                cursor.execute("SELECT * FROM pharmacien WHERE inami=%s", (inami,))
                pharmacist_info.append(cursor.fetchone())

            # informations sur les médicaments prescrits au patient
            medicaments = set([prescription[3] for prescription in prescriptions])
            medicament_info = []
            for medicament_id in medicaments:
                cursor.execute("SELECT * FROM medicament WHERE id=%s", (medicament_id,))
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
        tables = ['patient', 'medecin', 'pharmacien', 'pathologie', 'medicament', 'diagnostic', 'prescription', 'specialite']
        with self.conn.cursor() as cursor:
            for table_name in tables:
                cursor.execute(f'TRUNCATE {table_name} CASCADE')
            self.conn.commit()


        
        
        
        
        
    
# Contrôleur
class Controller:
    def __init__(self):
        self.db = Database()
        self.view = View(self)
        self.view.main_menu()

    def add_patient(self):
        niss = self.view.ask_niss()
        nom = self.view.ask_nom()
        prenom = self.view.ask_prenom()
        genre = self.view.ask_genre()
        date_de_naissance = self.view.ask_date_de_naissance()
        mail = self.view.ask_mail()
        telephone = self.view.ask_telephone()
        inami_medecin = self.view.ask_inami()
        inami_pharmacien = self.view.ask_inami()
        succes = self.db.add_patient(niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
        if succes:
            data = {"NISS": niss, "nom": nom, "prenom": prenom, "genre": genre, 
                "date_de_naissance": date_de_naissance, "mail": mail, "telephone": telephone, 
                "inami_medecin": inami_medecin, "inami_pharmacien": inami_pharmacien}
            self.view.print_summary("Patient", "ajouté(e)", data)
        else:
            self.view.display_error("Un patient avec ce numéro NISS existe déjà.")
        self.view.main_menu()

    def add_medecin(self):
        inami = self.view.ask_inami()
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        specialite = self.view.ask_specialite()
        telephone = self.view.ask_telephone()
        success = self.db.add_medecin(inami, nom, mail, specialite, telephone)
        if success:
            data = {"inami": inami, "nom": nom, "mail": mail, "specialite": specialite, "telephone": telephone}
            self.view.print_summary("Médecin", "ajouté(e)", data)
        else:
            self.view.display_error("Un médecin avec ce numéro INAMI existe déjà.")
        self.view.main_menu()

    def add_pharmacien(self):
        inami = self.view.ask_inami()
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        telephone = self.view.ask_telephone()
        succes = self.db.add_pharmacien(inami, nom, mail, telephone)
        if succes:
            data = {"inami": inami, "nom": nom, "mail": mail, "telephone": telephone}
            self.view.print_summary("Pharmacien", "ajouté(e)", data)
        else:
            self.view.display_error("Un pharmacien avec ce numéro INAMI existe déjà.")
        self.view.main_menu()
        self.view.main_menu()
    
    def login_patient(self):
        niss = self.view.ask_niss()
        date_de_naissance = self.view.ask_date_de_naissance()
        patient = self.db.get_patient(niss, date_de_naissance)
        if patient:
            self.view.patient_menu(patient)
        else:
            self.view.display_error("NISS ou date de naissance incorrects.")
            self.view.main_menu()

    def update_patient_medecin(self, patient):
        inami_medecin = self.view.ask_inami()
        self.db.update_patient_medecin(patient['NISS'], inami_medecin)
        self.view.display_success("Médecin mis à jour avec succès.")
        patient['inami_medecin'] = inami_medecin
        self.view.print_summary("Patient", "mis(e) à jour", patient)
        self.view.main_menu()

    def update_patient_pharmacien(self, patient):
        inami_pharmacien = self.view.ask_inami()
        self.db.update_patient_pharmacien(patient['NISS'], inami_pharmacien)
        self.view.display_success("Pharmacien mis à jour avec succès.")
        patient['inami_pharmacien'] = inami_pharmacien
        self.view.print_summary("Patient", "mis(e) à jour", patient)
        self.view.main_menu()
    
    def view_medical_info(self, patient):
        medical_info = self.db.get_medical_info(patient["NISS"])
        if medical_info:
            self.view.display_medical_info(medical_info)
        else:
            self.view.display_error("Aucune information médicale trouvée.")
        self.view.patient_menu(patient)

        
# Vue
class AskingView:
    
    def ask_niss(self):
        niss = input("Entrez le NISS du patient : ")
        if not re.match(r"^\d{10,15}$", niss):
            print("Le NISS doit être composé de 11 chiffres")
            return self.ask_niss()
        return niss

    def ask_nom(self):
        nom = input("Entrez le nom : ")
        if not re.match(r"^[A-Za-z]+$", nom):
            print("Le nom ne peut contenir que des lettres")
            return self.ask_nom()
        return nom

    def ask_prenom(self):
        prenom = input("Entrez le prénom : ")
        if not re.match(r"^[A-Za-z]+$", prenom):
            print("Le prénom ne peut contenir que des lettres")
            return self.ask_prenom()
        return prenom

    def ask_genre(self):
        genre = input("Entrez le genre du patient : ")
        if not re.match(r"^[0-9]+$", genre):
            print("Le genre doit être un chiffre")
            return self.ask_genre()
        return genre

    def ask_date_de_naissance(self):
        date_de_naissance = input("Entrez la date de naissance du patient (format YYYY-MM-DD : ")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_de_naissance):
            print("La date de naissance doit être au format YYYY-MM-DD")
            return self.ask_date_de_naissance()
        return date_de_naissance

    def ask_inami(self):
        inami = input("Entrez le numéro INAMI : ")
        if not re.match(r"^\d{9,15}$", inami):
            print("Le numéro INAMI doit être composé de 9 à 15 chiffres")
            return self.ask_inami()
        return inami

    def ask_specialite(self):
        specialite = input("Entrez la spécialité : ")
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", specialite):
            print("La spécialité ne peut contenir que des lettres et des espaces")
            return self.ask_specialite()
        return specialite

    def ask_telephone(self):
        telephone = input("Entrez le numéro de téléphone (appuyez sur Entrée pour laisser vide) : ")
        if not telephone:
            return telephone
        elif not re.match(r"^\+?\d{10,15}$", telephone):
            print("Le numéro de téléphone doit être composé de 10 à 15 chiffres")
            return self.ask_telephone()
        return telephone

    def ask_mail(self):
        mail = input("Entrez l'adresse e-mail (appuyez sur Entrée pour laisser vide) : ")
        if not mail:
            return mail
        elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", mail):
            print("L'adresse e-mail doit être valide")
            return self.ask_mail()
        return mail

class View(AskingView):
    
    def __init__(self, controller):
        self.controller = controller
    
    def main_menu(self):
        try:
            print("Bienvenue dans le gestionnaire de dossier médical\n")
            print("1. Ajouter un patient")
            print("2. Ajouter un médecin")
            print("3. Ajouter un pharmacien")
            print("4. Se connecter en tant que patient")
            print("5. Quitter")
            choice = input("Que voulez-vous faire ? ")
            if choice == "1":
                self.controller.add_patient()
            elif choice == "2":
                self.controller.add_medecin()
            elif choice == "3":
                self.controller.add_pharmacien()
            elif choice == "4":
                os.system('clear')
                self.controller.login_patient()
            elif choice == "5":
                exit()
            else:
                print("Choix invalide")
                self.main_menu()
        except KeyboardInterrupt:
            print("\n")
            exit()
        
    
    def patient_menu(self, patient):
        try:
            print(f"\nBonjour {patient['nom']} {patient['prenom']}\n")
            print("Menu patient:")
            print("1. Modifier médecin de référence")
            print("2. Modifier pharmacien de référence")
            print("3. Consulter les informations médicales")
            print("4. Consulter les traitements")
            print("5. Retour")
            choice = input("Que voulez-vous faire ? ")
            if choice == "1":
                self.controller.update_patient_medecin(patient)
            elif choice == "2":
                self.controller.update_patient_pharmacien(patient)
            elif choice == "3":
                self.controller.view_medical_info(patient)
            elif choice == "4":
                print("Consultation des traitements à implémenter.")
                self.patient_menu(patient)
            elif choice == "5":
                self.controller.view.main_menu()
            else:
                print("Choix invalide")
                self.patient_menu(patient)
        except KeyboardInterrupt:
            print("\n")
            exit()


    def display_error(self, error_message):
        print(error_message)

    def display_success(self, success_message):
        print(success_message)

    def print_summary(self, title, action, data):
        os.system('clear')
        print(f"\n{title} {action} avec succès :")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")
    
    def display_medical_info(self, medical_info):
        print("\nInformations médicales :")
        for key, value in medical_info.items():
            print(f"{key}: {value}")
            print("\n")
        print("\n")

    
    
        
if __name__ == "__main__":
    #db = Database()
    #db.clear_database()

    controller = Controller()
    view = View(controller)

    while True:
        view.main_menu()

