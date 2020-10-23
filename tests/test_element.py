from __future__ import annotations

from numpy.testing import assert_approx_equal

from truss.truss import ElementProperties, Truss


def test_nodes():
    properties = ElementProperties(
        young_modulus=2e11,
        poisso_ratio=0.25,
        area=0.1,
    )
    problem = Truss(
        "./tests/test_el.txt",
        "./tests/test_nl.txt",
        properties,
    )
    element = problem.get_element_by_label("0")

    nodes = element.nodes

    assert nodes[0].label == "0"
    assert nodes[1].label == "1"


def test_length():
    properties = ElementProperties(
        young_modulus=2e11,
        poisso_ratio=0.25,
        area=0.1,
    )
    problem = Truss(
        "./tests/test_el.txt",
        "./tests/test_nl.txt",
        properties,
    )
    element = problem.get_element_by_label("0")

    length = element.length

    upper = 0.079
    lower = 0.077

    assert length < upper
    assert length > lower

    assert_approx_equal(length, 0.078, significant=2)


# def test_local_stiffness_matrix():
#     properties = ElementProperties(young_modulus=2e11, poisso_ratio=0.25, area=0.1,)
#     problem = Truss("./tests/test_el.txt", "./tests/test_nl.txt", properties,)
#     element = problem.get_element_by_label("0")

#     local_stiffness_matrix = element.local_stiffness_matrix

#     pass
