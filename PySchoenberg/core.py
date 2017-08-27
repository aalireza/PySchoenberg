_ORDERED_NOTE_REPRS = tuple(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",
                             "A", "A#", "B"])


class Note(object):
    def parse(pretty_note):
        return Note(pretty_note[0], bool(pretty_note[-1] == "#"))

    def __init__(self, name, is_sharp=False):
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
    def __init__(self, row_list=_ORDERED_NOTE_REPRS):
        assert len(row_list) == 12
        self.__row = tuple([Note.parse(note) for note in row_list])

    def shift_row(self, amount):
        self.__row = (self.__row[amount:] + self.__row[:amount])

    def to_numerical(self):
        return tuple(map(int, self))

    def parse_numerical(numerical_row):
        return Row([
            _ORDERED_NOTE_REPRS[number - 1]
            for number in numerical_row
        ])

    def corresponding_column(self, arity):
        numerical_column = [int(self.__row[arity - 1])]
        for i in range(1, 12):
            candidate = ((numerical_column[-1] - (int(self.__row[i]) -
                                                  int(self.__row[i - 1]))) % 12)
            numerical_column.append(12 if candidate == 0 else candidate)
        return Row.parse_numerical(numerical_column)

    def __eq__(self, other):
        return all([self[index] == other[index] for index in range(12)])

    def __iter__(self):
        return self.__row.__iter__()

    def __getitem__(self, i):
        return self.__row[i]

    def __repr__(self):
        return "Row{!r}".format(self.__row)


class Matrix(object):
    def __init__(self, base_row):
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
