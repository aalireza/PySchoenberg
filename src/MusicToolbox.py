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


from music21 import serial
from lxml import etree
import DataToolbox
import random
import time


UNIVERSE = [('A', ''), ('A', 'sharp'), ('B', ''), ('C', ''), ('C', 'sharp'),
            ('D', ''), ('D', 'sharp'), ('E', ''), ('F', ''), ('F', 'sharp'),
            ('G', ''), ('G', 'sharp')]

NORMAL_UNIVERSE = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G",
                   "G#"]

CORRELATIVE_UNIVERSE = dict(zip(NORMAL_UNIVERSE, UNIVERSE))


def normalToTuple(normalNotesList):
    """
    Parameters
    ----------
    normalNotesList:    list of str
                        list containing elements of NORMAL_UNIVERSE

    Returns
    -------
    result:             list of str
                        list containing elements of UNIVERSE
    """
    result = [CORRELATIVE_UNIVERSE[i] for i in normalNotesList]
    if len(result) == 1:
        return result[0]
    return result


def tupleToNormal(noteList):
    """
    Parameters
    ----------
    noteList:   list of str
                list containing elements of UNIVERSE

    Returns
    -------
    result:     list of str
                list containing elements of NORMAL_UNIVERSE
    """
    copyCorrelativeUniversie = CORRELATIVE_UNIVERSE.copy()
    result = [dict(zip(copyCorrelativeUniversie.values(),
                       copyCorrelativeUniversie.keys()))[i] for i in noteList]
    if len(result) == 1:
        return result[0]
    return result


def random12Notes():
    """
    The function generates a random note row. This function is the basis of
    almost all other functions to come.

    Returns
    -------
    universeCopy:   [str]
                    A random permutation of UNIVERSE
    """
    universeCopy = UNIVERSE[:]
    random.shuffle(universeCopy)
    return universeCopy


def assignNumbers(note):
    """
    The functions generates the clock diagram by starting from the first note of
    the note row. It's a basis for assigning a number to each note of the note
    row.

    Parameters
    ----------
    note:   str
            First note of the note row that's an element of UNIVERSE

    Returns
    -------
    clock:  {str: int}
            A dictionary of the notes of UNIVERSE and their numbers according to
            the given parameter `note`
    """
    universeCopy = UNIVERSE[:]
    noteClock = (universeCopy[universeCopy.index(note):] +
                 universeCopy[:universeCopy.index(note)])
    clock = dict(zip(noteClock, range(12)))
    return clock


def random12NotesNumbers(noteList):
    """
    Assigns a number to each of the notes of the given note row, based on the
    first note.

    Parameters
    ----------
    noteList:               [str]
                            A permutation of UNIVERSE

    Returns
    -------
    noteListWithNumbers:    [(str, int)]
                            A list of tuples whose 0th index are elements of
                            `noteList` and 1th index are their number based on
                            clock diagram

    See Also
    -------
    assignNumbers(note)
    """
    clock = assignNumbers(noteList[0])
    noteListWithNumbers = [(noteList[i], clock[noteList[i]]) for i in range(12)]
    return noteListWithNumbers


def getNote(number, noteListWithNumbers):
    """
    Gets a note from its number.

    Parameters
    ----------
    number:                 int
                            A note's number in range(12) that was generated
                            based ontheir clock diagram.
    noteListWithNumbers:    [(str,int)]
                            A list of tuples wose 0th index are elements of
                            UNIVERSE and 1th index are their number based on
                            clock diagram. This argument will be generated via
                            the function `random12NotesNumbers` if users doesn't
                            provide normal note row themseves.

    Returns
    -------
    element[0]:             str
                            An element of UNIVERSE and noteListWithNumbers

    See Also
    --------
    random12NotesNumbers(noteList)
    """
    for element in noteListWithNumbers:
        if number == element[1]:
            return element[0]


def getNumber(note, noteListWithNumbers):
    """
    Gets a note from its number.

    Parameters
    ----------
    note:                   str
                            An element of UNIVERSE and noteListWithNumbers
    noteListWithNumbers:    [(str,int)]
                            A list of tuples wose 0th index are elements of
                            UNIVERSE and 1th index are their number based on
                            clock diagram. This argument will be generated via
                            the function `random12NotesNumbers` if users doesn't
                            provide normal note row themseves.

    Returns
    -------
    element[1]:             int
                            A note's number in range(12) that was generated
                            based ontheir clock diagram.

    See Also
    --------
    random12NotesNumbers(noteList)
    """
    for element in noteListWithNumbers:
        if note == element[0]:
            return int(element[1])


