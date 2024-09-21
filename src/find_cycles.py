import os
import database.db_connector as connector

def find_cycles():
    conn = connector.get_db_connection()
    cur = conn.cursor()
    # run create tables script
    cur.execute('SELECT * FROM find_cycles(1);')
    conn.commit()
    results = cur.fetchall()
    cur.close()
    return results

print(find_cycles())