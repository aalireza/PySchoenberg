"""
This file is part of PySchoenberg.

    PySchoenberg is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, Version 2.

    PySchoenberg is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PySchoenberg.  If not, see <http://www.gnu.org/licenses/>.
"""


from lxml import etree
import AESToolbox
import DataToolbox
import MultimediaToolbox
import MusicToolbox


def encoder(ciphertext, normalNoteRow, fileXml, writePath, addenda):
    """
    The way that this program encodes a ciphertext in base 24, is to map each
    character of the ciphetext to a row/column of the 12 tone matrix, then
    getting that row/column and mapping every number on it to a note and filling
    fileXml. Here gets the ciphertext and a permutation of
    MusicToolbox.NORMAL_UNIVERSE as encoding key. Then gets the dictionary of
    numbers and their corresponding row/column and by feeding it into
    AESToolbox.stackProducer a note stack will be produced. Every time a note is
    find in the fileXml, stack is poped and the corresponding note will be
    replaced.

    Parameters
    ----------
    ciphertext:         str
                        Must be in base 24
    normalNoteRow:      [str]
                        A permutation of MusicToolbox.NORMAL_UNIVERSE
    fileXml:            str
                        Absolute path to the initial file
    writePath:          str
                        Absolute path to the directory where the result will be
                        written in
    addenda:            str
                        What'll be added to initial file's name e.g. _AES-

    Returns
    -------
    finalFilePath:      str
                        Absolute path to the outcome

    See Also
    --------
    MusicToolbox.generateMatrix(noteRowWithNumbers),
    MusicToolbox.methods(matrix),
    MusicToolbox.rowColumnNumbers(noteRowWithNumbers),
    EncryptAndEncodeMain(filePath),
    decoder(normalNoteRow, fileXml),
    DecodeAndDecryptMain(filePath),
    AESToolbox.stackProducer(ciphertextNumbers, rowColumnNumbers, fileXml)
    """
    fileXmlName = DataToolbox.pathHandler(fileXml)[1]
    noteRow = MusicToolbox.normalToTuple(normalNoteRow)
    noteRowWithNumbers = MusicToolbox.random12NotesNumbers(noteRow)
    ciphernum = AESToolbox.ciphernum(ciphertext)
    rowColumnNumbers = MusicToolbox.rowColumnNumbers(noteRowWithNumbers)
    noteStack = AESToolbox.stackProducer(ciphernum, rowColumnNumbers, fileXml)
    if not noteStack:
        raise SystemExit
    tree = etree.parse(fileXml)
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
                                    # Since number of notes in a musical sheet
                                    # must exactly be a multiple of twelve times
                                    # the number of characters in the ciphertext
                                    # (i.e. number of notes in a musical sheet
                                    # be exactly the number of methods over the
                                    # 12-tone matrix) and that rarely happens
                                    # (i.e. rarely there won't be any
                                    # exceptions), notes from the last note
                                    # corresponding to the last letter of the
                                    # ciphertext till the end  will be deleted.
                                    # So in case of decoding, just the right
                                    # notes in the right order would be
                                    # extracted.
                                    try:
                                        currentNoteNumber = noteStack.pop()
                                        currentNote = (
                                            MusicToolbox.getNote(
                                                currentNoteNumber,
                                                noteRowWithNumbers))
                                        if currentNote[1] == '':
                                            accidentalNeeded = False
                                            alterFound = False
                                        elif currentNote[1] != '':
                                            accidentalNeeded = True
                                            alterFound = False
                                        subpitch.text = currentNote[0]
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
                                for otherSubnote in note:
                                    if otherSubnote.tag == "accidental":
                                        accidentalFound = True
                                        if accidentalNeeded:
                                            otherSubnote.text = currentNote[1]
                                        elif not accidentalNeeded:
                                            note.remove(otherSubnote)
                                        break
                                if not accidentalFound:
                                    if accidentalNeeded:
                                        newNode = etree.SubElement(note,
                                                                   "accidental")
                                        newNode.text = currentNote[1]
                        elif deleteFlag:
                            break
                    if deleteFlag:
                        note.remove(subnote)
                if deleteFlag:
                    e1.remove(note)
    finalFileName = "{}.xml".format(fileXmlName + addenda)
    finalFilePath = writePath + finalFileName
    tree.write(finalFilePath)
    return finalFilePath


def EncryptAndEncodeMain(filePath):
    """
    It's the proper way to interact with encoder and AESToolbox.encrypt
    functions. It first asks user for a message, encryption key and an encoding
    key which is a permutation of MusicToolbox.NORMAL_UNIVERSE. Then Encrypts
    the message and produces the ciphertext and will feed that inside the
    encoder function (It'll convert the initial file to MusicXML if its format
    is not xml), then asks user to either play it as wav or view it as pdf or
    do nothing and save the encoded xml.

    Parameters
    ----------
    filePath:       str
                    Absolute path to the encoded file.

    See Also
    --------
    encoder(ciphertext, normalNoteRow, fileXml, writePath, addenda),
    MusicToolbox.acquireNormalNoteRow(),
    AESToolbox.getEncryptionKey()
    AESToolbox.encrypt(message, key),
    MultimediaToolbox.Main(initialFile, addenda, choice, shouldRunIt),
    MultimediaToolbox.decide(filePath)
    """
    srcParentDir = DataToolbox.config()[-1]
    fileName, fileFormat = DataToolbox.pathHandler(filePath)[1:]
    secretMessage = str(raw_input("What is your message? "))
    encryptionKey = AESToolbox.getEncryptionKey()
    noteKey = MusicToolbox.acquireNormalNoteRow()
    ciphertext = AESToolbox.encrypt(secretMessage, encryptionKey)
    writePath = "{}/data/AES/".format(srcParentDir)
    if fileFormat != "xml":
        filePath = MultimediaToolbox.Main(filePath, "_Converted-", "xml",
                                          False)
        fileName = DataToolbox.pathHandler(filePath)[1]
    counter = DataToolbox.fileCounter(fileName, "xml", "_AES-")
    finalFilePath = encoder(ciphertext, noteKey, filePath, writePath,
                            "_AES-{}".format(counter))
    MultimediaToolbox.decide(finalFilePath)


