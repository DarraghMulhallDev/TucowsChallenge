import xml.etree.ElementTree as XMLParser
import requests

# XML_URL = 'http://www.w3schools.com/xml/plant_catal.xml'
GRAPH_FILE = 'xml/graph.xml'

# read file from internet and write to local file
def download_file(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status() 
    # if error with request - return from function instead of writing to local file
    except requests.RequestException as ex: 
        print("Download Failed: {}", ex)
        return
    with open(GRAPH_FILE, 'wb') as file:
        file.write(response.content)


# check that any of the child tag exists in parent
def validate_child_tag_exists(parent, child_tag):
    if parent.findall(child_tag) is None:
            raise ValueError("{0} tag must be present in {1} tag".format(child_tag, parent.tag))


# validate child tag values inside tags of list are distinct
def validate_child_tags_value(parent_list, tag):
    values_set = set()
    for node in parent_list:
        child_tag = node.find(tag)
        val = child_tag.text
        if val in values_set:
            raise ValueError("All node tags must have a unique {} value".format(tag))
        values_set.add(val)
    del values_set


# check if 1 child tag only exists in parent
def validate_singular_child_tag(parent, child_tag):
    child_tags = parent.findall('from')
    if len(child_tags) > 1:
        raise ValueError('Only 1 {} tag must exist in each node edge', child_tag)


# validate and update any missing costs to default
def parse_cost_tag(edge_node):
    cost_tag = edge_node.find('cost')
    cost = cost_tag.text if cost_tag is not None else 0
    if cost_tag is None:
        cost_tag = XMLParser.Element('cost')
        cost_tag.text = 0
        edge_node.append(cost_tag)


# main function to parse/validate the given xml file
def parse_graph_xml(xml_file):
    try:
        # check if parse already returns an exception
        xml_tree = XMLParser.parse(GRAPH_FILE)
        graph_root = xml_tree.getroot()

        if graph_root.tag != 'graph':
            raise ValueError("Xml root tag must be a graph")
        
        validate_child_tag_exists(graph_root, 'id')
        validate_child_tag_exists(graph_root, 'name')

        nodes_tag = graph_root.find('nodes')
        nodes_list = nodes_tag.findall('node')
        # validate that there's at least 1 node inside nodes tag
        if len(nodes_list) == 0:
            raise ValueError("No <node> tags were found inside the <nodes> group")
        
        # make sure all ids are distinct within nodes
        validate_child_tags_value(nodes_list, 'id')

        # validate node edges
        edges_tag = graph_root.find('edges')
        node_edges = edges_tag.findall('node')
        for node in node_edges:
            # validate 1 occurrence of tags are found in node
            validate_singular_child_tag(node, 'from')
            validate_singular_child_tag(node, 'to')
            # validate and update any missing costs to default
            parse_cost_tag(node)
        return graph_root

    except Exception as ex:
        print(ex)
