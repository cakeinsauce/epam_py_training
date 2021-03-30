"""
Given a dictionary (tree), that can contains multiple nested structures.
Write a function, that takes element and finds the number of occurrences
of this element in the tree.

Tree can only contains basic structures like:
    str, list, tuple, dict, set, int, bool
"""
from typing import Generator


def find_occurrences(tree: dict, element: any) -> int:
    """Return the element's number in the tree."""

    def find_occurrences_gen(node: any, elem: any) -> Generator:
        for v in (
            node.values() if isinstance(node, dict) else node
        ):  # Iter over dict or list values.
            if v == elem:  # Match
                yield v
            elif isinstance(v, (list, tuple, set)):  # Value is list, tuple or set.
                yield from find_occurrences_gen(v, elem)
            elif isinstance(v, dict):  # Value is a dict.
                yield from find_occurrences_gen(v.values(), elem)

    return len(list(find_occurrences_gen(tree, element)))
