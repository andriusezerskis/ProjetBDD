"""
Projet de BDD : réaliser une base de données en SQL.
Date : 26/05/2023
Auteurs : Matias Nieto Navarrete, Andrius Ezerskis, Moïra Vanderslagmolen
Matricules : 502920, 542698, 547486
Section : B-INFO
"""

import psycopg2

def print_table_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    print(f"Résultats de la table {table_name}:")
    for row in rows:
        print(row)
    cursor.close()
    print()

def main():
    conn = psycopg2.connect(host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')

    print_table_data(conn, 'patient')
    print_table_data(conn, 'medecin')
    print_table_data(conn, 'pharmacien')
    print_table_data(conn, 'pathologie')
    print_table_data(conn, 'medicament')
    print_table_data(conn, 'diagnostique')
    print_table_data(conn, 'prescription')
    print_table_data(conn, 'specialite')
    
    conn.close()

if __name__ == "__main__":
    main()
