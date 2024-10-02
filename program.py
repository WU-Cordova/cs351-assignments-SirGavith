from datastructures.avltree import AVLTree
from datastructures.test_avltree_inserts import TestAVLInserts
from tests.car import Car, Color, Make, Model

def main():
    print('Hello world!')

    car = Car(vin='123456789', color=Color.RED, make=Make.TOYOTA, model=Model.COROLLA)
    print(car)

if __name__ == '__main__':
    # main()
    # tree = AVLTree()
    # tree.insert(6)
    # tree.insert(4)
    # tree.insert(2)
    tree = AVLTree[int, int]()

    for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
        tree.insert(node, node)

    assert tree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print(str(tree))

    assert tree.bforder() == [5, 3, 8, 2, 4, 6, 9, 1, 7, 10]


    TestAVLInserts()