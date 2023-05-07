import xml.etree.ElementTree as ET
import csv


def open_file(conn, file_path, node_name):
    with open(file_path, 'r') as file:
        xml_text = file.read()

    xml_text = f'<{node_name}>{xml_text}</{node_name}>'
    root = ET.fromstring(xml_text)

    cursor = conn.cursor()
    return root, cursor

def get_pathologie_id(conn, pathologie_nom):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM pathologie WHERE nom = %s", (pathologie_nom,)
        )
        result = cur.fetchone()
        return result[0] if result else None

def insert_patients(conn,file_path, node_name):
    
    root, cursor = open_file(conn, file_path, node_name)

    for patient in root.findall('patient'):
        niss = get_text(patient.find('NISS'))
        date_de_naissance = get_text(patient.find('date_de_naissance'))
        genre = int(get_text(patient.find('genre')))
        inami_medecin = get_text(patient.find('inami_medecin'))
        inami_pharmacien = get_text(patient.find('inami_pharmacien'))
        mail = get_text(patient.find('mail'))
        nom = get_text(patient.find('nom'))
        prenom = get_text(patient.find('prenom'))
        telephone = get_text(patient.find('telephone'))

        sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                 VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), %s, %s, %s, %s)"""
        cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien))

    conn.commit()
    cursor.close()

def insert_medecins(conn,file_path, node_name):
    
    root, cursor = open_file(conn, file_path, node_name)
    
    for medecin in root.findall('medecin'):
        inami = get_text(medecin.find('inami'))
        mail = get_text(medecin.find('mail'))
        nom = get_text(medecin.find('nom'))
        specialite = get_text(medecin.find('specialite'))
        telephone = get_text(medecin.find('telephone'))
        

        sql = """INSERT INTO medecin (inami, nom, mail, specialite, telephone)
                VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (inami, nom, mail, specialite, telephone))

    conn.commit()
    cursor.close()
    
def insert_pharmaciens(conn,file_path, node_name):
    
    root, cursor = open_file(conn, file_path, node_name)
    
    for pharmacien in root.findall('pharmacien'):
        inami = get_text(pharmacien.find('inami'))
        mail = get_text(pharmacien.find('mail'))
        nom = get_text(pharmacien.find('nom'))
        telephone = get_text(pharmacien.find('telephone'))
        

        sql = """INSERT INTO pharmacien (inami, nom, mail, telephone)
                VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (inami, nom, mail, telephone))

    conn.commit()
    cursor.close()

def insert_specialites(conn, file_path, node_name):
    root, cursor = open_file(conn, file_path, node_name)

    for specialite in root.findall('specialite'):
        name = get_text(specialite.find('name'))
        medicaments = specialite.findall('medicament')  # Pas besoin d'utiliser get_text ici
        medicament_systeme_anatomique = ''
        for medicament in medicaments:
            medicament_systeme_anatomique += get_text(medicament) + ';'  # Utilisez get_text pour lire le texte de chaque élément medicament
        # Supprime le dernier ';'
        medicament_systeme_anatomique = medicament_systeme_anatomique[:-1]

        query = "INSERT INTO specialite (name, medicament_systeme_anatomique) VALUES (%s, %s);"
        cursor.execute(query, (name, medicament_systeme_anatomique))

    conn.commit()
    cursor.close()

def insert_diagnostics(conn,file_path, node_name):
    
    root, cursor = open_file(conn, file_path, node_name)
    
    for diagnostique in root.findall('diagnostique'):
        NISS_patient = get_text(diagnostique.find('NISS'))
        date_diagnostic = get_text(diagnostique.find('date_diagnostic'))
        pathologie_nom = get_text(diagnostique.find('pathology'))

        pathologie_id = get_pathologie_id(conn, pathologie_nom)
        if pathologie_id is not None:
            sql = """INSERT INTO diagnostic (NISS_patient, date_diagnostic, pathologie_id)
                    VALUES (%s, TO_DATE(%s, 'MM/DD/YYYY'), %s)"""
            cursor.execute(sql, (NISS_patient, date_diagnostic, pathologie_id))
            
        else:
            print(f"Pathologie '{pathologie_nom}' non trouvée.")
    
    conn.commit()
    cursor.close()

def insert_prescriptions(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header line

        for row in reader:
            NISS_patient, medecin, inami_medecin, pharmacien, inami_pharmacien, medicament_nom_commercial, DCI, date_prescription, date_vente, duree_traitement = row
            insert_prescription(conn, NISS_patient, inami_medecin, inami_pharmacien, medicament_nom_commercial, date_prescription, date_vente, duree_traitement)

def insert_prescription(conn, NISS_patient, inami_medecin, inami_pharmacien, medicament_nom_commercial, date_prescription, date_vente, duree_traitement):
    with conn.cursor() as cur:
        # Get medicament_id from medicament_nom_commercial
        cur.execute("SELECT id FROM medicament WHERE nom_commercial = %s", (medicament_nom_commercial,))
        medicament_id = cur.fetchone()
        if medicament_id:
            medicament_id = medicament_id[0]
        else:
            print(f"Medicament '{medicament_nom_commercial}' not found.")
            return

        cur.execute(
            "INSERT INTO prescription (NISS_patient, inami_medecin, inami_pharmacien, medicament_id, date_prescription, date_vente, duree_traitement) VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), TO_DATE(%s, 'MM/DD/YYYY'), %s)",
            (NISS_patient, inami_medecin, inami_pharmacien, medicament_id, date_prescription, date_vente, duree_traitement)
        )
        conn.commit()

def insert_pathologies(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nom, systeme_anatomique = row
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pathologie (nom, systeme_anatomique) VALUES (%s, %s)",
                    (nom, systeme_anatomique)
                )
                conn.commit()

def insert_medicaments(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header line
        for row in reader:
            dci, nom_commercial, systeme_anatomique, conditionnement = row
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO medicament (dci, nom_commercial, systeme_anatomique, conditionnement) VALUES (%s, %s, %s, %s)",
                    (dci, nom_commercial, systeme_anatomique, conditionnement)
                )
                conn.commit()

def get_text(element):
    if element is not None and element.text is not None and element.text.strip() != '':
        return element.text.strip()
    else:
        return None

