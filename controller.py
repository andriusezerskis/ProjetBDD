from model import Database
from view import MainView


class Controller:
    def __init__(self):
        self.db = Database()
        self.view = MainView(self)
        self.view.main_menu()

    def add_patient(self):
        niss = self.view.ask_niss()
        nom = self.view.ask_nom()
        prenom = self.view.ask_prenom()
        genre = self.view.ask_genre()
        date_de_naissance = self.view.ask_date_de_naissance()
        mail = self.view.ask_mail()
        telephone = self.view.ask_telephone()
        inami_medecin = self.view.ask_inami("médecin")
        inami_pharmacien = self.view.ask_inami("pharmacien")
        succes = self.db.add_patient(
            niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
        if succes:
            data = {"NISS": niss, "nom": nom, "prenom": prenom, "genre": genre,
                    "date_de_naissance": date_de_naissance, "mail": mail, "telephone": telephone,
                    "inami_medecin": inami_medecin, "inami_pharmacien": inami_pharmacien}
            self.view.print_summary("Patient", "ajouté(e)", data)
        else:
            self.view.display_error(
                "Un patient avec ce numéro NISS existe déjà.")
        self.view.main_menu()

    def add_medecin(self):
        inami = self.view.ask_inami("médecin")
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        specialite = self.view.ask_specialite()
        telephone = self.view.ask_telephone()
        success = self.db.add_medecin(inami, nom, mail, specialite, telephone)
        if success:
            data = {"inami": inami, "nom": nom, "mail": mail,
                    "specialite": specialite, "telephone": telephone}
            self.view.print_summary("Médecin", "ajouté(e)", data)
        else:
            self.view.display_error(
                "Un médecin avec ce numéro INAMI existe déjà.")
        self.view.main_menu()

    def add_pharmacien(self):
        inami = self.view.ask_inami("pharmacien")
        nom = self.view.ask_nom()
        mail = self.view.ask_mail()
        telephone = self.view.ask_telephone()
        succes = self.db.add_pharmacien(inami, nom, mail, telephone)
        if succes:
            data = {"inami": inami, "nom": nom,
                    "mail": mail, "telephone": telephone}
            self.view.print_summary("Pharmacien", "ajouté(e)", data)
        else:
            self.view.display_error(
                "Un pharmacien avec ce numéro INAMI existe déjà.")
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
        inami_medecin = self.view.ask_inami("medecin")
        self.db.update_patient_medecin(patient['NISS'], inami_medecin)
        self.view.display_success("Médecin mis à jour avec succès.")
        patient['inami_medecin'] = inami_medecin
        self.view.print_summary("Patient", "mis(e) à jour", patient)
        self.view.patient_menu(patient)

    def update_patient_pharmacien(self, patient):
        inami_pharmacien = self.view.ask_inami("pharmacien")
        self.db.update_patient_pharmacien(patient['NISS'], inami_pharmacien)
        self.view.display_success("Pharmacien mis à jour avec succès.")
        patient['inami_pharmacien'] = inami_pharmacien
        self.view.print_summary("Patient", "mis(e) à jour", patient)
        self.view.patient_menu(patient)

    def view_medical_info(self, patient):
        medical_info = self.db.get_medical_info(patient["NISS"])
        if medical_info:
            self.view.display_medical_info(medical_info)
        else:
            self.view.display_error("Aucune information médicale trouvée.")
        self.view.patient_menu(patient)