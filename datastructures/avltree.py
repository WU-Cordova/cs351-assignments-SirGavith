from typing import Callable, Generic, Iterable, List
from datastructures.iavltree import IAVLTree, K, V
from __future__ import annotations


class Node(Generic[K,V]):
    Left: Node[K,V] = None
    Right: Node[K,V] = None
    Height = 0
    Key: K
    Value: V 
    def __init__(self, key: K, val: V) -> None:
        self.Key = key
        self.Value = val


class AVLTree(IAVLTree[K,V], Generic[K,V]):
    Root: Node[K,V] = None
    Count = 0
    
    def __init__(self, seq: Iterable[tuple[K,V]]) -> None:
        for k,v in seq or []: self.insert(k,v)

    def insert(self, key: K, val: V) -> None:
        if self.Root is None:
            self.Root = Node(key, val)
            return
        self.insert_helper(Node(key,val), self.Root)
        

    def insert_helper(self, newNode: Node[K,V], node: Node[K,V]):
        child = node.Left if newNode.Key < node.Key else node.Right
        if child is None:
            child = newNode
            return 
        else:
            self.insert_helper(newNode, child)
            node.Height = 1 + max(node.Left.Height or 0, node.Right.Height or 0)

            #TODO balance factor & rotations


    def search(self, key: K) -> V | None:
        raise NotImplementedError

    def delete(self, key: K) -> None:
        raise NotImplementedError

    def inorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        raise NotImplementedError

    def preorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        raise NotImplementedError

    def postorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        raise NotImplementedError

    def bforder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        raise NotImplementedError

    def size(self) -> int:
        return self.Count
