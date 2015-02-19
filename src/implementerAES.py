import atonalize
import aes
import basicMusic
import basicEncoding
from lxml import etree


def encoder(cipher, list12note, filexml, addenda="", readPath="../data/XML/",
            writePath="../data/AES/"):
    # Implements the whole thing: Since number of notes in a musical sheet must
    # exactly be a multiple of twelve times the number of characters in the
    # ciphertext (i.e. number of notes in a musical sheet be exactly the number
    # of methods over the 12-tone matrix) and that rarely happens (i.e. rarely
    # there won't be any exceptions), notes from the last note corresponding to
    # the last letter of the ciphertext till the end  will be deleted. So in
    # case of decoding, just the right notes in the right order be extracted.
    # We'd handle the case for length of embedded12 > number of notes in a
    # musical sheet by printing out the number of notes that are needed for the
    # ciphertext to be embedded and a message to use a larger musical sheet.

    randwn = atonalize.rand12wn(basicEncoding.normal2tuple(list12note))
    charnum = basicEncoding.ciphernum(cipher)
    mnum = basicEncoding.methodsnum(list12note)
    embedded12 = []

    # embedded12 is a list containing methods of the 12-tone matrix
    # corresponding to each character of the ciphertext.
    for element in charnum:
        embedded12 += mnum[element]
    embedded12.reverse()

    if len(embedded12) > basicMusic.numnotes(filexml, readPath=readPath):
        shortnotes = (len(embedded12) - basicMusic.numnotes(filexml,
                                                           readPath=readPath))
        print ("You lack " + str(shortnotes) + " number of notes in the list " +
               "of your musical sheets. Process is aborted. Please use a " +
               "larger one.")
        return False

    tree = etree.parse(str(readPath + filexml))
    root = tree.getroot()
    deleteFlag = None
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    for subnote in note:
                        stepFound = False
                        if subnote.tag == "pitch":
                            for subpitch in subnote:
                                if subpitch.tag == "step":
                                    try:
                                        notenum = embedded12.pop()
                                        inote = atonalize.getnote(notenum,
                                                                  randwn)
                                        if inote[1] == '':
                                            accidentalNeeded = False
                                            alterFound = False
                                        elif inote[1] != '':
                                            accidentalNeeded = True
                                            alterFound = False
                                        subpitch.text = str(inote[0])
                                        stepFound = True
                                        deleteFlag = False
                                    except IndexError:
                                        deleteFlag = True
                                elif subpitch.tag == "alter":
                                    alterFound = True
                                    if not deleteFlag:
                                        if not accidentalNeeded:
                                            subnote.remove(subpitch)
                                        elif accidentalNeeded:
                                            subpitch.text = "1"
                            if not deleteFlag:
                                if not alterFound and accidentalNeeded:
                                    alterFound = True
                                    alter = etree.SubElement(subnote, "alter")
                                    alter.text = "1"
                        if not deleteFlag:
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
                                        a = etree.SubElement(note, "accidental")
                                        a.text = str(inote[1])
                        elif deleteFlag:
                            break
                    if deleteFlag:
                        note.remove(subnote)
                if deleteFlag:
                    e1.remove(note)

    tree.write(str(writePath + filexml.split('.')[0] + addenda + ".xml"))


def decoder(list12note, filexml, readPath="../data/XML/"):
    # Implements the whole thing. It corresponds every 12 notes in the file to a
    # letter based on aes.num_rep_complete to get the ciphertext.

    if basicMusic.numnotes(filexml, enc=True, readPath=readPath) % 12 != 0:
        print "Invalid Encoding: Number of notes not multiple of 12"
        return False

    ciphertext = ""
    note12toMethod = []
    temp_normal_note = ""
    randwn = atonalize.rand12wn(basicEncoding.normal2tuple(list12note))
    mnum = basicEncoding.methodsnum(list12note)

    tree = etree.parse(str(readPath + filexml))
    root = tree.getroot()
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    assert len(note12toMethod) <= 12
                    for subnote in note:

                        if len(note12toMethod) != 12:
                            if subnote.tag == "pitch":
                                for subpitch in subnote:
                                    if subpitch.tag == "step":
                                        temp_normal_note += subpitch.text
                                        for other_subpitch in subnote:
                                            if other_subpitch.tag == "alter":
                                                assert other_subpitch.text == '1'
                                                temp_normal_note += '#'
                                note12toMethod.append(temp_normal_note)
                                temp_normal_note = ""

                        elif len(note12toMethod) == 12:
                            nmethod = []
                            method2cipher_number = None
                            note12toMethod = basicEncoding.normal2tuple(
                                note12toMethod)
                            nmethod = [atonalize.getnumber(n, randwn)
                                       for n in note12toMethod]
                            for number in range(24):
                                if nmethod == mnum[number]:
                                    method2cipher_number = number
                                    break
                            if method2cipher_number is None:
                                print str("The twelve-note block is not part " +
                                          "of the assigned methods from its " +
                                          " twelve-tone matrix. Conversion to" +
                                          " ciphertext failed.")
                                return False
                            elif method2cipher_number is not None:
                                ciphertext += aes.num_rep_complete[
                                    method2cipher_number]
                            note12toMethod = []
                            nmethod = []
    return ciphertext
