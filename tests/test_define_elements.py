from truss.classes import Problem


def test_define_elements():
    problem = Problem.define_problem("./tests/test_nl.txt", "./tests/test_el.txt")

    assert problem

    elements = problem.elements
    assert len(elements) == 7

    for element in elements:
        assert len(element.nodes) == 2
