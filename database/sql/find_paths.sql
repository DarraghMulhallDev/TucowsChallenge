-- function to return all cycles in a graph
CREATE OR REPLACE FUNCTION find_paths(graph_id INT, start_node VARCHAR, end_node VARCHAR)
RETURNS TABLE(path VARCHAR[]) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE recursive_paths(from_node_id, edge_path) AS (
        SELECT
            start_node,
            ARRAY[start_node]::VARCHAR[]
        
        UNION ALL

        SELECT
            e.to_node_id,
            rp.edge_path || e.to_node_id
        FROM edges e, recursive_paths rp 
        WHERE e.from_node_id = rp.from_node_id AND NOT e.to_node_id = ANY(rp.edge_path)
    )
    SELECT edge_path FROM recursive_paths WHERE from_node_id = end_node GROUP BY edge_path;
END;
$$ LANGUAGE plpgsql;

-- function to find cheapest path based off edge cost
CREATE OR REPLACE FUNCTION find_cheapest_path(graph_id INT, start_node VARCHAR, end_node VARCHAR)
RETURNS TABLE(path VARCHAR[]) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE recursive_paths(from_node_id, edge_path, total_cost) AS (
        SELECT
            start_node,
            ARRAY[start_node]::VARCHAR[],
            0.0::FLOAT
        
        UNION ALL

        SELECT
            e.to_node_id,
            rp.edge_path || e.to_node_id,
            rp.total_cost + e.cost
        FROM edges e, recursive_paths rp 
        WHERE e.from_node_id = rp.from_node_id AND NOT e.to_node_id = ANY(rp.edge_path)
    )
    SELECT edge_path FROM recursive_paths WHERE from_node_id = end_node ORDER BY total_cost LIMIT 1;
END;
$$ LANGUAGE plpgsql;





