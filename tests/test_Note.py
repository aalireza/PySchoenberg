from PySchoenberg.core import Note
import pytest


@pytest.mark.parametrize(('pretty_note', 'note', 'is_sharp'), [
    ("C#", "C", True),
    ("C", "C", False),
    ("G#", "G", True)
])
def test_parse(pretty_note, note, is_sharp):
    assert Note.parse(pretty_note) == Note(note, is_sharp)


@pytest.fixture()
def notes():
    return [Note.parse(pretty_note) for pretty_note in [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    ]]


def test_int(notes):
    for index, note in enumerate(notes):
        assert int(note) == index + 1

@pytest.mark.parametrize(('first', 'second'), [(0, 1), (0, 11), (5, 9)])
def test_order(notes, first, second):
    assert notes[first] < notes[second]


@pytest.mark.parametrize(('first', 'second'), [(0, 0), (1, 0)])
def test_order_negative(notes, first, second):
    assert not (notes[first] < notes[second])


@pytest.mark.parametrize(('first', 'second'), [(0, 0), (1, 1)])
def test_equality(notes, first, second):
    assert notes[first] == notes[second]
