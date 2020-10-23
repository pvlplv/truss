from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from scipy.spatial.distance import pdist


@dataclass
class ElementProperties:
    """
    Свойства элемента

    Аргументы
    ---------
    young :
        модуль Юнга [Па]
    poisson :
        коэффициент Пуассона
    area :
        площадь сечение [м2]
    """

    young: float
    poisson: float
    area: float


@dataclass
class Element:
    """
    Стержневой элемент

    Аргументы
    ---------
    problem :
        задача, в которой участвует элемент
    label :
        номер элемента
    node_labels :
        номера узлов, принадлежащих элементу
    properies :
        свойства элемента
    """

    problem: Truss
    label: str
    node_labels: Tuple[str, str]
    properties: ElementProperties

    @property
    def nodes(self) -> Tuple[Node, ...]:
        """Объекты узлов, принадлежащих элементу"""
        labels = self.node_labels
        return tuple(self.problem.get_node_by_label(label) for label in labels)

    @property
    def length(self) -> float:
        """Длинна элемента"""
        points = np.array([node.coordinates for node in self.nodes])
        return pdist(points)[0]

    @property
    def local_stiffness_matrix(self) -> np.ndarray:
        """Локальная матрица жесткости"""
        young = self.properties.young
        area = self.properties.area
        length = self.length
        matrix = np.array(
            [
                [-1, 1],
                [1, -1],
            ]
        )
        return matrix * young * area / length


@dataclass
class Node:
    """
    Узел

    Аргументы
    ---------
    problem :
        задача, в которой участвует узел
    label :
        номер узла
    element_labels :
        номера элементов, которым принадлежащит узел
    """

    problem: Truss
    label: str
    coordinates: np.ndarray
    element_labels: List[str]

    @property
    def elements(self) -> List[Element]:
        """Объекты элементов, которым принадлежащит узел"""
        labels = self.element_labels
        return [self.problem.get_element_by_label(label) for label in labels]


class Truss:
    """
    Задача расчета фермы
    """

    def __init__(
        self,
        elements_listing: Path,
        nodes_listing: Path,
        properties: ElementProperties,
    ):
        """
        Задача отпределяется листингами элементов и узлов,
        а так же свойствами элемента

        Аргументы
        ---------
        elements_listing :
            путь к листингу элементов
        nodes_listing :
            путь к листингу узлов
        properties :
            свойства элементов

        Листинг элементов должен быть текстовым файлом,
        где на одной строчке расположены, разделенные пробелом,
        номер элемента и номера принадлежащих элементу узлов, например:
        0 0 1
        1 1 2
        2 0 2
        3 2 3
        4 3 4
        5 2 4
        6 1 3

        Листинг узлов должен быть текстовым файлом,
        где на одной строчке расположены, разделенные пробелом,
        номер узла, координата x, координата y, например:
        0 0.00 0.00
        1 0.05 0.06
        2 0.10 0.00
        3 0.15 0.06
        4 0.20 0.00
        """

        def get_listing_data(path: Path) -> List[List[str]]:
            """Парсинг листингов элементов и узлов"""
            with open(path) as listing:
                lines = listing.readlines()
            return [line.rstrip("\n").split(" ") for line in lines]

        elements_data = get_listing_data(elements_listing)
        nodes_data = get_listing_data(nodes_listing)
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
                coordinates=np.array(data[1:3], dtype=float),
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
        """Возвращает объект элемента, принадлежащего задаче, по его номеру"""
        return next(element for element in self.elements if element.label == label)

    def get_node_by_label(self, label: str) -> Node:
        """Возвращает объект узла, принадлежащего задаче, по его номеру"""
        return next(node for node in self.nodes if node.label == label)
