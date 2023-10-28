import pytest

from OptsFile.abc import IReadNode
from OptsFile.read_node import ReadNode

@pytest.fixture
def new_node():
    return ReadNode("*", content="...")

@pytest.fixture
def add_children(new_node):
    new_node.add_child_node(ReadNode("one", content="two"))
    new_node.add_child_node(ReadNode("red", content="blue"))
    another_node = ReadNode("blah")
    another_node.add_child_node(ReadNode("foo", content="bar"))
    new_node.add_child_node(another_node)
    return new_node

@pytest.fixture
def flat_results():
    ret1 = [("one", "two"), ("red", "blue"), ("blah", "")]
    ret2 = [("foo", "bar")]
    return ret1, ret2

@pytest.fixture
def nest_results():
    return {
        "*": {
            "one": "two",
            "red": "blue",
            "blah": {
                "foo": "bar"
            }
        }
    }

def test_read_node_init(new_node):
    assert isinstance(new_node, IReadNode)
    assert hasattr(new_node, "_name")
    assert isinstance(new_node._name, str)
    assert new_node._name == "*"
    assert hasattr(new_node, "_content")
    assert isinstance(new_node._content, str)
    assert new_node._content == "..."
    assert hasattr(new_node, "_children")
    assert isinstance(new_node._children, list)
    assert len(new_node._children) == 0

def test_read_node_add_child_node(add_children, flat_results):
    assert all(isinstance(child, ReadNode) for child in add_children._children)
    assert len(add_children._children) == 3
    for c, child in enumerate(add_children._children):
        assert child._name == flat_results[0][c][0]
        assert child._content == flat_results[0][c][1]

    assert len(add_children._children[2]._children) == 1
    for c, child in enumerate(add_children._children[2]._children):
        assert child._name == flat_results[1][c][0]
        assert child._content == flat_results[1][c][1]

def test_read_node_collapse(add_children, nest_results):
    opts = add_children.collapse()
    assert isinstance(opts, dict)
    assert opts == nest_results    
