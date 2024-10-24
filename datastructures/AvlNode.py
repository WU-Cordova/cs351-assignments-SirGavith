from __future__ import annotations
from typing import Generic
from datastructures.iavltree import IAVLTree, K, V


class AVLNode(Generic[K,V]):
    Left: AVLNode[K,V] = None
    Right: AVLNode[K,V] = None
    Height = 1
    bf = 0
    Key: K
    Value: V 
    def __init__(self, key: K, val: V) -> None:
        self.Key = key
        self.Value = val

    def recalc_height(self):
        lHeight = 0 if not self.Left else self.Left.Height
        rHeight = 0 if not self.Right else self.Right.Height

        self.Height = 1 + max(lHeight, rHeight)
        self.bf = lHeight - rHeight

    def __repr__(self) -> str:
        return f"Node[{self.Key}]"