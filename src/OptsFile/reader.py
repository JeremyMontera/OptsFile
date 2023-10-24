import os
import pathlib
from typing import Any, Dict, List


class OptsFileReader:
    @staticmethod
    def _validate(filepath: pathlib.Path) -> None:
        """
        This will make sure the file exists and has the appropriate extension.

        Args:
            filepath:
                The path to the file to read from.
        """

        assert filepath.exists(), "***ERROR***:\tThe file doesn't exist!"

    @staticmethod
    def read_from_file(filename: str) -> Dict[str, Any]:
        """
        This will read from an `OptsFile` file type. It is responsible for parsing the
        structure of the OptsFile and converting it to a dictionary.

        Args:
            filename:
                The name of the file to read from.

        Returns:
            opts_dict:
                The converted dictionary.
        """

        # Convert filename string to `pathlib.Path` object and validate.
        filepath: pathlib.Path = pathlib.Path(os.path.abspath(filename))
        OptsFileReader._validate(filepath)

        # Read from the `.of` file and populate the options dictionary.
        opts_dict: Dict[str, Any] = {}
        with open(filepath, "r") as f:
            for line in f.readlines():
                if len(line) > 1:
                    print(f"{line.rstrip()=}")
