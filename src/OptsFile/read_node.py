from __future__ import annotations

from typing import Any, Dict, Optional

from .abc import IReadNode

class ReadNode(IReadNode):

        def __init__(self, name: str, content: Optional[str] = None):
            """
            Constructor... this calls [`__init__`][OptsFile.abc.IReadNode] method.

            Args:
                name:
                    The name of the node (corresponds to the option name).
                content:
                    The content of the node (corresponds to the option value). This can be
                    `'None'` (which corresponds to the case of the option being a
                    subcategory).
            """

            super(ReadNode, self).__init__(name, content=content)

        def add_child_node(self, child: ReadNode) -> None:
            """
            This will add a new child node to the list of children of the current node.

            Args:
                child:
                    The child node to add.
            """

            self._children.append(child)

        def collapse(self) -> Dict[Any, Any]:
            """
            This will collapse the tree data structure into a dictionary using DFS.

            TODO: implement BFS too? Make this a user option?

            Returns:
                options:
                    The options nest data structure.
            """

            if len(self._children) == 0:
                return {self._name: self._content}
            else:
                options: Dict[Any, Any] = {self._name: {}}
                for child in self._children:
                    options[self._name].update(child.collapse())

                return options
