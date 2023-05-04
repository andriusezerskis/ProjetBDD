import re
import os

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
        date_de_naissance = input(
            "Entrez la date de naissance du patient (format YYYY-MM-DD : ")
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
