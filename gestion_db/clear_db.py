
import psycopg2

def clear_database():
    conn = psycopg2.connect(
            host='192.168.1.10', 
            user='postgres', 
            password='azertyuiop', 
            dbname='dossier_medical')
    
    tables = ['patient', 'medecin', 'pharmacien', 'pathologie',
                'medicament', 'diagnostique', 'prescription', 'specialite']
    with conn.cursor() as cursor:
        for table_name in tables:
            cursor.execute(f'TRUNCATE {table_name} CASCADE')
        conn.commit()

if __name__ == '__main__':
    clear_database()