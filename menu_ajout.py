import psycopg2

def add_patient(conn, niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien):
    with conn.cursor() as cursor:
        sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien))
        conn.commit()

def add_medecin(conn, inami, nom, mail, specialite, telephone):
    with conn.cursor() as cursor:
        sql = """INSERT INTO medecin (inami, nom, mail, specialite, telephone)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (inami, nom, mail, specialite, telephone))
        conn.commit()

def add_pharmacien(conn, inami, nom, mail, telephone):
    with conn.cursor() as cursor:
        sql = """INSERT INTO pharmacien (inami, nom, mail, telephone)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (inami, nom, mail, telephone))
        conn.commit()

def get_patient_info():
    niss = input("Entrez le NISS: ")
    nom = input("Entrez le nom: ")
    prenom = input("Entrez le prénom: ")
    genre = input("Entrez le genre (1 pour homme, 2 pour femme): ")
    date_de_naissance = input("Entrez la date de naissance (YYYY-MM-DD): ")
    mail = input("Entrez l'adresse e-mail: ")
    telephone = input("Entrez le numéro de téléphone: ")
    inami_medecin = input("Entrez le numéro INAMI du médecin: ")
    inami_pharmacien = input("Entrez le numéro INAMI du pharmacien: ")

    return (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)

def get_medecin_info():
    inami = input("Entrez le numéro INAMI: ")
    nom = input("Entrez le nom: ")
    mail = input("Entrez l'adresse e-mail: ")
    specialite = input("Entrez la spécialité: ")
    telephone = input("Entrez le numéro de téléphone: ")

    return (inami, nom, mail, specialite, telephone)

def get_pharmacien_info():
    inami = input("Entrez le numéro INAMI: ")
    nom = input("Entrez le nom: ")
    mail = input("Entrez l'adresse e-mail: ")
    telephone = input("Entrez le numéro de téléphone: ")

    return (inami, nom, mail, telephone)

def supp_patient(conn, niss):
    cursor = conn.cursor()

    query = "DELETE FROM patient WHERE niss = %s;"
    cursor.execute(query, (niss,))

    conn.commit()
    cursor.close()

    print("Patient avec NISS", niss, "supprimé avec succès.")

    
    
    
    
def main():
    conn = psycopg2.connect(host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')

    while True:
        print("\n1. Ajouter un patient")
        print("2. Ajouter un médecin")
        print("3. Ajouter un pharmacien")
        print("4. Supprimer un patient")
        print("5. Quitter")
        choice = input("Choisissez une option: ")

        if choice == '1':
            patient_info = get_patient_info()
            add_patient(conn, *patient_info)
            print("Patient ajouté avec succès.")
        elif choice == '2':
            medecin_info = get_medecin_info()
            add_medecin(conn, *medecin_info)
            print("Médecin ajouté avec succès.")
        elif choice == '3':
            pharmacien_info = get_pharmacien_info()
            add_pharmacien(conn, *pharmacien_info)
            print("Pharmacien ajouté avec succès.")
        elif choice == '4':
            niss = input("Entrez le NISS du patient à supprimer: ")
            supp_patient(conn, niss)
        elif choice == '5':
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
