from __future__ import annotations

from truss.truss import ElementProperties, Truss


def test_elements():
    properties = ElementProperties(
        young=2e11,
        poisson=0.25,
        area=0.1,
    )
    problem = Truss(
        "./tests/test_el.txt",
        "./tests/test_nl.txt",
        properties,
    )
    node = problem.get_node_by_label("0")

    elements = node.elements

    assert elements[0].label == "0"
    assert elements[1].label == "2"
