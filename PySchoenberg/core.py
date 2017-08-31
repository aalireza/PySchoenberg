from lxml import etree
from random import shuffle
import os


_ORDERED_NOTE_REPRS = tuple(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",
                             "A", "A#", "B"])


class Note(object):
    class Verification(object):
        def pretty(note):
            if note not in _ORDERED_NOTE_REPRS:
                raise TypeError("The note is not parsable")
            return True

    def parse(pretty_note):
        assert Note.Verification(pretty_note)
        return Note(pretty_note[0], bool(pretty_note[-1] == "#"))

    def __init__(self, name, is_sharp=False):
        assert len(name) == 1
        self.name = name.capitalize()
        self.is_sharp = is_sharp

    def __repr__(self):
        return "{}{}".format(
            self.name,
            ("#" if self.is_sharp else ''))

    def __eq__(self, other):
        if isinstance(other, Note):
            return int(self) == int(other)
        return False

    def __lt__(self, other):
        if (not isinstance(other, Note)) or (self == other):
            return False
        return int(self) < int(other)

    def __int__(self):
        return _ORDERED_NOTE_REPRS.index(self.__repr__()) + 1


class Row(object):

    class Verification(object):
        def length(row_list):
            if len(row_list) != 12:
                raise ValueError("There must be 12 notes in the row")
            if len(row_list) != len(set(row_list)):
                raise ValueError("There must be 12 unique notes in a row")
            return True

        def numerical(row_list):
            if not all([isinstance(note, int) for note in row_list]):
                raise TypeError("At least one note is not an integer")
            if not all([1 <= note <= 12 for note in row_list]):
                raise ValueError("At least one note is not between 1 and 12")
            return True

        def pretty(row_list):
            if any([note not in _ORDERED_NOTE_REPRS for note in row_list]):
                raise TypeError(
                    "At least one note does not have correct representation"
                )
            return True

        def note_object(row_list):
            if not all([isinstance(note, Note) for note in row_list]):
                raise TypeError("At least one note is not an instance of Note")
            return True

    def __init__(self, row_list):
        assert Row.Verification.length(row_list)
        assert Row.Verification.note_object(row_list)
        self.__row = tuple(row_list)

    def shift_row(self, amount):
        self.__row = (self.__row[amount:] + self.__row[:amount])

    def to_numerical(self):
        return tuple(map(int, self))

    def parse_pretty_notes(pretty_row_list):
        assert Row.Verification.length(pretty_row_list)
        assert Row.Verification.pretty(pretty_row_list)
        return Row(tuple([Note.parse(pretty_note)
                          for pretty_note in pretty_row_list]))

    def parse_numerical(numerical_row):
        assert Row.Verification.length(numerical_row)
        assert Row.Verification.numerical(numerical_row)
        return Row(list(map(Note.parse, ([_ORDERED_NOTE_REPRS[number - 1]
                                          for number in numerical_row]))))

    def corresponding_column(self, arity):
        numerical_column = [int(self.__row[arity - 1])]
        for i in range(1, 12):
            candidate = (numerical_column[-1] -
                         (int(self.__row[i]) - int(self.__row[i - 1]))) % 12
            numerical_column.append(12 if candidate == 0 else candidate)
        return Row.parse_numerical(numerical_column)

    def random():
        return Row.parse_pretty_notes(shuffle(_ORDERED_NOTE_REPRS))

    def __eq__(self, other):
        return all([self[index] == other[index] for index in range(12)])

    def __iter__(self):
        return self.__row.__iter__()

    def __getitem__(self, i):
        return self.__row[i]

    def __repr__(self):
        return "Row{!r}".format(self.__row)


class Matrix(object):

    class Verification(object):
        def base_row(row):
            if isinstance(row, Row):
                return True
            raise TypeError("The input row is not an instance of Row")

    def __init__(self, base_row):
        assert Matrix.Verification.base_row(base_row)
        # Looping through correspondign columns generates a transposed matrix
        # if it's fed with the base_row directly since there's no specific
        # representation of a column in Python and they must be represented as
        # rows. Also, the corresponding column of first arity of the
        # first column, would by definition be equivalent to the generating
        # base row itself. So to have the proper matrix, we'd feed it the
        # corresponding column of the first arity of the base_row instead of
        # base_row itself.
        transformed_base_row = base_row.corresponding_column(1)
        self.__matrix = [
            transformed_base_row.corresponding_column(arity)
            for arity in range(1, 13)
        ]

    @property
    def base_row(self):
        return self.__matrix[0]

    def to_numerical(self):
        return tuple([x.to_numerical() for x in self])

    def make_transposed(self):
        return Matrix(self.base_row.corresponding_column(1))

    def row(self, index):
        return self[index]

    def column(self, index):
        return self.base_row.corresponding_column(index + 1)

    def __iter__(self):
        return self.__matrix.__iter__()

    def __getitem__(self, i):
        return self.__matrix[i]

    def __repr__(self):
        return "Matrix{!r}".format(self.__matrix)


class Sheet(object):
    def __init__(self, path):
        self.tree = etree.parse(os.path.abspath(path))

    @property
    def root(self):
        return self.tree.getroot()

    @property
    def parts(self):
        return self.root.findall('part')

    def _find_all_flatly(things, name):
        names = list()
        for thing in things:
            names.extend(thing.findall(str(name)))
        return names

    def measures(self, part_index=None):
        if part_index is None:
            return Sheet._find_all_flatly(self.parts, 'measure')
        return self.parts[part_index].findall('measure')

    def notes(self, part_index=None, measure_index=None):
        if measure_index is None:
            return Sheet._find_all_flatly(self.measures(part_index), 'note')
        return self.measures(part_index)[measure_index].findall('note')

    def __embed_credits(self, pad=10):
        defaults = self.root.find("defaults")
        pageLayout = defaults.find("page-layout")
        pageHeight = pageLayout.find("page-height")
        credit = etree.Element("credit", {"page": "1"})
        creditWords = etree.SubElement(
            credit, "credit-words", {
                "default-x": str(pad),
                "default-y": str(int(float(pageHeight.text) - pad)),
                "font-size": "12",
                "justify": "left",
                "valign": "top"
            }
        )
        creditWords.text = "Atonalized by PySchoenberg"
        defaults.addnext(credit)

    def export(self, path):
        self.__embed_credits()
        self.tree.write(path)

    def __len__(self):
        return len(self.notes)
