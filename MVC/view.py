import re
import os
from tabulate import tabulate

class AskingView:

    def ask_niss(self):
        niss = input("Entrez le NISS du patient : ")
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
        os.system('clear')
        print("Exécution des requêtes\n")
        print(" 1. Requête 1")
        print(" 2. Requête 2")
        print(" 3. Requête 3")
        print(" 4. Requête 4")
        print(" 5. Requête 5")
        print(" 6. Requête 6")
        print(" 7. Requête 7")
        print(" 8. Requête 8")
        print(" 9. Requête 9")
        print("10. Requête 10")
        requete = int(input("Quelle requête voulez-vous exécuter ? "))
        if requete < 1 or requete > 10:
            print("Choix invalide")
            return self.ask_requete()
        return requete

    def ask_date_specifique(self):
        date = input("Entrez la date (format MM/DD/YYYY) : ")
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", date):
            print("La date doit être au format MM/DD/YYYY")
            return self.ask_date_specifique()
        return date

        

class MainView(AskingView):

    def __init__(self, controller):
        self.controller = controller

    def main_menu(self):
        try:
            print("Bienvenue dans le gestionnaire de dossier médical\n")
            print("1. Ajouter un patient")
            print("2. Ajouter un médecin")
            print("3. Ajouter un pharmacien")
            print("4. Se connecter en tant que patient")
            print("5. Executer les requêtes")
            print("6. Quitter")
            choice = input("Que voulez-vous faire ? ")
            if choice == "1":
                self.controller.add_patient()
            elif choice == "2":
                self.controller.add_medecin()
            elif choice == "3":
                self.controller.add_pharmacien()
            elif choice == "4":
                self.controller.login_patient()
                os.system('clear')
            elif choice == "5":
                self.controller.execute_requete()
                os.system('clear')
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
            print("Menu patient:")
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
                os.system('clear')
                self.controller.view.main_menu()
            else:
                print("Choix invalide")
                self.patient_menu(patient)
        except KeyboardInterrupt:
            print("\n")
            exit()

    def display_error(self, error_message):
        os.system('clear')
        print(error_message)

    def display_success(self, success_message):
        os.system('clear')
        print(success_message)

    def print_summary(self, title, action, data):
        os.system('clear')
        print(f"\n{title} {action} avec succès :")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")

    def display_medical_info(self, medical_info):
        os.system('clear')
        print("\nInformations médicales :")
        headers = ["Date du diagnostic", "Nom de la pathologie"]
        print(tabulate(medical_info, headers=headers, tablefmt='fancy_grid',colalign=("center", "center")))

    def display_traitements(self, traitement):
        os.system('clear')
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
       
        os.system('clear')
        print("\nContact:")
        headers = ["Nom Medecin", "E-mail", "Téléphone"]
        print(tabulate(contact_medecin, headers=headers, tablefmt='fancy_grid',colalign=("center", "center", "center")))
        
        headers = ["Nom Pharmacien", "E-mail", "Téléphone"]
        print(tabulate(contact_pharmacien, headers=headers, tablefmt='fancy_grid', colalign=("center", "center", "center")))

    def display_requete(self,filename):
        os.system('clear')
        os.system(f"cd requete && ./execute_requete.sh {filename}")
        os.system("cd ..")
