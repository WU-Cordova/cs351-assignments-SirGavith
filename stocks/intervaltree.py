from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from datastructures.AvlNode import AVLNode
from datastructures.avltree import AVLTree

@dataclass
class IntervalNode:
    Interval: tuple[int, int]
    Max: int = 0
    Sublist: list[tuple[int, Any]] = None

    def __repr__(self):
        return f"IntervalNode({self.Interval} {self.Sublist} Max: {self.Max})"

class IntervalTree:
    def __init__(self):
        self.Tree: AVLTree[int, IntervalNode] = AVLTree()
    
    def insert(self, low: int, high: int, value: Any):
        node = self.Tree.search(low)

        if node:
            for i in range(len(node.Sublist)):
                if node.Sublist[i][0] > high:
                    node.Sublist.insert(i, (high, value))
                    break
        else:
            new_node = IntervalNode((low,high), high)
            new_node.Sublist = [(high, value)]
            self.Tree.insert(low, new_node, lambda node: self.UpdateMax(node))

    def delete(self, low: int, high: int, value):
        node = self.Tree.get_node(low)

        if not node: return None
        if len(node.Value.Sublist) > 1:
            node.Value.Sublist.remove((high, value))
            self.UpdateMax(node)
        else:
            self.Tree.delete(low, lambda node: self.UpdateMax(node))
        
    def UpdateMax(self, node: AVLNode[int, IntervalNode]):
        node.Value.Max = max(node.Right.Value.Max if node.Right else 0,
                             node.Left.Value.Max if node.Left else 0,
                             *(s[0] for s in node.Value.Sublist))
        
    # Returns all intervals containing value
    def value_query(self, value) -> list[Any]:
        if self.Tree.Root is None: return []

        overlapping_intervals: tuple[int, int, Any] = []

        def recurse(node: AVLNode[int, IntervalNode]):
            if not node: return

            if value < node.Key:
                recurse(node.Left)
                return

            if node.Left and node.Left.Value.Max >= value:
                recurse(node.Left)
            if value <= node.Value.Max:
                for high,v in node.Value.Sublist:
                    if value <= high:
                        overlapping_intervals.append((node.Key, high, v))
                recurse(node.Right)

        recurse(self.Tree.Root)

        
        return overlapping_intervals
    
    # Returns all intervals overlapping with range [low, high]

    def range_query(self, low, high) -> list[Any]:
        if self.Tree.Root is None: return []

        overlapping_intervals: tuple[int, int, Any] = []

        def in_range(v: int):
            return v >= low or v <= high

        def recurse(node: AVLNode[int, IntervalNode]):
            if not node: return

            if high < node.Key:
                recurse(node.Left)
                return
            if low > node.Value.Max:
                recurse(node.Right)
                return
            
            for hi,v in node.Value.Sublist:
                if in_range(node.Key) or in_range(hi):
                    overlapping_intervals.append((node.Key, hi, v))

            if node.Right and node.Right.Key <= high:
                recurse(node.Right)

            if node.Left and node.Left.Value.Max >= low:
                recurse(node.Left)

        recurse(self.Tree.Root)
        return overlapping_intervals
    
    #Returns k lowest values by their low; if there are duplicates they are returned by order of insertion
    def lowest_k_values(self, k: int) -> list[Any]:
        if self.Tree.Root is None or k == 0: return []

        values: tuple[int, int, Any] = []

        def recurse(node: AVLNode[int, IntervalNode]):
            if node.Left: recurse(node.Left)
            for _,v in node.Value.Sublist:
                values.append(v)
                if len(values) == k: raise LookupError
            if node.Right: recurse(node.Right)

        try:
            recurse(self.Tree.Root)
        finally:
            return values 
    
    #Returns k highest values by their low; if there are duplicates they are returned by order of insertion
    def highest_k_values(self, k: int) -> list[Any]:
        if self.Tree.Root is None or k == 0: return []

        values: tuple[int, int, Any] = []

        def recurse(node: AVLNode[int, IntervalNode]):
            if node.Right: recurse(node.Right)
            for _,v in reversed(node.Value.Sublist):
                values.append(v)
                if len(values) == k: raise LookupError
            if node.Left: recurse(node.Left)

        try:
            recurse(self.Tree.Root)
        finally:
            return values 
