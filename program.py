from datastructures.avltree import AVLTree
from datastructures.test_avltree import TestAVLDeletes, TestAVLInserts
from tests.car import Car, Color, Make, Model

def main():
    # tree = AVLTree()
    # tree.insert(6)
    # tree.insert(4)
    # tree.insert(2)
    tree = AVLTree[int, int]()

    for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
        tree.insert(node, node)

    print(str(tree))

    assert tree.search(5) == 5


if __name__ == '__main__':
    main()