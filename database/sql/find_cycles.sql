-- function to return all cycles in a graph

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