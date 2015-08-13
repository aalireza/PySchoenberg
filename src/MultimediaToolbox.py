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


import DataToolbox
import os
import subprocess


MUSESCORE_NOT_XML_FORMATS = frozenset(["mxl", "MXL", "MSCZ", "mscz"])
MUSESCORE_FORMATS = frozenset(["xml", "XML"]) | MUSESCORE_NOT_XML_FORMATS
AUDIVERIS_FORMATS = frozenset(["pdf", "PDF", "jpg", "JPG", "JPEG", "jpeg"])
ALLOWED_FORMATS = MUSESCORE_FORMATS | AUDIVERIS_FORMATS


def MusescoreConvertor(initialFile, choice, addenda):
    """
    Parameters
    ----------
    initialFile:    str
                    Absolute path of initialFile
    choice:         str
                    One of "xml" or "wav" or "pdf"

    Result
    ------
    finalFilePath:  str
                    Absolute path to the converted file

    See Also
    --------
    AudiverisConvertor(initialFile, addenda)
    """
    musescoreLocation = DataToolbox.config()[0]
    srcParentDir = DataToolbox.config()[-1]
    fileName = DataToolbox.pathHandler(initialFile)[1]
    finalFilePath = "{}/data/{}/{}{}.{}".format(srcParentDir, choice.upper(),
                                                fileName, addenda,
                                                choice.lower())
    script = "{} {} -o {}".format(musescoreLocation, initialFile, finalFilePath)
    subprocess.Popen(script, shell=True).communicate()
    if not os.path.exists(finalFilePath):
        print "*****************************************************"
        print str("* Something went wrong. Your " + choice +
                  " was not generated. *")
        print "*****************************************************"
        return False
    return finalFilePath


def MusescoreMain(initialFile, choice, addenda):
    """
    It's the function that handles the conversion. It'll count how many times
    a file with same name and addenda has been produced in the directory and
    then writes a new one with a new name.

    Parameters
    ----------
    initialFile:            str
                            Absolute path of initialFile
    choice:
                            str
                            One of "wav", "xml" or "pdf"
    addenda:                str
                            It will be added to the end of file name e.g.
                            _Converted-

    Returns
    -------
    resultMusescorePath:    str
                            Absolute path of the converted file

    SeeAlso
    -------
    MusescoreConvertor(initialFile, choice, addenda),
    AudiverisMain(initialFile, addenda)
    """
    resultMusescorePath = MusescoreConvertor(initialFile, choice, addenda)
    return resultMusescorePath


def AudiverisConvertor(initialFile, addenda):
    """
    Converts a jpg or pdf to MusicXML using Audiveris

    Parameters
    ----------
    initialFile:        str
                        Absolute path of initialFile
    addenda:            str
                        It will be added to the end of file name e.g.
                        _Converted-

    Returns
    -------
    finalFilePath       str
                        Absolute path to the converted file

    See Also
    --------
    MusescoreConvertor(initialFile, choice, addenda)
    """
    audiverisLocation = DataToolbox.config()[1]
    srcParentDir = DataToolbox.config()[-1]
    fileName = DataToolbox.pathHandler(initialFile)[1]
    finalFilePath = "{}/data/XML/{}{}.xml".format(srcParentDir, fileName,
                                                  addenda)
    script = "{} -batch -input {} -export {}".format(audiverisLocation,
                                                     initialFile,
                                                     finalFilePath)
    subprocess.Popen(script, shell=True).communicate()
    if not os.path.exists(finalFilePath):
        print "**********************************************************"
        print "* Something went wrong. Your MusicXML was not generated. *"
        print "**********************************************************"
        return False
    return finalFilePath


def AudiverisMain(initialFile, addenda):
    """
    It's the function that handles the conversion. It'll count how many times
    a file with same name and addenda has been produced in the directory and
    then writes a new one with a new name.

    Parameters
    ----------
    initialFile:            str
                            Absolute path of initialFile
                            One of "wav", "xml" or "pdf"
    addenda:                str
                            It will be added to the end of file name e.g.
                            _Converted-

    Returns
    -------
    resultMusescorePath:    str
                            Absolute path of the converted file

    See Also
    --------
    AudiverisConvertor(initialFile, addenda),
    MusescoreMain(initialFile, choice, addenda)
    """
    resultAudiverisPath = AudiverisConvertor(initialFile, addenda)
    return resultAudiverisPath


