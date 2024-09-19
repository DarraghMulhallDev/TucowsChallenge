from src import xml_parser
import pytest
import xml.etree.ElementTree as Parser

# Fixture to parse XML data from a file and return the root element.
@pytest.fixture
def xml_data(request):
    file = request.param
    xml_tree = Parser.parse(file)
    graph_root = xml_tree.getroot()
    return graph_root


# Test case to verify that 'id' tag must be present in the XML file.
@pytest.mark.parametrize('xml_data', ['tests/xml/missing_id.xml'], indirect=True)
def test_validate_child_tag_exists(xml_data):
    with pytest.raises(ValueError, match="id tag must be present in graph tag"):
        xml_parser.validate_child_tag_exists(xml_data, 'id')


# Test case to ensure that all 'id' values within nodes are distinct.
@pytest.mark.parametrize('xml_data', ['tests/xml/duplicate_node_ids.xml'], indirect=True)
def test_validate_child_tags_distinct_ids(xml_data):
    nodes = xml_data.find('nodes')
    with pytest.raises(ValueError, match="All node tags must have a unique id value"):
        xml_parser.validate_child_tags_distinct(nodes, 'id')


# Test case to ensure that 'name' values within nodes are distinct. No error should be raised if names are unique.
@pytest.mark.parametrize('xml_data', ['tests/xml/duplicate_node_ids.xml'], indirect=True)
def test_validate_child_tags_distinct_names(xml_data):
    nodes = xml_data.find('nodes')
    xml_parser.validate_child_tags_distinct(nodes, 'name')


# Test case to ensure that only one 'from' tag exists in each edge node. An error should be raised if there are multiple 'from' tags.
@pytest.mark.parametrize('xml_data', ['tests/xml/multiple_froms.xml'], indirect=True)
def test_validate_singular_child_tag_from(xml_data):
    edges = xml_data.find('edges')
    node = edges[0]
    with pytest.raises(ValueError, match="Only 1 <from> tag must exist in each node edge"):
        xml_parser.validate_singular_child_tag(node, 'from')


# Test case to ensure that only one 'to' tag exists in each edge node. An error should be raised if there are multiple 'to' tags.
@pytest.mark.parametrize('xml_data', ['tests/xml/missing_to.xml'], indirect=True)
def test_validate_singular_child_tag_to(xml_data):
    edges = xml_data.find('edges')
    node = edges[0]
    with pytest.raises(ValueError, match="Only 1 <to> tag must exist in each node edge"):
        xml_parser.validate_singular_child_tag(node, 'to')


# Test case to ensure that missing 'cost' tags are added with a default value of 0.
@pytest.mark.parametrize('xml_data', ['tests/xml/missing_cost.xml'], indirect=True)
def test_parse_cost_tag(xml_data):
    edges = xml_data.find('edges')
    node = edges[1]
    not_orig_cost_exists = node.find('cost') is None
    xml_parser.parse_cost_tag(node)
    cost = node.find('cost')
    assert not_orig_cost_exists
    assert cost is not None
    assert cost.text == 0


# Test case to ensure that the XML file with multiple 'from' tags raises an error.
def test_parse_graph_xml_froms():
    with pytest.raises(ValueError, match="Only 1 <from> tag must exist in each node edge"):
        xml_parser.parse_graph_xml('tests/xml/multiple_froms.xml')


# Test case to ensure that an XML file missing the root 'graph' tag raises an error.
def test_parse_graph_xml_no_graph():
    with pytest.raises(ValueError, match="Xml root tag must be a graph"):
        xml_parser.parse_graph_xml('tests/xml/missing_graph.xml')


# Test case to ensure that an XML file with no 'node' tags inside the 'nodes' group raises an error.
def test_parse_graph_xml_no_nodes():
    with pytest.raises(ValueError, match="No <node> tags were found inside the <nodes> group"):
        xml_parser.parse_graph_xml('tests/xml/empty_node_list.xml')


# Test case to ensure that a valid XML file is parsed without errors.
def test_parse_graph_xml():
    xml_parser.parse_graph_xml('tests/xml/valid_sample.xml')