def generateMatrix(noteListWithNumbers):
    """
    Generates a unique 12 tone matrix. 12 different note rows could produce the
    same matrix (each will be one of its rows), but the matrix itself is unique
    for these 12 and its structure or order won't change.

    Parameters
    ----------
    noteListWithNumbers:    [(str,int)]
                            A list of tuples wose 0th index are elements of
                            UNIVERSE and 1th index are their number based on
                            clock diagram. This argument is generated via the
                            function `random12NotesNumbers`.

    Returns
    -------
    matrix:                 str
                            The generated 12 tone matrix based on note numbers.
                            It's in a str format like "Row1\nRow2\n...Row12\n "
                            where Row1,Row2,...,Row12 are a permutation of
                            range(12) in str format like " n1 n2 n3 ... n12"
                            This matrix is evidently not in a well formed format
                            and will be parsed via the following functions.

    See Also
    --------
    random12NotesNumbers(noteList), matrix.serial.rowToMatrix(numberList),
    leftToright(matrix), upToDown(matrix)
    """
    numberList = [int(noteListWithNumbers[i][1]) for i in range(12)]
    matrix = serial.rowToMatrix(numberList)
    return matrix


def leftToRight(matrix):
    """
    A valid path on 12 tone matrix can be a row of it, read from left to right.
    This function parses `matrix` to get these paths. Removes extra \n, turns
    matrix to a list of rows. Remove extra space from the rows and turns string
    of ints to ints.

    Parameters
    ----------
    matrix:                 str
                            The generated 12 tone matrix based on note numbers.
                            It's in a str format like "Row1\nRow2\n...Row12\n "
                            where Row1,Row2,...,Row12 are a permutation of
                            range(12) in str format like " n1 n2 n3 ... n12"
                            This matrix is evidently not in a well formed format
                            and will be parsed via the following functions.

    Returns
    -------
    rows:                   [[int]]
                            A list i.e. the matrix, whose elements are a list of
                            ints i.e. its rows.

    See Also
    --------
    generateMatrix(noteListWithNumbers)
    """
    normalizedMatrix = matrix.split('\n')
    rows = [map(int, normalizedMatrix[i].split()) for i in range(12)]
    return rows


def upToDown(matrix):
    """
    First parses matrix to get its rows using leftToRight. Then gets the
    list of the columns of the matrix (i.e. a list who has 12 elements that
    are all lists of 12 numbers) by looping through each element of rows 12
    times to assign the numbers with the same index to a column.
    Parameters
    ----------
    matrix:                 str
                            The generated 12 tone matrix based on note numbers.
                            It's in a str format like "Row1\nRow2\n...Row12\n "
                            where Row1,Row2,...,Row12 are a permutation of
                            range(12) in str format like " n1 n2 n3 ... n12"
                            This matrix is evidently not in a well formed format
                            and will be parsed via the following functions.

    Returns
    -------
    columns:                [[int]]
                            A list i.e. the matrix, whose elements are a list of
                            ints i.e. its columns.

    See Also
    --------
    generateMatrix(noteListWithNumbers), leftToRight(matrix)
    """
    rows = leftToRight(matrix)
    columns = [[int(rows[j][i]) for j in range(12)] for i in range(12)]
    return columns


def methods(noteListWithNumbers, totalNotesNeeded):
    """
    Generates enough numbers by randomly picking methods from the 12 tone
    matrix to fill up all the music sheet.

    Parameters
    ----------
    noteListWithNumbers:    [(str, int)]
                            A list of tuples whose 0th index are elements of
                            `noteList` and 1th index are their number based on
                            clock diagram.
    totalNotesNeeded:       int
                            Total number of notes needed to fill up the sheet.
                            It should be derived from `numberOfNotes` function.

    Returns
    -------
    numberList              [int]
                            Total number of note numbers that will be used to
                            fill the sheet.

    See Also
    --------
    random12NotesNumbers(noteList), generateMatrix(noteListWithNumbers),
    getNumber(note, noteListWithNumbers)
    """
    matrix = generateMatrix(noteListWithNumbers)
    methodList = [leftToRight, upToDown]
    numberList = [getNumber(i[0], noteListWithNumbers)
                  for i in noteListWithNumbers]
    upperlimit = (totalNotesNeeded/12) + 1  # If not enough notes, go over
    steps = 0
    while steps <= upperlimit:
        # Result of random.choice(methodList) is a function name in
        # methodList, the argument would be a matrix that'll be parsed to get
        # either its rows or its columns. Then random.randint(0,11) randomly
        # picks one of the rows or columns and adds it to the available
        # numberList that we've got from the initial 12 notes.
        numberList += random.choice(methodList)(matrix)[random.randint(0, 11)]
        steps += 1
    return numberList


