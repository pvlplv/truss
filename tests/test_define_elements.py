from truss.classes import Problem, Node, Element, ElementProperties


def test_define_elements():
    properties = ElementProperties(
        young_modulus=2e11,
        poisso_ratio=0.25,
        area=0.1,
    )
    problem = Problem.define_problem(
        "./tests/test_nl.txt",
        "./tests/test_el.txt",
        properties,
    )
    nodes = [
        Node(label="0", x=0.00, y=0.00, z=0.00),
        Node(label="1", x=0.05, y=0.06, z=0.00),
        Node(label="2", x=0.10, y=0.00, z=0.00),
        Node(label="3", x=0.15, y=0.06, z=0.00),
        Node(label="4", x=0.20, y=0.00, z=0.00),
    ]
    elements = [
        Element(label="0", nodes=[nodes[0], nodes[1]], properties=properties),
        Element(label="1", nodes=[nodes[1], nodes[2]], properties=properties),
        Element(label="2", nodes=[nodes[0], nodes[2]], properties=properties),
        Element(label="3", nodes=[nodes[2], nodes[3]], properties=properties),
        Element(label="4", nodes=[nodes[3], nodes[4]], properties=properties),
        Element(label="5", nodes=[nodes[2], nodes[4]], properties=properties),
        Element(label="6", nodes=[nodes[1], nodes[3]], properties=properties),
    ]
    problem_elements = problem.elements
    for i in range(len(problem_elements)):
        problem_element = problem_elements[i]
        problem_element_properties = problem_element.properties
        element = elements[i]
        assert problem_element.label == element.label
        assert problem_element_properties.young_modulus == properties.young_modulus
        assert problem_element_properties.poisso_ratio == properties.poisso_ratio
        assert problem_element_properties.area == properties.area
        assert len(element.nodes) == 2
        for n in range(len(problem_element.nodes)):
            problem_element_node = problem_element.nodes[n]
            element_node = element.nodes[n]
            assert problem_element_node.label == element_node.label
            assert problem_element_node.x == element_node.x
            assert problem_element_node.y == element_node.y
            assert problem_element_node.z == element_node.z
