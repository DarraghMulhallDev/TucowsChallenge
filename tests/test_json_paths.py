import psycopg2
import os
import pytest
from src import json_paths

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(
        dbname="test_database",
        user="user",
        password="password",
        host="localhost",  # or your host
        port="5433"        # default PostgreSQL port
    )
    yield conn
    conn.close()


# create data with several and complex cycles
@pytest.fixture
def create_data_complex_path(db_connection):
    db_connection.autocommit = True
    cur = db_connection.cursor()
    cur.execute("INSERT INTO graphs (id, name) VALUES ('g0', 'The Graph Name') ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO nodes (id, name, graph_id) VALUES ('a', 'Name_a', 1),('b', 'Name_b', 1),('c', 'Name_c', 1), ('d', 'Name_d', 1),('e', 'Name_e', 1) ON CONFLICT (id) DO NOTHING;")
    cur.execute("INSERT INTO edges (graph_id, from_node_id, to_node_id, cost) VALUES (1, 'a', 'b', 1),(1, 'b', 'e', 3),(1, 'e', 'a', 1),(1, 'b', 'c', 1),(1, 'c', 'e', 1),(1, 'e', 'd', 1) ON CONFLICT (from_node_id, to_node_id) DO NOTHING;")


# test query_paths with complex example
def test_find_path(db_connection, create_data_complex_path):
    answers = json_paths.query_paths('{"queries": [{"paths": {"start": "a","end": "e" }},{"cheapest": {"start": "a","end": "e" }}, {"cheapest": {"start": "a","end": "h" }}]}')
    assert len(answers['answers'][0]['paths']['paths']) == 2

# test cheapest path with complex example where longer but cheaper path is selected
def test_find_path(db_connection, create_data_complex_path):
    answers = json_paths.query_paths('{"queries": [{"cheapest": {"start": "a","end": "e" }},{"cheapest": {"start": "a","end": "e" }}, {"cheapest": {"start": "a","end": "h" }}]}')
    cheapest = answers['answers'][0]['cheapest']['path']
    assert len(cheapest) == 1
    assert cheapest == [(['a', 'b', 'c', 'e'],)]

# test finding cheapest but no paths found
def test_find_cheapest_none(db_connection, create_data_complex_path):
    answers = json_paths.query_paths('{"queries": [{"cheapest": {"start": "d","end": "a" }},{"cheapest": {"start": "a","end": "e" }}, {"cheapest": {"start": "a","end": "h" }}]}')
    cheapest = answers['answers'][0]['cheapest']['path']
    assert cheapest == False

# test finding paths but no paths found
def test_find_paths_none(db_connection, create_data_complex_path):
    answers = json_paths.query_paths('{"queries": [{"paths": {"start": "d","end": "a" }},{"cheapest": {"start": "a","end": "e" }}, {"cheapest": {"start": "a","end": "h" }}]}')
    db_connection.autocommit = True
    cur = db_connection.cursor()
    cur.execute("TRUNCATE TABLE edges CASCADE;TRUNCATE TABLE nodes CASCADE;TRUNCATE TABLE graphs RESTART IDENTITY CASCADE;")
    assert len(answers['answers'][0]['paths']['paths']) == 0