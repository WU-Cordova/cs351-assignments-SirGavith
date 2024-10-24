from __future__ import annotations
from typing import Callable, Generic, Iterable, List, Optional
from datastructures.iavltree import IAVLTree, K, V
from datastructures.AvlNode import AVLNode

class AVLTree(IAVLTree[K,V], Generic[K,V]):
    Root: AVLNode[K,V] = None
    Count = 0
    
    def __init__(self, seq: Iterable[tuple[K,V]] = None) -> None:
        for k,v in seq or []: self.insert(k,v)

    def insert(self, key: K, val: V = None, on_recalc = lambda node: ()) -> None:
        self.Root = self.insert_helper(AVLNode(key,val), self.Root, on_recalc)
        self.Count += 1
        
    def insert_helper(self, newNode: AVLNode[K,V], node: AVLNode[K,V], on_recalc) -> AVLNode[K,V]:
        if node is None:
            return newNode

        if newNode.Key < node.Key:
            node.Left = self.insert_helper(newNode, node.Left, on_recalc)
        else:
            node.Right = self.insert_helper(newNode, node.Right, on_recalc)
        
        node.recalc_height()
        new_node = self.balance_tree(node, on_recalc) if node.bf > 1 or node.bf < -1 else node
        on_recalc(new_node)
        return new_node

    def delete(self, key: K, on_recalc = lambda node: ()) -> None:
        self.Root = self.delete_helper(self.Root, key, on_recalc)
        self.Count -= 1
    
    def delete_helper(self, node: AVLNode[K,V], key: K, on_recalc) -> AVLNode[K,V]:
        if node is None:
            raise KeyError(f"Key {key} not found in tree")
        
        if key == node.Key:
            if node.Left is None or node.Right is None:
                #deleting single parent or leaf
                return node.Left or node.Right
            #deleting double-parent
            successor = node.Right
            while successor.Left is not None:
                successor = successor.Left

            node.Key = successor.Key
            node.Value = successor.Value
            node.Right = self.delete_helper(node.Right, successor.Key, on_recalc)

        elif (key < node.Key):
            node.Left = self.delete_helper(node.Left, key, on_recalc)
        else:
            node.Right = self.delete_helper(node.Right, key, on_recalc)

        node.recalc_height()
        new_node = self.balance_tree(node, on_recalc) if node.bf > 1 or node.bf < -1 else node
        on_recalc(new_node)
        return new_node
    
    def balance_tree(self, node: AVLNode[K,V], on_recalc) -> AVLNode[K,V]:
        if node.bf > 1 and node.Left.bf >= 0:               #LL
            return self.rotate_right(node, on_recalc)
        elif node.bf < -1 and node.Right.bf <= 0:           #RR
            return self.rotate_left(node, on_recalc)
        elif node.bf > 1 and node.Left.bf <= -1:            #LR
            node.Left = self.rotate_left(node.Left, on_recalc)
            return self.rotate_right(node, on_recalc)
        elif node.bf < -1 and node.Right.bf >= 1:           #RL
            node.Right = self.rotate_right(node.Right, on_recalc)
            return self.rotate_left(node, on_recalc)

    def rotate_right(self, node: AVLNode[K,V], on_recalc) -> AVLNode[K,V]:
        root = node.Left
        subtree = root.Right
        root.Right = node
        node.Left = subtree
        node.recalc_height()
        root.recalc_height()
        on_recalc(node)
        return root

    def rotate_left(self, node: AVLNode[K,V], on_recalc) -> AVLNode[K,V]:
        root = node.Right
        subtree = root.Left
        root.Left = node
        node.Right = subtree
        node.recalc_height()
        root.recalc_height()
        on_recalc(node)
        return root
    
    def search(self, key: K) -> V | None:
        return node.Value if (node:= self.get_node(key)) is not None else None
    
    def get_node(self, key: K) -> V | None:
        if self.Root is None: return None
        def recurse(node: AVLNode[K,V]) -> V:
            return node if node.Key == key else \
                recurse(child) if \
                (child := node.Left if key < node.Key else node.Right) is not None \
                    else None
        return recurse(self.Root)

    def inorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: AVLNode[K,V]) -> list[K]:
            if node.Left: recurse(l, node.Left)
            if visit: visit(node.Value)
            l.append(node.Value)
            if node.Right: recurse(l, node.Right)
            return l
        return recurse([], self.Root)
    
    def preorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: AVLNode[K,V]) -> list[K]:
            if visit: visit(node.Value)
            l.append(node.Value)
            if node.Left: recurse(l, node.Left)
            if node.Right: recurse(l, node.Right)
            return l
        return recurse([], self.Root)
    
    def postorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: AVLNode[K,V]) -> list[K]:
            if node.Left: recurse(l, node.Left)
            if node.Right: recurse(l, node.Right)
            if visit: visit(node.Value)
            l.append(node.Value)
            return l
        return recurse([], self.Root)

    def bforder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        queue = [self.Root]
        l = [self.Root.Value]
        while len(queue) != 0:
            node = queue.pop(0)
            if visit: visit(node.Value)
            if node.Left is not None:
                queue.append(node.Left)
                l.append(node.Left.Value)
            if node.Right is not None:
                queue.append(node.Right)
                l.append(node.Right.Value)
        return l
    
    def size(self) -> int:
        return self.Count

    def __str__(self) -> str:
        level_outputs = []
        def draw_tree(node: Optional[AVLNode], level: int = 0):
            if not node: return
            draw_tree(node.Right, level + 1)
            level_outputs.append(f"{" "*4*level} -> {str(node.Value)}")
            draw_tree(node.Left, level + 1)
        draw_tree(self.Root)
        return '\n'.join(level_outputs)