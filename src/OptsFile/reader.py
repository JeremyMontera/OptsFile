import os
import pathlib
from collections import namedtuple
from typing import Any, Dict, List

from .abc import IReader
from .read_node import ReadNode


class ReaderError(Exception):
    ...


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

        with open(self._filename, "r") as of:
            text: List[str] = of.readlines()

        return Reader._format_text(text)

    @staticmethod
    def _format_text(text: List[str]) -> List[namedtuple]:
        """
        This private method will format the text in a way for the parser to consume. It
        will not only strip the newline character from the end of each line, but it
        will also count the number of tabs and will split the line on spaces.

        Example:
            >>> text = ["\t\tfoo bar\n", "\t\tspam:\n", "\t\t\tturtle: duck\n"]
            >>> entries = Reader._format_text(text)
            >>> entries
            [(2, "foo", "bar"), (2, "spam:"), (3, "turtle", "duck")]

        Args:
            text:
                Text read in from [`read_from_file`][OptsFile.reader.Reader].

        Returns:
            entries:
                A list of tuples with the number of tabs and the entry items.
        """

        entry: namedtuple = namedtuple("entry", ["depth", "content"])
        entries: List[namedtuple] = []
        for line in text:
            line: str = line.rstrip()
            split_option: str = Reader._check_for_tabs(line)
            depth: int = line.count(split_option)
            content: List[str] = line[len(split_option) * depth :].split(" ")
            if len(content) == 1:
                content[0] = Reader._remove_column(content[0])
            
            entries.append(entry(depth, content))

        return entries

    @staticmethod
    def _check_for_tabs(line: str) -> str:
        """
        This private method will check if there are any tabs. Since linters like to
        replace tabs with whitespaces, we need to check if this has happened.

        Args:
            line:
                A line of text we are checking if there are tabs.

        Returns:
            split_option:
                If there are tabs, then this will be `'\t'`. If there are no tabs, then
                this will be `'    '`.
        """

        if "\t" not in line and "    " not in line and line[0] == " ":
            raise ReaderError("***ERROR***:\tThe current line seems to be malformed!")

        return "\t" if "\t" in line else "    "
    
    @staticmethod
    def _remove_column(content: str) -> str:
        """
        This will remove a column from the end of the subcategory line.

        Example:
            >>> example = "Foo:"
            >>> Reader._remove_column(example)
            "Foo"

        Args:
            content:
                Category line (will be the only item on the line).

        Returns:
            content:
                The modified line (the column stripped).
        """

        if content[-1] != ":":
            raise ReaderError("***ERROR***:\tThe current line seems to be malformed!")
        
        return content[:-1]

    def parse_text(
        self, entries: List[namedtuple], parser: ReadNode
    ) -> Dict[Any, Any]:
        """
        This will convert the text read in from the target file into a dictionary. This
        parsing will involve using a tree data structure and will collapse it into the
        target nested dictionary.

        Args:
            text:
                A list of tuples with the number of tabs and the entry items.
            parser:
                The parser (added here in case we come up with other ways of parsing).

        Returns:
            options:
                The nested dictionary containing all of the user options.
        """

        root: ReadNode = ReadNode("*")
        for entry in entries:
            depth, content = entry.depth, entry.content
