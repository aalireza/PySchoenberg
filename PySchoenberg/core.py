class Note(object):
    def __init__(self, name, is_sharp=False):
        self.name = name.capitalize()
        self.is_sharp = is_sharp

    def __repr__(self):
        return "{}{}".format(
            self.name,
            ("#" if self.is_sharp else ''))

    def __eq__(self, other):
        if not isinstance(other, Note):
            raise TypeError
        return self.name == other.name and self.is_sharp == other.is_sharp

    def __lt__(self, other):
        if not isinstance(other, Note):
            raise TypeError
        if self == other:
            return False
        if self.name == other.name:
            return other.is_sharp
        return self.name < other.name


NOTES = [
    Note(note[0], bool(note[-1] == "#"))
    for note in ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
]
