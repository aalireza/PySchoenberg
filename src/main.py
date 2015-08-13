"""
PySchoenberg
Twelve-Tonic Atonalizer and Encoder
Copyright (C) 2015  Alireza Rafiei

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, Version 2.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/> or write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA  02110-1301, USA.
"""


from pprint import pprint
import Atonalizer
import DataToolbox
import EncoderAndDecoder
import MultimediaToolbox
import argparse
import os
import subprocess


def argumentHandling(srcParentDir):
    """
    Parameters
    ----------
    srcParentDir:       str
                        Absolute path to the directory containing src/ and data/
                        and it's needed for the option --resetData

    Returns
    -------
    args.initialFile:   str
                        path to the initial file

    Raises
    ------
    SystemExit:         if initial file doesn't exit
                        if --resetData was used
                        if format of the file can't be handled i.e. it's not in
                           MultimediaToolbox.ALLOWED_FORMATS

    See Also
    --------
    DataToolbox.pathHandler(filePath),
    DataToolbox.isDataEmpty(srcParentDir)
    """
    parser = argparse.ArgumentParser(prog="PySchoenberg")
    argGroup = parser.add_mutually_exclusive_group(required=True)
    argGroup.add_argument("-f", "--initialFile",
                          help="The absolute path to your file",
                          type=str)
    argGroup.add_argument("-r", "--resetData",
                          help=("Reset to default and remove " +
                                "everything in {}/data/*".format
                                (srcParentDir)),
                          action='store_true')
    args = parser.parse_args()
    if args.resetData:
        if DataToolbox.isDataEmpty(srcParentDir):
            print "No file is currently inside {}/data/*".format(srcParentDir)
        else:
            decision = None
            while decision not in ['y', 'n']:
                decision = str(raw_input("Do you need to check the file befo" +
                                         "re removing them? If not, all of " +
                                         "them will be removed recursively " +
                                         "(y/n): "))
            if decision == 'y':
                subprocess.Popen("rm -i {}/data/*/*".format(srcParentDir),
                                 shell=True).communicate()
            elif decision == 'n':
                subprocess.Popen("rm -r {}/data/*/*".format(srcParentDir),
                                 shell=True).communicate()
        raise SystemExit
    if not os.path.exists(args.initialFile):
        print "File does not exist."
        raise SystemExit
    fileFormat = DataToolbox.pathHandler(args.initialFile)[2]
    if fileFormat not in MultimediaToolbox.ALLOWED_FORMATS:
        print "Invalid file format"
        raise SystemExit
    return args.initialFile


if __name__ == '__main__':
    srcParentDir = DataToolbox.config()[-1]
    initialFile = argumentHandling(srcParentDir)
    DataToolbox.directoryCreator(srcParentDir)
    commandList = [
        "a: Atonalize sheet music",
        ("e: Encrypt a message with AES128 and encode it within an atonaliz" +
         "ed sheet music"),
        ("d: Decrypt and decode an AES128 encrypted message that's encoded " +
         "within an atonalized sheet (Must have two keys)"),
        "p: Play the file by converting it to .wav",
        "v: View the sheet music as PDF (only works on xml, mxl and mscz)",
        "---",
        "h: Help",
        "q: Quit"
    ]
    while True:
        command = str(raw_input("Enter your command (Enter 'h' for help): "))
        if command is 'h':
            pprint(commandList)

        elif command is 'q':
            break

        elif command is 'p':
            MultimediaToolbox.Main(initialFile, "_Converted-", "wav")
            break

        elif command is 'v':
            MultimediaToolbox.Main(initialFile, "_Converted-", "pdf")
            break

        elif command is 'a':
            Atonalizer.Main(initialFile)
            break

        elif command is 'e':
            EncoderAndDecoder.EncryptAndEncodeMain(initialFile)
            break

        elif command is 'd':
            EncoderAndDecoder.DecodeAndDecryptMain(initialFile)
            break

        else:
            print "\nCommand not understood.\n"
