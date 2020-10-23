from __future__ import annotations

import numpy as np
from numpy.testing import assert_array_equal

from truss.truss import ElementProperties, Truss


def test_problem_init():
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

    elements = problem.elements
    nodes = problem.nodes

    for element in elements:
        assert element.problem == problem
        assert element.properties == properties

    assert elements[0].label == "0"
    assert elements[1].label == "1"
    assert elements[2].label == "2"
    assert elements[3].label == "3"
    assert elements[4].label == "4"
    assert elements[5].label == "5"
    assert elements[6].label == "6"

    assert elements[0].node_labels == ("0", "1")
    assert elements[1].node_labels == ("1", "2")
    assert elements[2].node_labels == ("0", "2")
    assert elements[3].node_labels == ("2", "3")
    assert elements[4].node_labels == ("3", "4")
    assert elements[5].node_labels == ("2", "4")
    assert elements[6].node_labels == ("1", "3")

    for node in nodes:
        assert node.problem == problem

    assert nodes[0].label == "0"
    assert nodes[1].label == "1"
    assert nodes[2].label == "2"
    assert nodes[3].label == "3"
    assert nodes[4].label == "4"

    assert_array_equal(nodes[0].coordinates, np.array([0.00, 0.00]))
    assert_array_equal(nodes[1].coordinates, np.array([0.05, 0.06]))
    assert_array_equal(nodes[2].coordinates, np.array([0.10, 0.00]))
    assert_array_equal(nodes[3].coordinates, np.array([0.15, 0.06]))
    assert_array_equal(nodes[4].coordinates, np.array([0.20, 0.00]))

    assert nodes[0].element_labels == ["0", "2"]
    assert nodes[1].element_labels == ["0", "1", "6"]
    assert nodes[2].element_labels == ["1", "2", "3", "5"]
    assert nodes[3].element_labels == ["3", "4", "6"]
    assert nodes[4].element_labels == ["4", "5"]


def test_get_element_by_label():
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

    element = problem.get_element_by_label("0")

    assert element.label == "0"
    assert element.node_labels == ("0", "1")


def test_get_node_by_label():
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

    assert node.label == "0"
    assert_array_equal(node.coordinates, np.array([0.00, 0.00]))
    assert node.element_labels == ["0", "2"]
