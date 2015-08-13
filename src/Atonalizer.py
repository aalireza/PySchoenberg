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
import DataToolbox
import MultimediaToolbox
import MusicToolbox


def Atonalizer(noteRow, fileXml, writePath, addenda):
    """
    It atonalizes the sheet music by getting a noteRow, generating a 12 tone
    matrix out of it and randomly picking rows/columns from the matrix and map
    them to 12 notes and replace the existing notes from the beginning until
    it runs out of notes, then creates new notes until total number of notes are
    divisible by 12 and then stops and write the result in a new MusicXMl file.
    Finally, it adds a signiture to the file to indicate atonalizaton if one
    were to view the pdf of the outcome.

    Parameters
    ----------
    noteRow:        [(str, str)]
                    A permutation of MusicToolbox.UNIVERSE e.g. ('A', 'sharp')
                    is in `noteRow`
    fileXml:        str
                    Absolute path of the fileXml
    writePath:      str
                    Absolute path to the directory that the result will be
                    written in.
    addenda:        str
                    Will be added to the name of the initial file e.g.
                    _Atonalized-

    Returns
    -------
    finalFilePath:  str
                    Absolute path to the outcome

    See Also
    --------
    MusicToolbox.random12NotesNumbers(noteList),
    MusicToolbox.generateMatrix(noteRowWithNumbers),
    MusicToolbox.methods(matrix),
    Main(filePath, noteRow)
    """
    fileXmlName = DataToolbox.pathHandler(fileXml)[1]
    noteRowWithNumbers = MusicToolbox.random12NotesNumbers(noteRow)
    numberList = MusicToolbox.methods(
        noteRowWithNumbers, MusicToolbox.numberOfNotes(fileXml))
    numberList.reverse()
    tree = etree.parse(fileXml)
    root = tree.getroot()
    for e0 in root:
        for e1 in e0:
            for note in e1:
                if note.tag == "note":
                    for subnote in note:
                        stepFound = False
                        if subnote.tag == "pitch":
                            alterFound = False
                            for subpitch in subnote:
                                if subpitch.tag == "step":
                                    # For each pitch in a sheet music with step
                                    # in it, it pops a number from numberList,
                                    # gets what kind of note it is and it'll be
                                    # inserted instead. Accidentals will also
                                    # be handled, that is, if accidental is
                                    # needed it will insert a sharp and if not,
                                    # it'll either do nothing or delete the
                                    # existing accidental of the note.
                                    noteNumber = numberList.pop()
                                    currentNote = MusicToolbox.getNote(
                                        noteNumber, noteRowWithNumbers)
                                    if currentNote[1] == '':
                                        accidentalNeeded = False
                                    elif currentNote[1] != '':
                                        accidentalNeeded = True
                                    subpitch.text = str(currentNote[0])
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
                            for otherSubnote in note:
                                if otherSubnote.tag == "accidental":
                                    accidentalFound = True
                                    if accidentalNeeded:
                                        otherSubnote.text = str(currentNote[1])
                                    elif not accidentalNeeded:
                                        note.remove(otherSubnote)
                                    break
                            if not accidentalFound:
                                if accidentalNeeded:
                                    accidental = etree.SubElement(note,
                                                                  "accidental")
                                    accidental.text = str(currentNote[1])
    # Atonalization is over. Bellow a signiture will be added.
    try:
        defaults = root.find("defaults")
        pageLayout = defaults.find("page-layout")
        pageHeight = pageLayout.find("page-height")
        pad = 10
        credit = etree.Element("credit", {"page": "1"})
        creditWords = etree.SubElement(credit, "credit-words",
                                       {"default-x": str(pad),
                                        "default-y": str(int(float(
                                            pageHeight.text) - pad)),
                                        "font-size": "12",
                                        "justify": "left",
                                        "valign": "top"})
        creditWords.text = "Atonalized by PySchoenberg"
        defaults.addnext(credit)
    except:
        pass
    finalFileName = "{}.xml".format(fileXmlName + addenda)
    finalFilePath = writePath + finalFileName
    tree.write(finalFilePath)
    return finalFilePath


def Main(filePath):
    """
    It's the proper way to interact with Atonalizer. It first converts the file
    into MusicXML if the format is not xml and then calls the Atonalizer
    function to produce and save the atonalized xml file, then asks user to view
    the result as pdf or play it as wav or do nothing and just save the xml
    file.
    The fundamental note row would either be provided by the user or generated
    randomly.

    Parameters
    ----------
    filePath:       str
                    Aboslute path to the initial file

    See Also
    --------
    Atonalizer(noteRow, fileXml, writePath, addenda),
    MultimediaToolbox.decide(filePath)
    """
    srcParentDir = DataToolbox.config()[-1]
    fileName, fileFormat = DataToolbox.pathHandler(filePath)[1:]
    writePath = "{}/data/XML/".format(srcParentDir)
    decision = None
    while decision not in ['y', 'n']:
        decision = str(raw_input("Do you wish to provide the note row yoursel" +
                                 "f? If not, it'll be generated randomly? " +
                                 "(y/n) "))
    if decision == 'y':
        normalNoteRow = MusicToolbox.acquireNormalNoteRow()
        noteRow = MusicToolbox.normalToTuple(normalNoteRow)
    elif decision == 'n':
        noteRow = MusicToolbox.random12Notes()
    if fileFormat != "xml":
            filePath = MultimediaToolbox.Main(filePath, "_Converted-",
                                              "xml", False)
            fileName = DataToolbox.pathHandler(filePath)[1]
    counter = DataToolbox.fileCounter(fileName, "xml", "_Atonalized-")
    finalFilePath = Atonalizer(noteRow, filePath, writePath,
                               "_Atonalized-{}".format(counter))
    MultimediaToolbox.decide(finalFilePath)
