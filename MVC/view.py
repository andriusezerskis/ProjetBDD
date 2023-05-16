import re
import os
from tabulate import tabulate

class AskingView:

    def ask_niss(self):
        niss = input("Entrez le NISS du patient : ")
        if not niss:
            self.clean()
            print("Le NISS ne peut pas être vide")
            return None
        if not re.match(r"^\d{10,15}$", niss):
            print("Le NISS doit être composé de 10 à 15 chiffres")
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
        date_de_naissance = input(
            "Entrez la date de naissance du patient (format YYYY-MM-DD) : ")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_de_naissance):
            print("La date de naissance doit être au format YYYY-MM-DD")
            return self.ask_date_de_naissance()
        return date_de_naissance

    def ask_inami(self, profession):
        inami = input(f"Entrez le numéro INAMI du {profession} : ")
        if not inami:
            self.clean()
            print("Le numéro INAMI ne peut pas être vide")
            return None
        if not re.match(r"^\d{9,15}$", inami):
            print("Le numéro INAMI doit être composé de 9 à 15 chiffres")
            return self.ask_inami(profession)
        return inami

    def ask_specialite(self):
        specialite = input("Entrez la spécialité : ")
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", specialite):
            print("La spécialité ne peut contenir que des lettres et des espaces")
            return self.ask_specialite()
        return specialite

    def ask_telephone(self):
        telephone = input(
            "Entrez le numéro de téléphone (appuyez sur Entrée pour laisser vide) : ")
        if not telephone:
            return telephone
        elif not re.match(r"^\+?\d{10,15}$", telephone):
            print("Le numéro de téléphone doit être composé de 10 à 15 chiffres")
            return self.ask_telephone()
        return telephone

    def ask_mail(self):
        mail = input(
            "Entrez l'adresse e-mail (appuyez sur Entrée pour laisser vide) : ")
        if not mail:
            return mail
        elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", mail):
            print("L'adresse e-mail doit être valide")
            return self.ask_mail()
        return mail

    def ask_requete(self):
        for i in range(1, 11):
            if i < 10:
                print(f"{i}.  Requête {i}")
            else:
                print(f"{i}. Requête {i}")
        print("11. Retour au menu principal")
        
        while True:
            requete_str = input("\nQuelle requête voulez-vous exécuter ? ")
            
            if requete_str.strip() == "":
                print("Choix invalide")
            else:
                try:
                    requete = int(requete_str)
                    if requete < 1 or requete > 11:
                        print("Choix invalide")
                    else:
                        return requete
                except ValueError:
                    print("Choix invalide")



    def ask_date_specifique(self):
        date = input("Entrez la date (format MM/DD/YYYY) : ")
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", date):
            print("La date doit être au format MM/DD/YYYY")
            return self.ask_date_specifique()
        return date
    
    def ask_nom_medicament(self):
        nom_med = input("Entrez le nom du médicament : ")
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nom_med):
            print("Le nom du médicament ne peut contenir que des lettres")
            return self.ask_nom_medicament()
        return nom_med
        

class MainView(AskingView):

    def __init__(self, controller):
        self.controller = controller
        
    def print_title(self, title):
        print("\n                  " + "=" * len(title))
        print("                  "+title)
        print("                  " + "=" * len(title) + "\n")

    def main_menu(self):
        try:
            self.print_title("Gestionnaire de dossier médical")
            print("1. Se connecter en tant que patient")
            print("2. Executer les requêtes")
            print("3. Ajouter un patient")
            print("4. Ajouter un médecin")
            print("5. Ajouter un pharmacien")
            print("6. Quitter\n")
            choice = input("Que voulez-vous faire ? ")
            if choice == "1":
                self.clean()
                self.print_title("Connexion patient")
                self.controller.login_patient()
                self.clean()
            elif choice == "2":
                self.clean()
                self.print_title("Exécution des requêtes")
                self.controller.execute_requete()
                self.clean()
            elif choice == "3":
                self.clean()
                self.print_title("Ajout d'un patient")
                self.controller.add_patient()
            elif choice == "4":
                self.clean()
                self.print_title("Ajout d'un médecin")
                self.controller.add_medecin()
            elif choice == "5":
                self.clean()
                self.print_title("Ajout d'un pharmacien")
                self.controller.add_pharmacien()
            elif choice == "6":
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
            self.print_title("Menu patient")
            print("1. Modifier médecin de référence")
            print("2. Modifier pharmacien de référence")
            print("3. Consulter les informations médicales")
            print("4. Consulter les traitements")
            print("5. Consulter les coordonnées du médecin et du pharmacien")
            print("6. Retour")
            choice = input("Que voulez-vous faire ? ")
            if choice == "1":
                self.controller.update_patient_medecin(patient)
            elif choice == "2":
                self.controller.update_patient_pharmacien(patient)
            elif choice == "3":
                self.controller.medical_info(patient)
            elif choice == "4":
                self.controller.traitements(patient)
            elif choice == "5":
                self.controller.contact(patient)
            elif choice == "6":
                self.clean()
                self.controller.view.main_menu()
            else:
                print("Choix invalide")
                self.patient_menu(patient)
        except KeyboardInterrupt:
            print("\n")
            exit()

    def display_error(self, error_message):
        self.clean()
        print("Erreur : " + error_message)

    def display_success(self, success_message):
        self.clean()
        print(success_message)

    def print_summary(self, title, action, data):
        self.clean()
        print(f"{title} {action} avec succès")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")

    def display_medical_info(self, medical_info):
        self.clean()
        print("\nInformations médicales :")
        headers = ["Date du diagnostic", "Nom de la pathologie"]
        print(tabulate(medical_info, headers=headers, tablefmt='fancy_grid',colalign=("center", "center")))

    def display_traitements(self, traitement):
        self.clean()
        print("\nTraitements:")
        headers = ["Date d'achat", "Nom du médicament", "Durée du traitement (en jours)"]
        print(tabulate(traitement, headers=headers, tablefmt='fancy_grid', colalign=("center", "center", "center")))

    def display_contact(self, contact):
        contact_list = list(contact)
        for i in range (len(contact_list)):
            if contact_list[i] == None:
                contact_list[i] = "Non renseigné"
        contact_medecin = [tuple(contact_list[0:3])]
        contact_pharmacien = [tuple(contact_list[3:6])]
       
        self.clean()
        print("\nContact:")
        headers = ["Nom Medecin", "E-mail", "Téléphone"]
        print(tabulate(contact_medecin, headers=headers, tablefmt='fancy_grid',colalign=("center", "center", "center")))
        
        headers = ["Nom Pharmacien", "E-mail", "Téléphone"]
        print(tabulate(contact_pharmacien, headers=headers, tablefmt='fancy_grid', colalign=("center", "center", "center")))

    def display_requete(self,filename):
        self.clean()
        os.system(f"cd requete && ./execute_requete.sh {filename}")
        os.system("cd ..")
    
    def clean(self):
        os.system('clear')




