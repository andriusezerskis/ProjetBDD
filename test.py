import psycopg2

# Connexion à la base de données
conn = psycopg2.connect(host='localhost', user='postgres', password='azertyuiop', dbname='dossier_medical')
cursor = conn.cursor()

# Exécution de la requête SELECT
cursor.execute('SELECT * FROM patient')

# Récupération de toutes les lignes
rows = cursor.fetchall()

# Impression des résultats
for row in rows:
    print(row)

# Fermeture de la connexion
cursor.close()
conn.close()
