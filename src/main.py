import xml_parser
import json_paths

def xml_challenge():
    xml_parser.download_file(xml_parser.XML_URL)
    parsed_xml = xml_parser.parse_graph_xml(xml_parser.GRAPH_FILE)
    return parsed_xml


def run_json_path_finder():
    return json_paths.query_paths()


parsed_xml = xml_challenge()


print(run_json_path_finder())