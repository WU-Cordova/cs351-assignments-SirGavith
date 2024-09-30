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

    def recalc_height(self):
        self.Height = 1 + max(self.Left.Height or 0, self.Right.Height or 0)


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
        self.Count += 1
        

    def insert_helper(self, newNode: Node[K,V], node: Node[K,V]) -> Node[K,V]:

        child = node.Left if newNode.Key < node.Key else node.Right
        if child is None:
            child = newNode
            return newNode
        else:
            self.insert_helper(newNode, child)
            node.Height = 1 + max(node.Left.Height or 0, node.Right.Height or 0)

            #TODO balance factor & rotations


    def balance_tree(self, node: Node[K,V]) -> Node[K,V]:
        if node.bf > 1 and node.Left.bf >= 0:               #LL
            return self.rotate_right(node)
        elif node.bf < -1 and node.Right.bf <= 0:           #RR
            return self.rotate_left(node)
        elif node.bf > 1 and node.Left.bf <= -1:            #LR
            node.Left = self.rotate_left(node.Left)
            return self.rotate_right(node)
        elif node.bf < -1 and node.Right.bf >= 1:           #RL
            node.Right = self.rotate_right(node.Right)
            return self.rotate_left(node)

    def rotate_right(self, node: Node[K,V]) -> Node[K,V]:
        root = node.Left
        subtree = root.Right
        root.Right = node
        node.Left = subtree
        node.recalc_height()
        root.recalc_height()
        return root

    def rotate_left(self, node: Node[K,V]) -> Node[K,V]:
        root = node.Right
        subtree = root.Left
        root.Left = node
        node.Right = subtree
        node.recalc_height()
        root.recalc_height()
        return root

    def search(self, key: K) -> V | None:
        raise NotImplementedError

    def delete(self, key: K) -> None:

        self.Count -= 1
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
