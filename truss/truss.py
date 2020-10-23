from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from scipy.spatial.distance import pdist


@dataclass
class ElementProperties:
    young_modulus: float
    poisso_ratio: float
    area: float


@dataclass
class Element:
    problem: Truss
    label: str
    node_labels: Tuple[str, str]
    properties: ElementProperties

    @property
    def nodes(self) -> Tuple[Node, ...]:
        return tuple(map(self.problem.get_node_by_label, self.node_labels))

    @property
    def length(self) -> float:
        points = np.array([node.coordinates for node in self.nodes])
        return pdist(points)[0]

    @property
    def local_stiffness_matrix(self) -> np.ndarray:
        young_modulus = self.properties.young_modulus
        area = self.properties.area
        length = self.length
        return young_modulus * area / length * np.array([[-1, 1], [1, -1]])


@dataclass
class Node:
    problem: Truss
    label: str
    coordinates: np.ndarray
    element_labels: List[str]

    @property
    def elements(self) -> List[Element]:
        return list(map(self.problem.get_element_by_label, self.element_labels))


def get_line_data(f) -> List[List[str]]:
    return [line.rstrip("\n").split(" ") for line in f.readlines()]


class Truss:
    def __init__(
        self,
        elements_listing: Path,
        nodes_listing: Path,
        properties: ElementProperties,
    ):
        with open(elements_listing) as el, open(nodes_listing) as nl:
            elements_data = get_line_data(el)
            nodes_data = get_line_data(nl)
        elements = [
            Element(
                problem=self,
                label=data[0],
                node_labels=(data[1], data[2]),
                properties=properties,
            )
            for data in elements_data
        ]
        nodes = [
            Node(
                problem=self,
                label=data[0],
                coordinates=np.array(data[1:-1], dtype=float),
                element_labels=[
                    element.label
                    for element in elements
                    if data[0] in element.node_labels
                ],
            )
            for data in nodes_data
        ]
        self.elements = elements
        self.nodes = nodes

    def get_element_by_label(self, label: str) -> Element:
        return next(element for element in self.elements if element.label == label)

    def get_node_by_label(self, label: str) -> Node:
        return next(node for node in self.nodes if node.label == label)
