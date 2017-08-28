from PySchoenberg.core import Note, Row
import pytest

def test_row():
    pass

def test_pretty_parse():
    pass


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
    first = Row.parse_pretty_notes(row)
    second = Row.parse_pretty_notes(result)
    first.shift_row(amount)
    assert first == second

def test_row_numerical_parsability():
    pass

def test_corresponding_column():
    pass

def test_row_equality():
    pass