def run(player, filePath):
    """
    Run's a shell command to open up the file. If it's a .wav then play it or
    if it's a .pdf then open a pdf reader etc.

    Parameters
    ----------
    player:         str
                    Absolute path of the player. It should be in config.txt file
                    which will be derived using DataToolbox.config()
    filePath:       str
                    Absolute path of the file

    See Also
    --------
    DataToolbox.config()
    """
    subprocess.Popen("{} {}".format(player, filePath), shell=True).communicate()


def Main(initialFile, addenda, choice, shouldRunIt=True):
    """
    The main function that'll be called from `main.py`. Everything in this
    program must eventually be in MusicXML. It checks the format to see whether
    it's a pdf or jpg to need optical music recognition in order to be converted
    to xml or not. If it is, then calls Audiveris and then calls Musescore to
    either play it as .wav or .pdf or leave at .xml. If there's no need for
    Audiveris, it calls Musescore directly.

    Parameters
    ----------
    initialFile:        str
                        Absolute path of initialFile
    addenda:            str
                        It will be added to the end of file name e.g._Converted-
    choice:             str
                        One of "wav" or "pdf" or "xml" (if "xml", the
                        `shouldRunIt` must be False)
    shouldRunIt:        Bool
                        True    if user wishes to run the result.
                        False   if either user don't wishes to play the result
                                or this function is called inside another
                                function which needs the absolute path of the
                                converted file to do further processing on it

    Returns
    -------
    finalFilePath:      str
                        Absolute path to the converted file. Will be returned if
                        shouldRunIt is False

    Raises
    ------
    SystemExit          if shouldRunIt is True
                        will be raised after running the file

    Seel Also
    ---------
    DataToolbox.config(),
    DataToolbox.addendaHandler(addenda, choice, fileFormat)
    AudiverisMain(initialFile, addenda),
    MusescoreMain(initialFile, choice, addenda)
    """
    (musescoreLocation, audiverisLocation, pdfPlayer, wavPlayer,
     srcParentDir) = DataToolbox.config()
    fileName, fileFormat = DataToolbox.pathHandler(initialFile)[1:]
    addendaAudiveris, addendaMusescore = DataToolbox.addendaHandler(addenda,
                                                                    choice,
                                                                    fileFormat)
    finalFilePath = None
    if fileFormat in ALLOWED_FORMATS:
        if fileFormat in AUDIVERIS_FORMATS:
            semiFinalFilePath = AudiverisMain(initialFile, addendaAudiveris)
            semiFinalFileName = DataToolbox.pathHandler(semiFinalFilePath)[1]
            finalFilePath = MusescoreConvertor(semiFinalFilePath, choice,
                                               addendaMusescore)
        elif fileFormat in MUSESCORE_FORMATS:
            finalFilePath = MusescoreMain(initialFile, choice, addendaMusescore)
    if shouldRunIt:
        if os.path.exists(finalFilePath):
            # if shouldRunIt, then choice is either `wav` or `pdf` and the
            # location of the player is within variables pdfPlayer or wavPlayer.
            # Below calls the the appropiate variable local to the function
            # based on its string name.
            run(locals()["{}Player".format(choice.lower())], finalFilePath)
            raise SystemExit
    elif not shouldRunIt:
        return finalFilePath


def decide(filePath):
    """
    This function will be called in context of larger functions like
    AtonalizerMain or EncryptAndEncodeMain for the user to decide what to do
    with the result.

    Parameters
    ----------
    filePath:           str
                        Absolute Path to the file

    Raises
    ------
    SystemExit:         If the user decides to do nothing with the file

    See Also
    --------
    Main(initialFile, addenda, choice, shoultRunIt)
    """
    decision = None
    while decision not in set(['p', 'v', 'n']):
        decision = str(raw_input("\nWhat do you want to do with the atonaliz" +
                                 "ed version of the File? (p)lay or (v)iew" +
                                 " it as PDF or (n)othing and just save the " +
                                 "file:\n{}\nYour choice: ".format(filePath)))
    if decision == 'p':
        Main(filePath, "_Converted-", "wav")
    elif decision == 'v':
        Main(filePath, "_Converted-", "pdf")
    elif decision == 'n':
        raise SystemExit
