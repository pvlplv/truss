from __future__ import annotations

import numpy as np
from numpy.testing import assert_almost_equal, assert_array_almost_equal

from truss.truss import ElementProperties, Truss


def test_nodes():
    properties = ElementProperties(
        youngs_modulus=2e11,
        poissons_ratio=0.25,
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
        youngs_modulus=2e11,
        poissons_ratio=0.25,
        area=0.1,
    )
    problem = Truss(
        "./tests/test_el.txt",
        "./tests/test_nl.txt",
        properties,
    )
    element = problem.get_element_by_label("0")

    length = element.length
    expected_length = 0.078

    assert_almost_equal(length, expected_length, decimal=3)


def test_local_stiffness_matrix():
    properties = ElementProperties(
        youngs_modulus=2e11,
        poissons_ratio=0.25,
        area=0.1,
    )
    problem = Truss(
        "./tests/test_el.txt",
        "./tests/test_nl.txt",
        properties,
    )
    element = problem.get_element_by_label("0")

    local_stiffness_matrix = element.local_stiffness_matrix

    expected_local_stiffness_matrix = np.array(
        [
            [0.00000000e00, 0.00000000e00, 0.00000000e00, 0.00000000e00],
            [0.00000000e00, -4.19793049e09, 0.00000000e00, 4.19793049e09],
            [0.00000000e00, 0.00000000e00, 0.00000000e00, 0.00000000e00],
            [0.00000000e00, 4.19793049e09, 0.00000000e00, -4.19793049e09],
        ]
    )

    assert_array_almost_equal(
        local_stiffness_matrix, expected_local_stiffness_matrix, decimal=0
    )
