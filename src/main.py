import xml_parser

def xml_challenge():
    xml_parser.download_file(xml_parser.XML_URL)
    parsed_xml = xml_parser.parse_graph_xml(xml_parser.GRAPH_FILE)
    return parsed_xml

parsed_xml = xml_challenge()