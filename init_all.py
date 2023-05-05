import psycopg2
from controller import Controller

from fileLoader import insert_diagnostics, insert_medecins, insert_medicaments, insert_pathologies, insert_patients, insert_pharmaciens, insert_prescriptions, insert_specialites
from gestion_dossier_medical import Database
from view import View


def main():

    conn = psycopg2.connect(host='localhost', user='postgres',
                            password='azertyuiop', dbname='dossier_medical')

    file_path = 'data/pathologies.csv'
    insert_pathologies(conn, file_path)

    file_path = 'data/medicaments.csv'
    insert_medicaments(conn, file_path)

    file_path = 'data/patient.xml'
    node_name = 'patient'
    insert_patients(conn, file_path, node_name)

    file_path = 'data/medecins.xml'
    node_name = 'medecin'
    insert_medecins(conn, file_path, node_name)

    file_path = 'data/pharmaciens.xml'
    node_name = 'pharmacien'
    insert_pharmaciens(conn, file_path, node_name)

    file_path = 'data/specialites.xml'
    node_name = 'specialite'
    insert_specialites(conn, file_path, node_name)

    file_path = 'data/diagnostiques.xml'
    node_name = 'diagnostique'
    insert_diagnostics(conn, file_path, node_name)

    file_path = 'data/dossiers_patients.csv'
    insert_prescriptions(conn, file_path)

    conn.close()


if __name__ == "__main__":
    print("Insertion des données dans la base de données...")
    db = Database()
    db.clear_database()
    main()
    print("Insertion terminée.")
