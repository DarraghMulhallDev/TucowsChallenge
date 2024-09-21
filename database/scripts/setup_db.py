import os
import psycopg2
import database.db_connector as connector

def load_file(cur, file):
    sql = ''
    script_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(script_dir, '../sql/{}'.format(file))
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)

def setup_db():
    print("connecting to database")
    conn = connector.get_db_connection()
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
    conn = connector.get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute("CREATE DATABASE test_database;")
        print("Test database created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'test_database' already exists")
    cur.close()
    conn.close()

    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    conn = connector.get_db_connection()
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