
import find_paths
import json

def query_paths():
    json_input = '{"queries": [{"paths": {"start": "a","end": "e" }},{"cheapest": {"start": "a","end": "e" }}, {"cheapest": {"start": "a","end": "h" }}]}'
    json_data = json.loads(json_input)

    queries = json_data.get('queries', [])

    answers = []
    for query in queries:
        key_type = 'paths' if 'paths' in query else 'cheapest'
        start = '\''+query[key_type]['start']+'\''
        end = '\''+query[key_type]['end']+'\''
        cheapest = key_type == 'cheapest'
        result_path_type = 'paths' if key_type == 'paths' else 'path'
        search_result = find_paths.find_paths_func(start, end, cheapest)
        if len(search_result) == 0 and key_type == 'cheapest':
            search_result = False
        answers.append({key_type:{'from':start, 'to':end, result_path_type:search_result}})
    return json.dumps({'answers':answers})