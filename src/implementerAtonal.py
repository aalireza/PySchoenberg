import basicMusic
import atonalize
from lxml import etree


def implementer(noterow, filexml, readPath="../data/XML/",
                writePath="../data/XML/", addenda=""):

    # Creates a list of numbers from randomly passing through methods over the
    # 12-tone matrix. It is intended to pop a number per notes of the sheet
    # music.
    notelist = noterow[:]
    randwn = atonalize.rand12wn(notelist)
    numberlist = atonalize.methods(randwn,
                                   basicMusic.numnotes(filexml,
                                                       readPath=readPath))
    numberlist.reverse()

    def noteHandler(n):
        # To be invoked below.
        for subnote in n:
            stepFound = False
            if subnote.tag == "pitch":
                alterFound = False
                for subpitch in subnote:
                    if subpitch.tag == "step":
                        # For each pitch in a sheet music with step in it, it
                        # pops a number from numberlist, getswhat kind of note
                        # it is and it'll be inserted instead. Accidentals will
                        # also be handled.
                        notenum = numberlist.pop()
                        inote = atonalize.getnote(notenum, randwn)
                        if inote[1] == '':
                            accidentalNeeded = False
                        elif inote[1] != '':
                            accidentalNeeded = True
                        subpitch.text = str(inote[0])
                        stepFound = True
                    elif subpitch.tag == "alter":
                        alterFound = True
                        if not accidentalNeeded:
                            subnote.remove(subpitch)
                        elif accidentalNeeded:
                            subpitch.text = "1"
                if not alterFound and accidentalNeeded:
                    alterFound = True
                    alter = etree.SubElement(subnote, "alter")
                    alter.text = "1"
            if stepFound:
                accidentalFound = False
                for other_subnote in note:
                    if other_subnote.tag == "accidental":
                        accidentalFound = True
                        if accidentalNeeded:
                            other_subnote.text = str(inote[1])
                        elif not accidentalNeeded:
                            note.remove(other_subnote)
                        break
                if not accidentalFound:
                    if accidentalNeeded:
                        accidental = etree.SubElement(note, "accidental")
                        accidental.text = str(inote[1])

    tree = etree.parse(str(readPath + filexml))
    root = tree.getroot()
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    noteHandler(note)

    tree.write(str(writePath + filexml.split('.')[0] + addenda + ".xml"))
