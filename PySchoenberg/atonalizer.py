from lxml import etree
from random import choice


def random_serial_row_deriving_closure(matrix):
    return lambda: getattr(matrix, choice(['row', 'column']))(choice(range(12)))


class AtonalStreamer(object):
    def _note_gen(row_deriving_closure):
        while True:
            for note in row_deriving_closure():
                yield note

    def __init__(self, row_deriving_closure):
        self._row_deriver = row_deriving_closure
        self._streamers = {1: AtonalStreamer._note_gen(self._row_deriver)}

    def get_one(self, staff):
        if int(staff) not in self._streamers:
            self._streamers[int(staff)] = AtonalStreamer._note_gen(
                self._row_deriver)
        return next(self._streamers[int(staff)])


class Transformer(object):
    def _form(initial, initial_name, initial_parent,
              atonal_note, new_text):
        if initial:
            if atonal_note.is_sharp:
                initial.text = new_text
            else:
                initial_parent.remove(initial)
        else:
            new_node = etree.SubElement(initial_parent, initial_name)
            new_node.text = new_text

    def check_possibility(note_node):
        return all([
            note_node.tag == 'note',
            any([bool(pitch.find('step') is not None)
                 for pitch in note_node.findall('pitch')])
        ])

    def of_alter(alter, pitch, atonal_note):
        Transformer._form(alter, "alter", pitch, atonal_note, "1")

    def of_accidental(accidental, note, atonal_note):
        Transformer._form(accidental, "accidental", note, atonal_note, "sharp")

    def of_note_node(initial, atonal_note):
        assert Transformer.check_possibility(initial)
        pitch = initial.find('pitch')
        step = pitch.find('step')
        alter = pitch.find('alter')
        accidental = initial.find('alter')

        step.text = atonal_note.name
        Transformer.of_alter(alter, pitch, atonal_note)
        Transformer.of_accidental(accidental, initial, atonal_note)


def atonalize(sheet, streamer):
    for index, part in enumerate(sheet.parts):
        for note_node in [
                note_node
                for note_node in sheet.notes(part_index=index)
                if Transformer.check_possibility(note_node)
        ]:
            note_node = Transformer.of_note_node(
                initial=note_node,
                atonal_note=streamer.get_one(
                    staff=(int(note_node.find('staff').text) or 1)
                )
            )
