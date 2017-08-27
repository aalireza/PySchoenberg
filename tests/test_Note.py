from PySchoenberg.core import Note, Row
from .utils import NOTES
import pytest

@pytest.mark.parametrize(('first', 'second'), [
    (NOTES[0], NOTES[1]),
    (NOTES[0], NOTES[11]),
    (NOTES[5], NOTES[9])
])
def test_order(first, second):
    assert first < second


@pytest.mark.parametrize(('first', 'second'), [
    (NOTES[0], NOTES[0]),
    (NOTES[1], NOTES[0]),
])
def test_order_negative(first,second):
    assert not (first < second)


@pytest.mark.parametrize(('first', 'second'), [
    (NOTES[0], NOTES[0]),
    (NOTES[1], NOTES[1]),
])
def test_equality(first, second):
    assert first == second


@pytest.mark.parametrize(('row', 'amount', 'result'), [
    (["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
     0,
     ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]),
    (["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
     2,
     ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#"]),
    (["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
     12,
     ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]),
])
def test_shifting_row(row, amount, result):
    first = Row(row)
    second = Row(result)
    first.shift_row(amount)
    assert first == second

