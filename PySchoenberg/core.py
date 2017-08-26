_ORDERED_NOTE_REPRS = tuple(["A", "A#", "B", "C", "C#", "D", "D#", "E",
                             "F", "F#", "G", "G#"])


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
            return self.name == other.name and self.is_sharp == other.is_sharp
        return False

    def __lt__(self, other):
        if (not isinstance(other, Note)) or (self == other):
            return False
        if self.name == other.name:
            return other.is_sharp
        return self.name < other.name


class Row(object):
    def __init__(self, row_list=_ORDERED_NOTE_REPRS):
        assert len(row_list) == 12
        self.__row = tuple([Note.parse(note) for note in row_list])

    def shift_row(self, amount):
        self.__row = (self.__row[amount:] + self.__row[:amount])

    def __eq__(self, other):
        return [self[index] == other[index] for index in range(12)]

    def __iter__(self):
        return self.__row.__iter__()

    def __getitem__(self, i):
        return self.__row[i]

    def __repr__(self):
        return "Row{}".format(self.__row)
