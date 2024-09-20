
import src.find_paths as find_paths
import json

JSON_FILE = 'json/json_paths_result.json'


def query_paths(json_input=None):
    if json_input is None:
        json_input = input("Please insert json:")
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
    return {'answers':answers}
    

def write_json(json_result):
    with open (JSON_FILE, 'w') as file:
        json.dump(json_result, file)