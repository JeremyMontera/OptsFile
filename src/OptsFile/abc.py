from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional


class IReader(metaclass=abc.ABCMeta):

    """
    This is the reader interface. The reader should:
    * Read from a `.of` file
    * Convert the text from a tab-indented hierarchical structure to a nested
      dictionary with approprate key-value pairs.
    """

    @abc.abstractmethod
    def __init__(self, filename: str):
        """
        Constructor...

        Args:
            filename:
                The name of the file to read from.
        """

        self._filename: str = filename
        """
        The name of the file to read from.

        Type:
            str
        """

    @abc.abstractmethod
    def read_from_file(self) -> List[str]:
        """
        This will read from the provided `.of` file and return the properly formatted
        lines from that file. Note that this method is left separate from the parsing
        method because: (1) separation of responsibilities, and (2) in case the user
        wants the (modified) plain text.

        Returns:
            text:
                The (modified) plain text.
        """

        ...

    @abc.abstractmethod
    def parse_text(self, text: List[str]) -> Dict[Any, Any]:
        """
        This will convert the text read in from the target file into a dictionary. This
        parsing will involve using a tree data structure and will collapse it into the
        target nested dictionary.

        Args:
            text:
                The (modified) plain text.

        Returns:
            options:
                The nested dictionary containing all of the user options.
        """

        ...


class IReadNode(metaclass=abc.ABCMeta):

    """
    This is a node interface which, when combined with other nodes, will form a tree
    that will parse the text read in from the target file into an options nested
    dictionary for the user to consume. This should be able to:
    * Add new children nodes (nested options).
    * Collapse into a dictionary and recusively add all of its childrens' dictionaries.
    """

    @abc.abstractmethod
    def __init__(self, name: str, content: Optional[str] = None):
        """
        Constructor...

        Args:
            name:
                The name of the node (corresponds to the option name).
            content:
                The content of the node (corresponds to the option value). This can be
                `'None'` (which corresponds to the case of the option being a
                subcategory).
        """

        self._name: str = name
        """
        The name of the node.

        Type:
            str
        """

        self._content: str = "" if content is None else content
        """
        The content of the node.

        Type:
            str
        """

        self._children: List[IReadNode] = []
        """
        A list of all the children of this node instance.

        Type:
            List[IReadNode]
        """

    @abc.abstractmethod
    def add_child_node(self, child: IReadNode) -> None:
        """
        This will add a new child node to the list of children of the current node.

        Args:
            child:
                The child node to add.
        """

        ...

    @abc.abstractmethod
    def collapse(self) -> Dict[Any, Any]:
        """
        This will collapse the tree data structure into a dictionary using DFS.

        TODO: implement BFS too? Make this a user option?

        Returns:
            options:
                The options nest data structure.
        """

        ...