def rowColumnNumbers(noteListWithNumbers):
    """
    Assign a number to all of the rows and columns of the 12-tone matrix that
    will be uniquely generated by the given noteListWithNumbers. Since the
    position of the rows/columns of the matrix don't change, it'll be the basis
    for encoding ciphertexts of base 24 (i.e. the bases for connecting 12 rows
    to 12 letters of ciphertext and 12 columns to another 12 letters and fill up
    the sheet based on the related rows/columns). We also don't call matrix as
    an argument (since it'll be the same), to reduce argument noise.

    Parameters
    ----------
    noteListWithNumbers:    [(str, int)]
                            A list of tuples whose 0th index are elements of
                            `noteList` and 1th index are their number based on
                            clock diagram.

    Returns
    -------
    methodsNumbers:         {int: [int]}
                            A dictionary of methods, connecting range(24) to
                            rows and columns of the generated matrix. Number 0
                            to 11 are for rows and then 12 to 23 are for columns

    See Also
    --------
    generateMatrix(noteListWithNumbers), leftToRight(matrix), upToDown(matrix)
    """
    methodsNumbers = {}
    matrix = generateMatrix(noteListWithNumbers)
    rows = leftToRight(matrix)
    columns = upToDown(matrix)
    for arrayCount in range(12):
        methodsNumbers[arrayCount] = rows[arrayCount]
        methodsNumbers[arrayCount + 12] = columns[arrayCount]
    return methodsNumbers


def acquireNormalNoteRow():
    """
    Asks the user to give a note row instead of randomly generating it.

    Inputs
    ------
    normalNoteRow:          str
                            A random permutation of NORMAL_UNIVERSE separated by
                            comma (,)

    Returns
    -------
    normalNoteRow:          [str]
                            An ordered list of a permutation of NORMAL_UNIVERSE

    See Also
    --------
    isNormalNoteRowValid(normalNoteRow)
    """
    normalNoteRow = None
    while not isNormalNoteRowValid(normalNoteRow):
        normalNoteRow = str(raw_input("Enter a note row (with 12 members). " +
                                      "They should be separated by a comma (," +
                                      ")and only # as accidental e.g.\nA,A#,C" +
                                      ",C#,B,G,G#,F#,E,F,D#,D\nYour note " +
                                      "row? "))
        normalNoteRow = filter(None, normalNoteRow.replace(" ", "").split(','))
        print "\nSo your note key is: {}\n".format(normalNoteRow)
        time.sleep(2)
    return normalNoteRow


def isNormalNoteRowValid(normalNoteRow):
    """
    Checks to see whether the given permutation of NORMAL_UNIVERSE is valid.

    Parameters
    ----------
    normalNoterow:          [str]
                            An ordered list of a permutation of NORMAL_UNIVERSE

    Returns
    -------
    Bool:                   True    if for all elements of `normalNoteRow`,
                                    element is in NORMAL_UNIVERSE
                            False   if not True
    """
    if normalNoteRow is None:
        return False
    if len(normalNoteRow) > 12:
        print "Too many notes found. Number of notes should be 12."
        return False
    elif len(normalNoteRow) < 12:
        print "Too few notes found. Number of notes should be 12."
        return False
    for normalNote in normalNoteRow:
        if normalNote not in NORMAL_UNIVERSE:
            print "Invalid Note Found!"
            return False
    if len(normalNoteRow) != len(set(normalNoteRow)):
        print "Duplicate notes found!"
        return False
    return True


def normalize(fileXml):
    """
    Only sharps are being used in this program, so gets rid
    of all accidentals that are not #.

    Parameters
    ----------
    fileXml:            str
                        Absolute path to the MusicXML file.

    Returns
    -------
    normalizedFileXml:  str
                        Absolute path to the normalized fileXml

    See Also
    --------
    DataToolbox.pathHandler(filePath), DataToolbox.config(),
    DataToolbox.fileCounter(fileName, choice, addenda),
    etree.parse(fileXml), etree.write(fileXml)
    """
    fileXmlName = DataToolbox.pathHandler(fileXml)[1]
    srcParentDir = DataToolbox.config()[-1]
    counter = DataToolbox.fileCounter(fileXmlName, "xml", "_Normalized-")
    tree = etree.parse(fileXml)
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
                            for otherSubnote in note:
                                if otherSubnote.tag != "accidental":
                                    if otherSubnote.text != "sharp":
                                        note.remove(otherSubnote)
    normalizedFileXml = "{}/data/XML/{}_Normalized-{}.xml".format(srcParentDir,
                                                                  fileXmlName,
                                                                  counter)
    tree.write(normalizedFileXml)
    return normalizedFileXml


def numberOfNotes(fileXml):
    """
    Counts the total number of notes in a file by reading it line by line and
    counting how many "<step" does it find (<step> is the beginning of a note
    tag)

    Parameters
    ----------
    fileXml:        str
                    Absolute path to MusicXML file

    Returns
    -------
    total:          int
    """
    total = 0
    with open(fileXml, 'r') as f:
        lines = f.readlines()
    for element in lines:
        if "<step" in element:
            total += 1
    return total
