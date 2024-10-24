import pytest

from datastructures.avltree import AVLTree
from datastructures.iavltree import IAVLTree

class TestAVLInserts():
    @pytest.fixture
    def avltree(self) -> AVLTree:
        tree = AVLTree[int, int]()
        for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
            tree.insert(node, node)
        return tree
    
    def test_insert_bforder(self, avltree: AVLTree) -> None: assert avltree.bforder() == [5, 3, 8, 2, 4, 6, 9, 1, 7, 10]
    def test_insert_inorder(self, avltree: AVLTree) -> None: assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    def test_insert_preorder(self, avltree: AVLTree) -> None: assert avltree.preorder() == [5, 3, 2, 1, 4, 8, 6, 7, 9, 10]
    def test_insert_postorder(self, avltree: AVLTree) -> None: assert avltree.postorder() == [1, 2, 4, 3, 7, 6, 10, 9, 8, 5]

class TestIAVLTree:
    
    @pytest.fixture
    def avltree(self) -> IAVLTree[int, int]:
        tree = AVLTree[int, int]()  # Replace AVLTree with your actual class
        for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
            tree.insert(node, node)
        return tree
    
    def test_insert(self, avltree: IAVLTree[int, int]) -> None:
        avltree.insert(11, 11)
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test_search_existing(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.search(5) == 5

    def test_search_nonexistent(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.search(11) is None

    def test_delete(self, avltree: IAVLTree[int, int]) -> None:
        avltree.delete(5)
        assert avltree.inorder() == [1, 2, 3, 4, 6, 7, 8, 9, 10]

    def test_delete_nonexistent(self, avltree: IAVLTree[int, int]) -> None:
        with pytest.raises(KeyError):
            avltree.delete(20)

    def test_inorder(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_preorder(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.preorder() == [5, 3, 2, 1, 4, 8, 6, 7, 9, 10]

    def test_postorder(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.postorder() == [1, 2, 4, 3, 7, 6, 10, 9, 8, 5]

    def test_bforder(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.bforder() == [5, 3, 8, 2, 4, 6, 9, 1, 7, 10]

    def test_size(self, avltree: IAVLTree[int, int]) -> None:
        assert avltree.size() == 10
        avltree.insert(11, 11)
        assert avltree.size() == 11
        avltree.delete(5)
        assert avltree.size() == 10

class TestAVLDeletes():
    @pytest.fixture
    def avltree(self) -> AVLTree:
        tree = AVLTree[int, int]()
        for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
            tree.insert(node, node)
        return tree

    def test_delete_leaf(self, avltree: AVLTree) -> None:
        avltree.delete(1)  # Deleting leaf node
        assert avltree.inorder() == [2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_delete_single_child(self, avltree: AVLTree) -> None:
        avltree.delete(9)  # Node with one child
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 10]

    def test_delete_two_children(self, avltree: AVLTree) -> None:
        avltree.delete(8)  # Node with two children
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 9, 10]

    def test_delete_root(self, avltree: AVLTree) -> None:
        avltree.delete(5)  # Deleting root node
        assert avltree.inorder() == [1, 2, 3, 4, 6, 7, 8, 9, 10]

    def test_delete_nonexistent(self, avltree: AVLTree) -> None:
        with pytest.raises(KeyError):
            avltree.delete(15)  # Trying to delete a nonexistent key
