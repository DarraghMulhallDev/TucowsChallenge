import os
import psycopg2

def find_cycles():
    conn = psycopg2.connect(
        dbname="database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )

    cur = conn.cursor()

    # run create tables script
    cur.execute('SELECT * FROM find_cycles(1);')
    conn.commit()
    results = cur.fetchall()
    cur.close()
    return results

print(find_cycles())