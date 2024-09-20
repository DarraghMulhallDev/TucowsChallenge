INSERT INTO graphs (id, name) VALUES
    ('g0', 'The Graph Name')
    ON CONFLICT (id) DO NOTHING
;


INSERT INTO nodes (id, name, graph_id) VALUES
    ('a', 'Name_a', 1),
    ('b', 'Name_b', 1),
    ('c', 'Name_c', 1),
    ('d', 'Name_d', 1),
    ('e', 'Name_e', 1)
    ON CONFLICT (id) DO NOTHING
;


INSERT INTO edges (graph_id, from_node_id, to_node_id, cost) VALUES
    (1, 'a', 'b', 1),
    (1, 'b', 'e', 1),                                       
    (1, 'e', 'a', 1),                                     
    (1, 'b', 'c', 1),
    (1, 'c', 'e', 1),
    (1, 'e', 'd', 1)
    ON CONFLICT (from_node_id, to_node_id) DO NOTHING
;