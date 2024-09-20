import psycopg2
import os


def setup_db():
    print("connecting to database")
    conn = psycopg2.connect(
        dbname="database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )

    cur = conn.cursor()

    # run create tables script
    sql = ''
    script_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(script_dir, '../sql/create_tables.sql')
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    conn.commit()
    # run table insertion script to initialize data
    sql_file_path = os.path.join(script_dir, '../sql/insert_data.sql')
    sql = ''
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    conn.commit()
    print("Database tables initialized")
    cur.close()

setup_db()