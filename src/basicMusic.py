from lxml import etree


universe = [('A', ''), ('A', 'sharp'), ('B', ''), ('C', ''), ('C', 'sharp'),
            ('D', ''), ('D', 'sharp'), ('E', ''), ('F', ''), ('F', 'sharp'),
            ('G', ''), ('G', 'sharp')]

normal_universe = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G",
                   "G#"]

correlative_universe = {"A": ('A', ''), "A#": ('A', 'sharp'), "B": ('B', ''),
                        "C": ('C', ''), "C#": ('C', 'sharp'), "D": ('D', ''),
                        "D#": ('D', 'sharp'), "E": ('E', ''), "F": ('F', ''),
                        "F#": ('F', 'sharp'), "G": ('G', ''),
                        "G#": ('G', 'sharp')}


def normalize(filexml, readPath="../data/XML/", writePath="../data/XML/"):
    # Only sharps are being used in this program. so gets rid
    # of all accidentals that are not #.
    tree = etree.parse(str(readPath + filexml))
    root = tree.getroot()
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    for subnote in note:
                        if subnote.tag == "pitch":
                            for subpitch in subnote:
                                if subpitch.tag == "alter":
                                    if subpitch.text != '1':
                                        subnote.remove(subpitch)
                            for other_subnote in note:
                                if other_subnote.tag != "accidental":
                                    if other_subnote.text != "sharp":
                                        note.remove(other_subnote)
    tree.write(str(writePath + filexml))


def numnotes(filexml, enc=False, readPath="../data/XML/"):
    # Total number of notes in the xml file.
    total = 0
    if not enc:
        with open(str(readPath + filexml), 'r') as f:
            lines = f.readlines()
    elif enc:
        with open(str(readPath + filexml), 'r') as f:
            lines = f.readline()
    for element in lines:
        if "<step" in element:
            total += 1
    return total
