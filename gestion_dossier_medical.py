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
            test = dict(zip(keys, result))
            print(test)
            return test
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

    ############################## A SUPPRIMER ################################
    def del_patient(self, niss):
        with self.conn.cursor() as cursor:
            sql = """DELETE FROM patient WHERE NISS = %s"""
            cursor.execute(sql, (niss,))
            self.conn.commit()
    
    def del_medecin(self, inami):
        with self.conn.cursor() as cursor:
            sql = """DELETE FROM medecin WHERE inami = %s"""
            cursor.execute(sql, (inami,))
            self.conn.commit()
    
    def del_pharmacien(self, inami):
        with self.conn.cursor() as cursor:
            sql = """DELETE FROM pharmacien WHERE inami = %s"""
            cursor.execute(sql, (inami,))
            self.conn.commit()
    ############################################################################
    
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
        inami_medecin = self.view.ask_inami_medecin()
        inami_pharmacien = self.view.ask_inami_pharmacien()
        succes = self.db.add_patient(niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
        if succes:
            self.view.patient_added({"NISS": niss, "nom": nom, "prenom": prenom, "genre": genre, "date_de_naissance": date_de_naissance, "mail": mail, "telephone": telephone, "inami_medecin": inami_medecin, "inami_pharmacien": inami_pharmacien})
        else :
            print("Un patient avec ce numéro NISS existe déjà.")
        self.view.main_menu()

    def add_medecin(self):
        inami = self.view.ask_inami()
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        specialite = self.view.ask_specialite()
        telephone = self.view.ask_telephone()
        success = self.db.add_medecin(inami, nom, mail, specialite, telephone)
        if success:
            self.view.medecin_added({"inami": inami, "nom": nom, "mail": mail, "specialite": specialite, "telephone": telephone})
        else:
            print("Un médecin avec ce numéro INAMI existe déjà.")
        self.view.main_menu()

            
    def add_pharmacien(self):
        inami = self.view.ask_inami()
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        telephone = self.view.ask_telephone()
        succes = self.db.add_pharmacien(inami, nom, mail, telephone)
        if succes:
            self.view.pharmacien_added({"inami": inami, "nom": nom, "mail": mail, "telephone": telephone})
        else:
            print("Un pharmacien avec ce numéro INAMI existe déjà.")
        self.view.main_menu()
    
    def login_patient(self):
        niss = self.view.ask_niss()
        date_de_naissance = self.view.ask_date_de_naissance()
        patient = self.db.get_patient(niss, date_de_naissance)
        if patient:
            self.view.patient_menu(patient)
        else:
            print("NISS ou date de naissance incorrects.")
            self.view.main_menu()

    def update_patient_medecin(self, niss):
        inami_medecin = self.view.ask_inami_medecin()
        self.db.update_patient_medecin(niss, inami_medecin)
        print("Médecin mis à jour avec succès.")
        self.view.main_menu()

    def update_patient_pharmacien(self, niss):
        inami_pharmacien = self.view.ask_inami_pharmacien()
        self.db.update_patient_pharmacien(niss, inami_pharmacien)
        print("Pharmacien mis à jour avec succès.")
        self.view.main_menu()

    
    ####################### A supprimer apres #######################
    def del_patient(self):
        niss = self.view.ask_niss()
        self.db.del_patient(niss)
        self.view.patient_deleted(niss)
        self.view.main_menu()
    
    def del_medecin(self):
        inami = self.view.ask_inami()
        self.db.del_medecin(inami)
        self.view.medecin_deleted(inami)
        self.view.main_menu()
    
    def del_pharmacien(self):
        inami = self.view.ask_inami()
        self.db.del_pharmacien(inami)
        self.view.pharmacien_deleted(inami)
        self.view.main_menu()
    #################################################################
# Vue
class View:
    
    def __init__(self, controller):
        self.controller = controller
    
    def main_menu(self):
        print("Bienvenue dans le gestionnaire de dossier médical")
        print("1. Ajouter un patient")
        print("2. Ajouter un médecin")
        print("3. Ajouter un pharmacien")
        print("4. Se connecter en tant que patient")
        print("5. Quitter")
        print("6. Supprimer")
        choice = input("Que voulez-vous faire ? ")
        if choice == "1":
            self.controller.add_patient()
        elif choice == "2":
            self.controller.add_medecin()
        elif choice == "3":
            self.controller.add_pharmacien()
        elif choice == "4":
            self.controller.login_patient()
        elif choice == "5":
            print("Au revoir !")
            exit()
        elif choice == "6":
            self.controller.del_medecin()  # mdofif ici pour sup un patient ou pharmacien
        else:
            print("Choix invalide")
            self.main_menu()

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
        if not re.match(r"^\d{11,15}$", inami):
            print("Le numéro INAMI doit être composé de 11 à 15 chiffres")
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


    def ask_inami_medecin(self):
        inami_medecin = input("Entrez le numéro INAMI du médecin : ")
        if not re.match(r"^\d{11,15}$", inami_medecin):
            print("Le numéro INAMI du médecin doit être composé de 11 à 15 chiffres")
            return self.ask_inami_medecin()
        return inami_medecin

    def ask_inami_pharmacien(self):
        inami_pharmacien = input("Entrez le numéro INAMI du pharmacien : ")
        if not re.match(r"^\d{11,15}$", inami_pharmacien):
            print("Le numéro INAMI du pharmacien doit être composé de 11 à 15 chiffres")
            return self.ask_inami_pharmacien()
        return inami_pharmacien

    def patient_added(self, data):
        self.print_summary("Patient", data)

    def medecin_added(self, data):
        self.print_summary("Médecin", data)

    def pharmacien_added(self, data):
        self.print_summary("Pharmacien", data)
    
    ########################### A supprimer #########################################
    def patient_deleted(self, niss):
        os.system('clear')
        print(f"\nPatient avec NISS {niss} supprimé(e) avec succès\n")
    
    def medecin_deleted(self, inami):
        os.system('clear')
        print(f"\nMédecin avec INAMI {inami} supprimé(e) avec succès\n")
    
    def pharmacien_deleted(self, inami):
        os.system('clear')
        print(f"\nPharmacien avec INAMI {inami} supprimé(e) avec succès\n")
    #################################################################################

    def print_summary(self, title, data):
        os.system('clear')
        print(f"\n{title} ajouté(e) avec succès :")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")
    
    def patient_menu(self, patient):
        print(f"\nBonjour {patient['prenom']} {patient['nom']}")
        print("\nMenu patient:")
        print("1. Modifier médecin de référence")
        print("2. Modifier pharmacien de référence")
        print("3. Consulter les informations médicales")
        print("4. Consulter les traitements")
        print("5. Retour")
        choice = input("Que voulez-vous faire ? ")
        if choice == "1":
            self.controller.update_patient_medecin(patient["NISS"])
        elif choice == "2":
            self.controller.update_patient_pharmacien(patient["NISS"])
        elif choice == "3":
            print("Consultation des informations médicales à implémenter.")
            self.patient_menu(patient)
        elif choice == "4":
            print("Consultation des traitements à implémenter.")
            self.patient_menu(patient)
        elif choice == "5":
            self.controller.view.main_menu()
        else:
            print("Choix invalide")
            self.patient_menu(patient)


        
        
if __name__ == "__main__":

    controller = Controller()
    view = View(controller)

    while True:
        view.main_menu()