def decoder(normalNoteRow, fileXml):
    """
    It is almost the inverse of encoder function. It reads the fileXml file,
    then maps every 12 notes of the fileXml to a row/column of the 12-tone
    matrix. Then the number of that note according to
    MusicToolbox.rowColumnNumbers will be derived and that number will be
    switched with its character according to AESToolbox.NUM_REPO_COMPLETE. The
    process will continue until all the notes are read and then the outcome
    would be a string i.e. the ciphertext.

    Parameters
    ----------
    normalNoterow:      [str]
                        A permutation of MusicToolbox.NORMAL_UNIVERSE
    fileXml:            str
                        Absolute path of the initial file

    Returns
    -------
    ciphertext:         str
                        It'll be in base 24... obviously

    Raises
    ------
    SystemExit:         If number of notes on `fileXml` % 12 != 0

    See Also
    --------
    MusicToolbox.generateMatrix(noteRowWithNumbers),
    MusicToolbox.methods(matrix),
    MusicToolbox.rowColumnNumbers(noteRowWithNumbers),
    encoder(ciphertext, normalNoteRow, fileXml, writePath, addenda),
    EncryptAndEncodeMain(filePath),
    DecodeAndDecryptMain(filePath)

    """
    encodingValidity = AESToolbox.encodingChecker(fileXml)
    if not encodingValidity:
        raise SystemExit
    ciphertext = ""
    noteRow = MusicToolbox.normalToTuple(normalNoteRow)
    noteRowWithNumbers = MusicToolbox.random12NotesNumbers(noteRow)
    rowColumnNumbers = MusicToolbox.rowColumnNumbers(noteRowWithNumbers)
    normalNotesToRowColumnNumber = []
    tempNormalNote = ""
    tree = etree.parse(fileXml)
    root = tree.getroot()
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    for subnote in note:
                        if len(normalNotesToRowColumnNumber) != 12:
                            if subnote.tag == "pitch":
                                for subpitch in subnote:
                                    if subpitch.tag == "step":
                                        tempNormalNote += subpitch.text
                                        for otherSubpitch in subnote:
                                            if otherSubpitch.tag == "alter":
                                                assert otherSubpitch.text == '1'
                                                tempNormalNote += '#'
                                normalNotesToRowColumnNumber.append(
                                    tempNormalNote)
                                tempNormalNote = ""
                        elif len(normalNotesToRowColumnNumber) == 12:
                            currentCipherDigit = None
                            notesToRowColumnNumber = (
                                MusicToolbox.normalToTuple(
                                    normalNotesToRowColumnNumber))
                            rowOrColumn = [(
                                MusicToolbox.getNumber(note,
                                                       noteRowWithNumbers))
                                           for note in notesToRowColumnNumber]
                            for number in range(24):
                                if rowOrColumn == rowColumnNumbers[number]:
                                    currentCipherDigit = number
                                    break
                            if currentCipherDigit is None:
                                print str("The twelve-note block is not part " +
                                          "of the assigned methods from its " +
                                          " twelve-tone matrix. Conversion to" +
                                          " ciphertext failed.")
                                return False
                            elif currentCipherDigit is not None:
                                ciphertext += AESToolbox.NUM_REPO_COMPLETE[
                                    currentCipherDigit]
                            normalNotesToRowColumnNumber = []
                            notesToRowColumnNumber = []
    return ciphertext


def DecodeAndDecryptMain(filePath):
    """
    It's the proper way to interact with decoder and AESToolbox.decrypt
    functions. It first asks user for the encryption key and the encoding key
    which is a permutation of MusicToolbox.NORMAL_UNIVERSE. Then converts the
    file to xml if it's already not and calls the decoder.

    Parameters
    ----------
    filePath:       str
                    Absolute path of the initial file

    Returns
    -------
    message:        str
                    The decrypted message in plain text

    Raises
    ------
    SystemExit:     If decryption was unsuccessful

    See Also
    --------
    AESToolbox.getEncryptionKey()
    MusicToolbox.acquireNormalNoteRow(),
    MultimediaToolbox.Main(intialFile, addenda, choice, shouldRunIt),
    decoder(normalNoteRow, fileXml)
    """
    fileName, fileFormat = DataToolbox.pathHandler(filePath)[1:]
    encryptionKey = AESToolbox.getEncryptionKey()
    noteKey = MusicToolbox.acquireNormalNoteRow()
    if fileFormat != "xml":
        filePath = MultimediaToolbox.Main(filePath, "_Converted-", "xml", False)
    ciphertext = decoder(noteKey, filePath)
    try:
        message = AESToolbox.decrypt(ciphertext, encryptionKey)
        print "Your message is:\n{}".format(message)
        return message
    except:
        print "Decryption Unsuccessful"
        raise SystemExit
