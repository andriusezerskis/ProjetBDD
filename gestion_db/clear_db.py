"""
Projet de BDD : réaliser une base de données en SQL.
Date : 26/05/2023
Auteurs : Matias Nieto Navarrete, Andrius Ezerskis, Moïra Vanderslagmolen
Matricules : 502920, 542698, 547486
Section : B-INFO
"""

import psycopg2

def clear_database():
    conn = psycopg2.connect(host='localhost', user='postgres',
                            password='azertyuiop', dbname='dossier_medical')
    
    tables = ['patient', 'medecin', 'pharmacien', 'pathologie',
                'medicament', 'diagnostique', 'prescription', 'specialite']
    with conn.cursor() as cursor:
        for table_name in tables:
            cursor.execute(f'TRUNCATE {table_name} CASCADE')
        conn.commit()

if __name__ == '__main__':
    print('Nettoyage de la base de données...')
    clear_database()
    print('Base de données nettoyée.')
