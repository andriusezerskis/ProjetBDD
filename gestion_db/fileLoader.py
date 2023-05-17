import xml.etree.ElementTree as ET
import csv
from io import StringIO


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
            "SELECT id_pathologie FROM pathologie WHERE nom = %s", (pathologie_nom,)
        )
        result = cur.fetchone()
        return result[0] if result else None
    

def get_specialite_id(conn, specialite_nom):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id_specialite FROM specialite WHERE nom = %s", (specialite_nom,)
        )
        result = cur.fetchone()
        return result[0] if result else None

def insert_patients(conn, file_path):
    with open(file_path, 'r') as f:
        content = '<root>' + f.read() + '</root>'
        root = ET.parse(StringIO(content)).getroot()

        cur = conn.cursor()
        for child in root:
            if child.tag == 'NISS':
                NISS = child.text
            elif child.tag == 'nom':
                nom = child.text
            elif child.tag == 'prenom':
                prenom = child.text
            elif child.tag == 'genre':
                genre = int(child.text)
            elif child.tag == 'date_de_naissance':
                date_de_naissance = child.text
            elif child.tag == 'mail':
                mail = child.text
            elif child.tag == 'telephone':
                telephone = child.text
            elif child.tag == 'inami_medecin':
                inami_medecin = child.text
            elif child.tag == 'inami_pharmacien':
                inami_pharmacien = child.text
                
            if child.tag == 'telephone': 
                cur.execute(
                    "INSERT INTO patient VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
                )
        conn.commit()
        cur.close()
        

def insert_medecins(conn,file_path, node_name):
    
    root, cursor = open_file(conn, file_path, node_name)
    
    for medecin in root.findall('medecin'):
        inami = get_text(medecin.find('inami'))
        mail = get_text(medecin.find('mail'))
        nom = get_text(medecin.find('nom'))
        specialite_id = get_specialite_id(conn, get_text(medecin.find('specialite')))
        telephone = get_text(medecin.find('telephone'))
        

        sql = """INSERT INTO medecin (inami, nom, mail, id_specialite, telephone)
                VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (inami, nom, mail, specialite_id, telephone))

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
        query = "INSERT INTO specialite (nom) VALUES (%s) ON CONFLICT(nom) DO NOTHING;"
        cursor.execute(query, (name,))
        
        medicaments = specialite.findall('medicament')  # Pas besoin d'utiliser get_text ici
        for medicament in medicaments:
            query = "INSERT INTO systeme_anatomique (nom) VALUES (%s) ON CONFLICT(nom) DO NOTHING;"
            cursor.execute(query, (get_text(medicament),))
            query = "INSERT INTO specialite_systeme_anatomique (id_specialite, id_systeme_anatomique) SELECT s.id_specialite, sa.id_systeme_anatomique FROM specialite s, systeme_anatomique sa where s.nom=%s and sa.nom=%s"
            cursor.execute(query, (name, get_text(medicament)))



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
            sql = """INSERT INTO diagnostique (NISS_patient, date_diagnostic, id_pathologie)
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
        cur.execute("SELECT id_medicament FROM medicament WHERE nom_commercial = %s", (medicament_nom_commercial,))
        medicament_id = cur.fetchone()
        if medicament_id:
            medicament_id = medicament_id[0]
        else:
            print(f"Medicament '{medicament_nom_commercial}' not found.")
            return

        cur.execute(
            "INSERT INTO prescription (NISS_patient, inami_medecin, inami_pharmacien, id_medicament, date_prescription, date_vente, duree_traitement) VALUES (%s, %s, %s, %s, TO_DATE(%s, 'MM/DD/YYYY'), TO_DATE(%s, 'MM/DD/YYYY'), %s)",
            (NISS_patient, inami_medecin, inami_pharmacien, medicament_id, date_prescription, date_vente, duree_traitement)
        )
        conn.commit()


def insert_pathologies(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        with conn.cursor() as cur:
            for row in reader:
                nom, specialite = row
                cur.execute(
                    "INSERT INTO specialite (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING",
                    (specialite,)
                )
                cur.execute(
                    "INSERT INTO pathologie (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING", (nom,)
                )
                cur.execute("INSERT INTO pathologie_specialite (id_pathologie, id_specialite) SELECT p.id_pathologie, s.id_specialite from pathologie p, specialite s where p.nom=%s and s.nom=%s ON CONFLICT (id_pathologie, id_specialite) DO NOTHING",
                            (nom, specialite)
                            )

        conn.commit()

def insert_medicaments(conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header line
        with conn.cursor() as cur:
            for row in reader:
                dci, nom_commercial, systeme_anatomique, conditionnement = row
                cur.execute(
                    "INSERT INTO systeme_anatomique (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING",
                    (systeme_anatomique,)
                )
                cur.execute(
                    """
                    INSERT INTO medicament (dci, id_systeme_anatomique, nom_commercial, conditionnement) 
                    SELECT %s, id_systeme_anatomique, %s, %s 
                    FROM systeme_anatomique 
                    WHERE nom = %s
                    ON CONFLICT (dci, nom_commercial, conditionnement) DO NOTHING
                    """, 
                    (dci, nom_commercial, conditionnement, systeme_anatomique)
                )
        conn.commit()


def get_text(element):
    if element is not None and element.text is not None and element.text.strip() != '':
        return element.text.strip()
    else:
        return None

