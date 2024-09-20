
**Prerequisites**

- Docker is needed to be installed for hosting the database server
- Mac: https://docs.docker.com/desktop/install/mac-install/
- Windows: https://docs.docker.com/desktop/install/windows-install/

**Deploy Postgres in Docker**

Once Docker is installed do the following once inside the root of the repo
```
cd database
docker-compose up
```
This will deploy a Postgres server at port 5433

**Python Environment**
- Navigate back to the root of the repo
- Run the following to create a virtual environment
```
python -m venv venv
```
- Activate the virtual environment
```
(MAC) source venv/bin/activate
(Windows) venv\Scripts\activate
```
 - Please install any missing requirements
 ```
pip install -r requirements.txt
 ```

**Setup Databases**
Please run the script database/scripts/setup_db.py which will create the tables for the graph and insert some sample data to be used, in both the 'production' setting and also for a test database. It also defines the find_cycles and find_paths sql functions which are used in the python files and tests
```
python database/scripts/setup_db.py
```


**Coding Challenge**

The src/main.py is where most of the challenge-related code gets executed.

1. I download the text file using an xml file that I have stored on this repo as a demo of pulling something from the internet, however it does expire with tokens so the code will need to be updated to pull a valid version for the src/xml_parser.py file. E.g. https://raw.githubusercontent.com/DarraghMulhallDev/TucowsChallenge/refs/heads/trunk/xml/graph.xml. If the download fails it will just read from the same file locally. This is all done in the xml_parser.py file.

2. This code exists mainly under the parse_graph_xml function inside xml_parser as is accompanied by a number of helper functions
   I chose to ElementTree in python as it is very simple in it's approach and also has officia documentation on the pythin website to offer support

3. The schemas are housed in database/sql/create_tables.sql which is also used as a script for initializing data.
   I chose to make tables for graphs, nodes and edges. Even though nodes technically belong to a list nodes as per the the xml, I feel that it just done with xml to be clear and separate them from the edge nodes, but in a relational database sense it seemed unnecessary to add in the nodes list also.

   For the graph schema I chose to have a serial auto-increment id for efficiency-sake while also having the id/name from the xml as strings and not null constrained
   
   For the nodes, I chose to just use the string id as the primary key as this appears to be what's used for linking nodes with edges from the xml. I also added the graph_id which is a FK to the id in graphs table, to show the relationship that a node is linked to a specific graph

   For the edges, I choose a composite key of the from/to node ids as this will always be unique for any edge and didn't want to add extra columns for the sake of an offical numeric id. The graph_id, from_node_id and to_node_id obviously point to some graph or node respestively in the other tables for the ability to join on them and show their relationships

4. For the finding cycles functionality, I made a wrapper python function inside src/find_cycles.py which basically connects to the database and run the equivalent sql function
   I decided make this sql query as a permanent function so it could be used in testing as well - database/sql/find_cycles.sql

  ```
  CREATE OR REPLACE FUNCTION find_cycles(graph_id INT)
  RETURNS TABLE(path VARCHAR[]) AS $$
  BEGIN
      RETURN QUERY
      WITH RECURSIVE find_cycles(graph_id, from_node_id, to_node_id, is_cycle, edge_path) AS (
          SELECT
              e.graph_id,
              e.from_node_id,
              e.to_node_id,
              false,
              ARRAY[e.from_node_id]::VARCHAR[]
          FROM edges e
  
          UNION ALL
  
          SELECT
              e.graph_id,
              e.from_node_id,
              e.to_node_id,
              e.from_node_id = ANY(fc.edge_path),
              fc.edge_path || e.from_node_id
          FROM edges e, find_cycles fc
          WHERE e.to_node_id = fc.from_node_id AND NOT is_cycle
      )
      SELECT edge_path FROM find_cycles WHERE is_cycle;
  END;
  $$ LANGUAGE plpgsql;
```
The idea here is utilizing the recursive functionality that postgres possesses and using it to navigate through tree/graph-like structures.
The main thought process is to recursively iterate through the graph connecting the current from node to where that same node exists as a "to".
This allows us to navigate through the graph and maintain an array of the nodes we have visited, if we find something that already exists in the array then we have a found a cycle path.
The recursive stack should end by finding a cycle or where the current node has no linkages

5. I made a couple more sql functions for finding the paths and cheapest path, both inspired by similar logic from the finding cycles function
   These are housed in database/sql/find_paths.sql.
   The first function find_paths is very similar to the find_cycles function, but just that it can take a start and end node and use the start node as the initial anchor and then the end node as a constraint for ending the recursive stack call
   The cheapest_function, utilizes a total_cost variable which is down the recursive stack call where we keep adding nodes to a accumulating path array and obtain the final cost per path once no more recursive calls can go deeper.
   We look through the end result paths for those where the from node  = our end target node. We use ORDER BY cost and LIMIT 1 to ensure we get the lowest cost path from start to end

  **JSON**
  
  In src/json_paths.py I have code to handle inputs for the json to find either the paths or cheapest path of given targets, which utilizes both of the path sql functions described above
  This just loops through thr JSON and depending the key_type (paths/cheapest) we call one of the paths functions and get back one or more paths if they exist.
  Simple IF logic is put in place to deal with paths vs cheapest and the different return types of [] vs false
  I chose to have the json_paths.query_paths be able to take a string of json optionally to allow for easy tests instead of always doing stdin. If no string is passed the function will look at stdin

**Testing**

   I added substantial tests to all of the core functionality requested here. I utilized adding a separate test database to allow manipulation of the graph data for different test cases

   In the case of the xml parsing, I added a bunch of different xml files to represent different invalid datasets to cover all test cases
  
