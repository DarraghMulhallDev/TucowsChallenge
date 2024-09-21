import os
import psycopg2
import pytest

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(
        dbname="test_database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )
    conn.autocommit = True
    yield conn
    conn.close()

@pytest.fixture
def clean_database(db_connection):
    cur = db_connection.cursor()
    try:
        cur.execute("TRUNCATE TABLE edges CASCADE;")
        cur.execute("TRUNCATE TABLE nodes CASCADE;")
        cur.execute("TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    finally:
        cur.close()


# create data with simple cycles
@pytest.fixture
def create_data_simple_path(db_connection):
    db_connection.autocommit = True
    cur = db_connection.cursor()
    cur.execute("INSERT INTO graphs (id, name) VALUES ('g0', 'The Graph Name') ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO nodes (id, name, graph_id) VALUES ('a', 'Name_a', 1),('b', 'Name_b', 1),('c', 'Name_c', 1) ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO edges (graph_id, from_node_id, to_node_id, cost) VALUES(1, 'a', 'b', 1),(1, 'b', 'c', 1),(1, 'c', 'a', 1) ON CONFLICT (from_node_id, to_node_id) DO NOTHING;")
    cur.close()


# create data with no cycles
@pytest.fixture
def create_data_no_path(db_connection):
    db_connection.autocommit = True
    cur = db_connection.cursor()
    cur.execute("INSERT INTO graphs (id, name) VALUES ('g0', 'The Graph Name') ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO nodes (id, name, graph_id) VALUES ('a', 'Name_a', 1),('b', 'Name_b', 1),('c', 'Name_c', 1) ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO edges (graph_id, from_node_id, to_node_id, cost) VALUES(1, 'a', 'b', 1),(1, 'c', 'b', 1) ON CONFLICT (from_node_id, to_node_id) DO NOTHING;")
    cur.close()

# create data with several and complex cycles
@pytest.fixture
def create_data_complex_path(db_connection):
    cur = db_connection.cursor()
    cur.execute("INSERT INTO graphs (id, name) VALUES ('g0', 'The Graph Name') ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO nodes (id, name, graph_id) VALUES ('a', 'Name_a', 1),('b', 'Name_b', 1),('c', 'Name_c', 1), ('d', 'Name_d', 1),('e', 'Name_e', 1) ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO edges (graph_id, from_node_id, to_node_id, cost) VALUES (1, 'a', 'b', 5),(1, 'b', 'e', 3),(1, 'e', 'a', 1),(1, 'b', 'c', 1),(1, 'c', 'e', 1),(1, 'e', 'd', 1) ON CONFLICT (from_node_id, to_node_id) DO NOTHING;")
    cur.close()

def test_find_simple_path(db_connection, create_data_simple_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_paths(1, 'a', 'c');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 1

# expect no path
def test_find_no_path(db_connection, create_data_no_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_paths(1, 'a', 'c');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 0


# expect 12 cycles
def test_find_complex_paths(db_connection, create_data_complex_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_paths(1, 'a', 'e');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 2


def test_find_simple_cheapest_path(db_connection, create_data_simple_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_cheapest_path(1, 'a', 'c');")
    result = cur.fetchall()
    cur.execute("SELECT * FROM find_cheapest_path(1, 'a', 'c');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 1


def test_find_no_cheapest_path(db_connection, create_data_no_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_paths(1, 'a', 'c');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 0


# 2 options [(['a', 'b', 'c', 'e'], 3.0), (['a', 'b', 'e'], 4.0)] - expect the longer one due to lower cost
def test_find_complex_cheapest_path(db_connection, create_data_complex_path):
    os.environ['DB_NAME'] = os.getenv('TEST_DB_NAME')
    cur = db_connection.cursor()
    cur.execute("SELECT * FROM find_cheapest_path(1, 'a', 'e');")
    result = cur.fetchall()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    cur.close()
    assert len(result) == 1
    assert result == [(['a', 'b', 'c', 'e'],)]