import os
import pathlib
from typing import Any, Dict, List

from .abc import IReader, IReadNode


class Reader(IReader):
    def __init__(self, filename: str):
        """
        Constructor... this calls [`__init__`][OptsFile.abc.IReader] method.

        Args:
            filename:
                The name of the file to read from.
        """

        super(Reader, self).__init__(filename)
        self._filename: pathlib.Path = pathlib.Path(os.path.abspath(self._filename))
        assert (
            self._filename.exists()
        ), f"***ERROR***:\t{self._filename} does not exist!"

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

    def parse_text(self, text: List[str], parser: object) -> Dict[Any, Any]:
        """
        This will convert the text read in from the target file into a dictionary. This
        parsing will involve using a tree data structure and will collapse it into the
        target nested dictionary.

        Args:
            text:
                The (modified) plain text.
            parser:
                The parser (added here in case we come up with other ways of parsing).

        Returns:
            options:
                The nested dictionary containing all of the user options.
        """

        ...
