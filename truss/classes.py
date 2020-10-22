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
class Element:
    label: Optional[str]
    nodes: List[Node]


@dataclass
class Problem:
    elements: List[Element]

    @classmethod
    def define_problem(cls, nl_path: Path, el_path: Path):
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
                )
                for line in el_data
            ]
            return cls(elements=elements)
