import database.db_connector as connector

def find_paths_func(start, end, cheapest:bool):
    conn = connector.get_db_connection()
    cur = conn.cursor()
    function = 'find_paths' if not cheapest else 'find_cheapest_path'
    # run create tables script
    cur.execute('SELECT * FROM {0}(1,{1},{2});'.format(function, start, end))
    conn.commit()
    results = cur.fetchall()
    cur.close()
    return results
