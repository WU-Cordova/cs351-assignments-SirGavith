from __future__ import annotations
from typing import Callable, Generic, Iterable, List, Optional
from datastructures.iavltree import IAVLTree, K, V


class Node(Generic[K,V]):
    Left: Node[K,V] = None
    Right: Node[K,V] = None
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


class AVLTree(IAVLTree[K,V], Generic[K,V]):
    Root: Node[K,V] = None
    Count = 0
    
    def __init__(self, seq: Iterable[tuple[K,V]] = None) -> None:
        for k,v in seq or []: self.insert(k,v)

    def insert(self, key: K, val: V = None) -> None:
        self.Count += 1
        if self.Root is None:
            self.Root = Node(key, val)
            return
        self.Root = self.insert_helper(Node(key,val), self.Root)
        

    def insert_helper(self, newNode: Node[K,V], node: Node[K,V]) -> Node[K,V]:
        if node is None:
            return newNode

        if (newNode.Key < node.Key):
            node.Left = self.insert_helper(newNode, node.Left)
        else:
            node.Right = self.insert_helper(newNode, node.Right)
        
        node.recalc_height()

        if node.bf > 1 or node.bf < -1:
            return self.balance_tree(node)

        return node


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
        def recurse(node: Node[K,V]) -> V:
            child = node.Left if key < node.Key else node.Right
            return recurse(child) if child is not None else None

        return recurse(self.Root)

    def delete(self, key: K) -> None:

        self.Count -= 1
        raise NotImplementedError
    
    #TODO: test delete
    
    def delete_helper(self, node: Node[K,V], key: K) -> Node[K,V]:
        if node is None:
            return None
        
        if (key < node.Key):
            node.Left = self.insert_helper(node.Left, key)
        else:
            node.Right = self.insert_helper(node.Right, key)
        
        #find successor
        successor = self.find_sucessor(node)
        node.Key = successor.Key
        node.Value = successor.Value
        node.Right = self.delete_helper(node.Right, successor.Key)

        if node is not None:
            node.recalc_height()
            if node.bf > 1 or node.bf < -1:
                return self.balance_tree(node)

        return None
    
    def find_sucessor(self, node: Node[K,V]) -> Node[K,V]:
        if node.Left is None or node.Right is None:
            return node.Left or node.Right
        current = node.Right
        while current.Left is not None:
            current = current.Left
        return current

    def inorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: Node[K,V]) -> list[K]:
            if node.Left: recurse(l, node.Left)
            if visit: visit(node.Value)
            l.append(node.Value)
            if node.Right: recurse(l, node.Right)
            return l
        return recurse([], self.Root)
    
    def preorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: Node[K,V]) -> list[K]:
            if visit: visit(node.Value)
            l.append(node.Value)
            if node.Left: recurse(l, node.Left)
            if node.Right: recurse(l, node.Right)
            return l
        return recurse([], self.Root)
    
    def postorder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        def recurse(l: list[K], node: Node[K,V]) -> list[K]:
            if node.Left: recurse(l, node.Left)
            if node.Right: recurse(l, node.Right)
            if visit: visit(node.Value)
            l.append(node.Value)
            return l
        return recurse([], self.Root)

    def bforder(self, visit: Callable[[V], None] | None = None) -> List[K]:
        stack = [self.Root]
        l = [self.Root.Value]
        while len(stack) != 0:
            node = stack.pop()
            if node.Right is not None:
                stack.append(node.Right)
            if node.Left is not None:
                stack.append(node.Left)
                l.append(node.Left.Value)
            if node.Right is not None:
                l.append(node.Right.Value)
        return l
    
    #TODO: fix inorder

    def size(self) -> int:
        return self.Count

    def __str__(self) -> str:
        level_outputs = []
        def draw_tree(node: Optional[Node], level: int = 0):
            if not node: return
            draw_tree(node.Right, level + 1)
            level_outputs.append(f"{" "*4*level} -> {str(node.Value)}")
            draw_tree(node.Left, level + 1)
        draw_tree(self.Root)
        return '\n'.join(level_outputs)