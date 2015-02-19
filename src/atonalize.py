import basicMusic
import random
from music21 import serial


def rand12():
    # Random permutation of 12 notes.
    allnote = basicMusic.universe[:]
    random.shuffle(allnote)
    return allnote


def numassign(note):
    # Generate numbers based on the first note following the clock diagram.
    # argument "note" is the first note of 12.
    allnote = basicMusic.universe[:]
    defclock = {}
    nclock = allnote[allnote.index(note):] + allnote[:allnote.index(note)]
    for i in range(12):
        defclock[nclock[i]] = i
    return defclock


def rand12wn(notelist):
    # Combine rand12 and numassign. Argument "notelist" is the randomly chosen
    # permutation of 12 notes i.e. rand12().
    clock = numassign(notelist[0])
    mainclock = []
    for i in range(12):
        mainclock.append((notelist[i], clock[notelist[i]]))
    return mainclock


def getnote(number, rand12wn):
    # Get note based on its number from clock diagram.
    for element in rand12wn:
        if number == element[1]:
            return element[0]


def getnumber(note, rand12wn):
    # Get number based on its note from clock diagram.
    for element in rand12wn:
        if note == element[0]:
            return int(element[1])


def genmatrix(randwn):
    # Generate the 12 tone matrix based on the numbers of randomly generated
    # 12 notes' from the clock diagram.
    numberlist = [randwn[i][1] for i in range(12)]
    matrix = serial.rowToMatrix(map(int, numberlist))
    return matrix


def lr(m):
    # Read rows from left to right on the 12 tone matrix.
    temp = m.split('\n')
    main = []
    for i in range(12):
        main.append(temp[i].split())
    for i in range(12):
        for j in range(12):
            main[i][j] = int(main[i][j])
    return main


def ud(m):
    # Read columns from up to down on the 12 tone matrix.
    temp = lr(m)
    main = []
    for i in range(12):
        tempmain = []
        for j in range(12):
            tempmain.append(int(temp[j][i]))
        main.append(tempmain)
    return main


def methods(rowwn, num):
    # Generate enough numbers by randomly picking methods from the 12 tone
    # matrix to fill up all the music sheet. Argument @num here refers to the
    # number of notes in the musical sheet which should determined via
    # basicMusic.numnotes(xmlfile)
    noterow = rowwn[:]
    notematrix = genmatrix(noterow)
    methodlist = [lr, ud]
    numberlist = [getnumber(notetuple[0], noterow) for notetuple in noterow]
    upperlimit = (num/12) + 1
    steps = 0
    while steps <= upperlimit:
        newnumberlist = (random.choice(methodlist)(notematrix)
                         [random.randint(0, 11)])
        numberlist += newnumberlist
        steps += 1
    return numberlist
