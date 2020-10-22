from truss.classes import Problem, Node, Element


def test_define_elements():
    problem = Problem.define_problem("./tests/test_nl.txt", "./tests/test_el.txt")

    problem_elements = problem.elements
    problem_elements_len = len(problem_elements)

    assert problem_elements_len == 7
    for element in problem_elements:
        assert len(element.nodes) == 2

    nodes = [
        Node(label="0", x=0.00, y=0.00, z=0.00),
        Node(label="1", x=0.05, y=0.06, z=0.00),
        Node(label="2", x=0.10, y=0.00, z=0.00),
        Node(label="3", x=0.15, y=0.06, z=0.00),
        Node(label="4", x=0.20, y=0.00, z=0.00),
    ]

    elements = [
        Element(label="0", nodes=[nodes[0], nodes[1]]),
        Element(label="1", nodes=[nodes[1], nodes[2]]),
        Element(label="2", nodes=[nodes[0], nodes[2]]),
        Element(label="3", nodes=[nodes[2], nodes[3]]),
        Element(label="4", nodes=[nodes[3], nodes[4]]),
        Element(label="5", nodes=[nodes[2], nodes[4]]),
        Element(label="6", nodes=[nodes[1], nodes[3]]),
    ]

    for i in range(problem_elements_len):
        problem_element = problem_elements[i]
        element = elements[i]
        assert problem_element.label == element.label
        for n in range(len(problem_element.nodes)):
            problem_element_node = problem_element.nodes[n]
            element_node = element.nodes[n]
            assert problem_element_node.label == element_node.label
            assert problem_element_node.x == element_node.x
            assert problem_element_node.y == element_node.y
            assert problem_element_node.z == element_node.z
