import xml.etree.ElementTree as ET
import psycopg2

# Lecture du fichier XML en tant que texte
with open('data/patient.xml', 'r') as file:
    xml_text = file.read()

# Ajout d'un élément racine temporaire pour englober tous les éléments "patient"
xml_text = f'<patients>{xml_text}</patients>'

# Création de l'arbre XML à partir de la chaîne de caractères
root = ET.fromstring(xml_text)

# Connexion à la base de données
conn = psycopg2.connect(host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')
cursor = conn.cursor()

# Importation des données
for patient in root.findall('patient'):
    niss = patient.find('NISS').text
    date_de_naissance = patient.find('date_de_naissance').text
    genre = int(patient.find('genre').text)
    inami_medecin = patient.find('inami_medecin').text
    inami_pharmacien = patient.find('inami_pharmacien').text
    mail = patient.find('mail').text
    nom = patient.find('nom').text
    prenom = patient.find('prenom').text
    telephone = patient.find('telephone').text

    sql = """INSERT INTO patient (NISS, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (niss, nom, prenom, genre, date_de_naissance, mail, telephone, inami_medecin, inami_pharmacien))

# Validation et fermeture de la connexion
conn.commit()
cursor.close()
conn.close()