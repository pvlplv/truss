from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


@dataclass
class Node:
    label: Optional[str]
    x: float
    y: float
    z: float


@dataclass
class ElementProperties:
    young_modulus: float
    poisso_ratio: float
    area: float


@dataclass
class Element:
    label: Optional[str]
    nodes: List[Node]
    properties: ElementProperties


@dataclass
class Problem:
    elements: List[Element]

    @classmethod
    def define_problem(
        cls,
        nl_path: Path,
        el_path: Path,
        properties: ElementProperties,
    ):
        """
        Метод задает задачу с узлами и элементами
        с предоставленными свойствами
        из листингов узлов и элементов.

        nl_path - путь к листингу узлов
        el_path - путь к листингу элементов
        properties - свойства элемента

        Листинг узлов должен быть текстовым файлом,
        где на одной строчке расположены, разделенные пробелом,
        номер узла, координата x, координата y, координата z.
        Например:
        0 0.00 0.00 0.00
        1 0.05 0.06 0.00
        2 0.10 0.00 0.00
        3 0.15 0.06 0.00
        4 0.20 0.00 0.00

        Листинг элементов должен быть текстовым файлом,
        где на одной строчке расположены, разделенные пробелом,
        номер элемента и номера принадлежащих элементу узлов.
        Например:
        0 0 1
        1 1 2
        2 0 2
        3 2 3
        4 3 4
        5 2 4
        6 1 3
        """
        with open(nl_path) as nl, open(el_path) as el:
            nl_data = [line.rstrip("\n").split(" ") for line in nl.readlines()]
            nodes = [
                Node(
                    label=line[0],
                    x=float(line[1]),
                    y=float(line[2]),
                    z=float(line[3]),
                )
                for line in nl_data
            ]
            el_data = [line.rstrip("\n").split(" ") for line in el.readlines()]
            elements = [
                Element(
                    label=line[0],
                    nodes=[
                        node
                        for node in nodes
                        if node.label in [node_label for node_label in line[0:]]
                    ],
                    properties=properties,
                )
                for line in el_data
            ]
            return cls(elements=elements)
