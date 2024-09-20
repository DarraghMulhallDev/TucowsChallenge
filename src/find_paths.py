import os
import psycopg2

def find_paths_func(start, end, cheapest:bool):
    conn = psycopg2.connect(
        dbname="database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )

    cur = conn.cursor()

    function = 'find_paths' if not cheapest else 'find_cheapest_path'
    # run create tables script
    cur.execute('SELECT * FROM {0}(1,{1}, {2});'.format(function, start, end))
    conn.commit()
    results = cur.fetchall()
    cur.close()
    return results
