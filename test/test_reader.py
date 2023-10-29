import collections
import os
import pathlib
import unittest.mock

import pytest

from OptsFile.abc import IReader
from OptsFile.reader import Reader, ReaderError


@pytest.fixture
def new_reader():
    reader: Reader = Reader("sample.of")
    return reader


@pytest.fixture
def sample_optsfile_text():
    return [
        "Car:\n",
        "\tMake: Honda\n",
        "\tModel: Accord",
        "\n",
        "Bike:\n",
        "\tType: Mountain\n",
    ]


@pytest.fixture
def sample_text_format_output():
    entry = collections.namedtuple("entry", ["depth", "content"])
    return [
        entry(0, ["Car"]),
        entry(1, ["Make:", "Honda"]),
        entry(1, ["Model:", "Accord"]),
        entry(0, ["Bike"]),
        entry(1, ["Type:", "Mountain"]),
    ]


def test_reader_init_error_file_not_found():
    with pytest.raises(AssertionError) as exc:
        Reader("durp.of")

    filename: pathlib.Path = pathlib.Path(os.path.abspath("durp.of"))
    assert exc.value.args[0] == f"***ERROR***:\t{filename} does not exist!"


def test_reader_init(new_reader):
    assert isinstance(new_reader, IReader)
    assert hasattr(new_reader, "_filename")
    assert isinstance(new_reader._filename, pathlib.Path)
    assert new_reader._filename == pathlib.Path(os.path.abspath("sample.of"))


@unittest.mock.patch.object(Reader, "_format_text")
@unittest.mock.patch("builtins.open")
def test_reader_read_from_file(mock_format, mock_open, new_reader):
    new_reader.read_from_file()
    mock_format.assert_called_once()
    mock_open.assert_called_once()


@unittest.mock.patch.object(Reader, "_check_for_tabs")
def test_reader_format_text(
    mock_check, sample_optsfile_text, sample_text_format_output
):
    mock_check.return_value = "\t"
    entries = Reader._format_text(sample_optsfile_text)
    assert "depth" in entries[0]._fields
    assert "content" in entries[0]._fields
    assert len(entries) == len(sample_optsfile_text) - 1
    for entry1, entry2 in zip(entries, sample_text_format_output):
        assert entry1 == entry2


@pytest.mark.parametrize(
    ("scenario", "content", "result"),
    [
        ("tabs", "\t\tBlah", "\t"),
        ("spaces", "        Blah", "    "),
        ("error", " Blah", ""),
    ],
)
def test_reader_check_for_tabs(scenario, content, result):
    if scenario == "error":
        with pytest.raises(ReaderError) as exc:
            Reader._check_for_tabs(content)

        assert (
            exc.value.args[0] == "***ERROR***:\tThe current line seems to be malformed!"
        )

    else:
        assert Reader._check_for_tabs(content) == result

@pytest.mark.parametrize(
    ("scenario", "content", "result"),
    [
        ("column", "Line:", "Line"),
        ("no column", "Line", ""),
    ]
)
def test_reader_remove_column(scenario, content, result):
    reader = Reader("sample.of")
    if scenario == "no column":
        with pytest.raises(ReaderError) as exc:
            reader._remove_column(content)

        assert exc.value.args[0] == "***ERROR***:\tThe current line seems to be malformed!"

    else:
        assert reader._remove_column(content) == result
