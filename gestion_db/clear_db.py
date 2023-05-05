
import psycopg2

def clear_database():
    conn = psycopg2.connect(
            host='localhost', 
            user='postgres', 
            password='azertyuiop', 
            dbname='dossier_medical')
    
    tables = ['patient', 'medecin', 'pharmacien', 'pathologie',
                'medicament', 'diagnostic', 'prescription', 'specialite']
    with conn.cursor() as cursor:
        for table_name in tables:
            cursor.execute(f'TRUNCATE {table_name} CASCADE')
        conn.commit()

if __name__ == '__main__':
    clear_database()