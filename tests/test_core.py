from PySchoenberg.core import Note, NOTES
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
