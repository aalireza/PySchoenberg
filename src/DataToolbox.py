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


import ConfigParser
import MultimediaToolbox
import os


def config():
    """
    Reads config.txt file and produces the argument for the directory containing
    source codes based on the location of this file i.e. __file__

    Returns
    -------
    MUSESCORE           str
    AUDIVERIS           str
    PDF                 str
    PLAYER              str
    srcParentDir        str
                        Absolute path to the directory containing src/

    See Also
    --------
    srcParentDir/config.txt
    """
    configParser = ConfigParser.RawConfigParser()
    srcDir = os.path.dirname(os.path.abspath(__file__))
    srcParentDir = os.path.dirname(srcDir)
    configFilePath = '{}/config.txt'.format(srcParentDir)
    configParser.read(configFilePath)
    MUSESCORE = configParser.get('System', 'MUSESCORE_PATH')
    AUDIVERIS = configParser.get('System', 'AUDIVERIS_PATH')
    PDF = configParser.get('System', 'PDF_VIEWER')
    PLAYER = configParser.get('System', 'PLAYER_PATH')
    return (MUSESCORE, AUDIVERIS, PDF, PLAYER, srcParentDir)


def pathHandler(filePath):
    """
    Parameters
    ----------
    filePath:       str
                    Absolute path of the file e.g. /home/alireza/test.py

    Returns
    -------
    fileBaseName:   str
                    Name of the file with format e.g. test.py
    fileName:       str
                    Name of the file e.g. test
    fileFormat:     str
                    Format of the file e.g. py
    """
    fileBaseName = os.path.basename(filePath)
    fileName = '.'.join(fileBaseName.split('.')[:-1])
    fileFormat = fileBaseName.split('.')[-1]
    return fileBaseName, fileName, fileFormat


def directoryCreator(srcParentDir):
    """
    Creates directories that are used by this program.

    Parameters
    ----------
    srcParentDir:       str
                        Absolute path of the directory containing src
    """
    if not os.path.exists("{}/data".format(srcParentDir)):
        os.makedirs("{}/data".format(srcParentDir))
    if not os.path.exists("{}/data/XML".format(srcParentDir)):
        os.makedirs("{}/data/XML".format(srcParentDir))
    if not os.path.exists("{}/data/WAV".format(srcParentDir)):
        os.makedirs("{}/data/WAV".format(srcParentDir))
    if not os.path.exists("{}/data/PDF".format(srcParentDir)):
        os.makedirs("{}/data/PDF".format(srcParentDir))
    if not os.path.exists("{}/data/AES".format(srcParentDir)):
        os.makedirs("{}/data/AES".format(srcParentDir))


def isDataEmpty(srcParentDir):
    """
    Checks to see whether srcParentDir/data/ is empty or not. If it is not empty
    --resetData in main.py will work to remove them.

    Parameters
    ----------
    srcParentDir:       str
                        Absolute path to the directory containing src/ and data/

    Returns
    -------
    Bool:               True    if no file is in data/ recursively
                        False   if not True
    """
    fileWalker = os.walk("{}/data/".format(srcParentDir))
    for currentDir, insideDirs, insideFiles in fileWalker:
        if len(insideFiles) != 0:
            return False
    return True


def fileCounter(fileName, choice, addenda):
    """
    Checks how many time the file with a name that'll be produced by another
    function exists in srcParentDir/data/*. Doesn't give back anything for
    empty addendas which are used for some mid level conversions.

    Parameters
    ----------
    fileName:       str
                    A file's name e.g. test in test.py
    choice:         str
                    Could be either 'wav' or 'pdf' or 'xml'. It'll be the format
                    of the file that'll be produced by another function and also
                    the data subdirectory that'll reside in.
    addenda:        str
                    What'll be added to the fileName to demonstrate and
                    distinguish the resultant file e.g. _Converted- or
                    _Atonalized- or _AES-.
    """
    srcParentDir = config()[-1]
    if addenda == "":
        counter = ""
    else:
        counter = 0
        while os.path.exists("{}/data/{}/{}{}{}.{}".format(srcParentDir,
                                                           choice.upper(),
                                                           fileName,
                                                           addenda,
                                                           counter,
                                                           choice.lower())):
            counter += 1
    return counter


def addendaHandler(addenda, choice, fileFormat):
    """
    This function will be used to give a percise name to the produced files.

    Parameters
    ----------
    addenda:            str
                        What'll already be added to the file name
    choice:             str
                        The target format, could be one of "wav", "pdf" or "xml"
    fileFormat:         str

    Returns
    -------
    addenda             str
                        If either the addenda is empty or not in form of
                        _Addenda-i where `i` is either an int or ''
    addendaAudiveris:   str
                        What'll be added to this file by Audiveris (will be
                        empty if Audiveris is not going to be used)
    Musescore:          str
                        What'll be added to this file by Musescore (will be
                        empty if Musescore is not going to be used)
    """
    if addenda == '':
        return addenda, addenda
    elif (addenda[-1] == '-' or (type(int(addenda[-1])) is int) and
          addenda[0] == '_'):
        if fileFormat in MultimediaToolbox.AUDIVERIS_FORMATS:
            addendaAudiveris = "{}2{}".format(addenda[:-1], "XML")
        elif fileFormat not in MultimediaToolbox.AUDIVERIS_FORMATS:
            addendaAudiveris = ""
        if choice != "xml":
            addendaMusescore = "{}2{}".format(addenda[:-1], choice.upper())
        elif choice == "xml":
            addendaMusescore = ""
        return addendaAudiveris, addendaMusescore
    else:
        print "{} is not standard an can't be properly handled.".format(addenda)
        return addenda, addenda
