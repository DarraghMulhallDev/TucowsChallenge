import psycopg2
import os

def load_file(cur, file):
    sql = ''
    script_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(script_dir, '../sql/{}'.format(file))
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)

def setup_db():
    print("connecting to database")
    conn = psycopg2.connect(
        dbname="database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )
    conn.autocommit = True
    cur = conn.cursor()

    # run create tables script
    load_file(cur, 'create_tables.sql')
    # run table insertion script to initialize data
    load_file(cur, 'insert_data.sql')
    print("Database tables initialized")

    # load find functions
    load_file(cur, 'find_cycles.sql')
    load_file(cur, 'find_paths.sql')
    cur.close()


def setup_test_db():
    conn = psycopg2.connect(
        dbname="database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute("CREATE DATABASE test_database;")
        print("Test database created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'test_database' already exists")
    cur.close()
    conn.close()


    conn = psycopg2.connect(
        dbname="test_database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )
    conn.autocommit = True
    cur = conn.cursor()

    # run create tables script
    load_file(cur, 'create_tables.sql')
    print("Test database tables initialized")
    # load find functions
    load_file(cur, 'find_cycles.sql')
    load_file(cur, 'find_paths.sql')

    cur.close()
    conn.close()

setup_db()
setup_test_db()