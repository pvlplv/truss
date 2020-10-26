from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from scipy.spatial.distance import pdist


@dataclass
class ElementProperties:
    youngs_modulus: float
    poissons_ratio: float
    area: float


@dataclass
class Element:
    problem: Truss
    label: str
    node_labels: List[str]
    properties: ElementProperties

    @property
    def nodes(self) -> List[Node]:
        labels = self.node_labels
        return [self.problem.get_node_by_label(label) for label in labels]

    @property
    def length(self) -> float:
        points = np.array([node.coordinates for node in self.nodes])
        return pdist(points)[0]

    @property
    def local_stiffness_matrix(self) -> np.ndarray:
        youngs_modulus = self.properties.youngs_modulus
        area = self.properties.area
        length = self.length
        matrix = np.array(
            [
                [-1, 1],
                [1, -1],
            ]
        )
        klocal = matrix * youngs_modulus * area / length
        x2 = self.nodes[0].coordinates[1]
        x1 = self.nodes[0].coordinates[0]
        y2 = self.nodes[1].coordinates[1]
        y1 = self.nodes[1].coordinates[0]
        l12 = (x2 - x1) / length
        m12 = (y2 - y1) / length
        T = np.array(
            [
                [
                    l12,
                    m12,
                    0,
                    0,
                ],
                [0, 0, l12, m12],
            ]
        )
        return T.transpose() @ klocal @ T


@dataclass
class Node:
    problem: Truss
    label: str
    coordinates: np.ndarray
    element_labels: List[str]

    @property
    def elements(self) -> List[Element]:
        labels = self.element_labels
        return [self.problem.get_element_by_label(label) for label in labels]


def get_listing_data(path: Path) -> List[List[str]]:
    with open(path) as listing:
        lines = listing.readlines()
    return [line.rstrip("\n").split(" ") for line in lines]


class Truss:
    def __init__(
        self,
        elements_listing: Path,
        nodes_listing: Path,
        properties: ElementProperties,
    ):
        self.elements = self.create_elements_from_listing(
            elements_listing,
            properties,
        )
        self.nodes = self.create_nodes_from_listing(nodes_listing, self.elements)

    def create_elements_from_listing(
        self,
        elements_listing: Path,
        properties: ElementProperties,
    ) -> List[Element]:
        elements_data = get_listing_data(elements_listing)
        return [
            self.create_element(element_data, properties)
            for element_data in elements_data
        ]

    def create_element(
        self,
        element_data: List[str],
        properties: ElementProperties,
    ) -> Element:
        return Element(
            problem=self,
            label=element_data[0],
            node_labels=element_data[1:3],
            properties=properties,
        )

    def create_nodes_from_listing(
        self,
        nodes_listing: Path,
        elements: List[Element],
    ) -> List[Node]:
        nodes_data = get_listing_data(nodes_listing)
        return [self.create_node(node_data, elements) for node_data in nodes_data]

    def create_node(
        self,
        node_data: List[str],
        elements: List[Element],
    ) -> Node:
        return Node(
            problem=self,
            label=node_data[0],
            coordinates=np.array(node_data[1:3], dtype=float),
            element_labels=self.get_element_labels_for_node(node_data[0], elements),
        )

    def get_element_labels_for_node(
        self,
        node_label: str,
        elements: List[Element],
    ) -> List[str]:
        return [
            element.label for element in elements if node_label in element.node_labels
        ]

    def get_element_by_label(self, label: str) -> Element:
        return next(element for element in self.elements if element.label == label)

    def get_node_by_label(self, label: str) -> Node:
        return next(node for node in self.nodes if node.label == label)
