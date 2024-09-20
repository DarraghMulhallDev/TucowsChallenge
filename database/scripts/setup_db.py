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
    conn.autocommit = True
    cur = conn.cursor()

    # run create tables script
    sql = ''
    script_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(script_dir, '../sql/create_tables.sql')
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    # run table insertion script to initialize data
    sql_file_path = os.path.join(script_dir, '../sql/insert_data.sql')
    sql = ''
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    print("Database tables initialized")

    # load find_cycles function
    sql_file_path = os.path.join(script_dir, '../sql/find_cycles.sql')
    sql = ''
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    cur.close()


def setup_test_db():
    conn = psycopg2.connect(
        dbname="test_database",
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
    # run create tables script
    sql = ''
    script_dir = os.path.dirname(__file__)
    sql_file_path = os.path.join(script_dir, '../sql/create_tables.sql')
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)
    print("Test database tables initialized")
    # load find_cycles function
    sql_file_path = os.path.join(script_dir, '../sql/find_cycles.sql')
    sql = ''
    with open(sql_file_path, 'r') as file:
        sql = file.read()
    cur.execute(sql)

    cur.close()

setup_db()
setup_test_db()