# Need to be shrinked up. Boring stuff though, dealing with files in a
# directory...!

import aes
import atonalize
import basicMusic
import implementerAES
import implementerAtonal
import maker
import scanner
import argparse
import ConfigParser
import getpass as gt
import os
import subprocess
import time

allowedFormats = frozenset(["pdf", "jpg", "jpeg", "JPG", "JPEG", "xml", "mxl",
                            "mscz"])

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config.txt'
configParser.read(configFilePath)
PLAYER = configParser.get('System', 'PLAYER_PATH')
PDF = configParser.get('System', 'PDF_VIEWER')


def argumentHandling():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--targetFile", required=True,
                        help="The absolute path to your file", type=str)
    parser.add_argument("-r", "--reset", help="Remove everything in ../data/*",
                        action="store_true")
    args = parser.parse_args()
    if args.reset:
        subprocess.call("rm -i ../data/*/*", shell=True)
    if not os.path.exists(args.targetFile):
        print "File does not exist."
        raise SystemExit
    fileFullName = os.path.basename(args.targetFile)
    fileName = '.'.join(fileFullName.split('.')[:-1])
    fileFormat = fileFullName.split('.')[-1]
    filePath = os.path.abspath(args.targetFile).strip(fileFullName)
    if fileFormat not in allowedFormats:
        print "Invalid file format"
        raise SystemExit
    return (args.targetFile, fileFullName, fileName, fileFormat, filePath)


if __name__ == '__main__':
    f = argumentHandling()
    while f is not None:
        command = str(raw_input("Enter your command (Enter 'h' for help): "))
        if command is 'h':
            print ("a: Atonalize the musical sheet.")
            print ("e: Encrypt a message with AES128 and encode it within a " +
                   "musical sheet.")
            print ("d: Decrypt a message which is encrypted with AES128 by " +
                   "decoding its musical sheet. (Must have the two keys)")
            print ("p: Play the file by converting it to WAV")
            print ("v: View the sheet music of the file (Only works on xml, " +
                   "mxl and mscz files)")
            print ("r: Reset to default and remove everything in ../data/*")
            print ("h: Help")
            print ("q: Quit")

        elif command is 'q':
            break

        elif command is 'r':
            subprocess.call("rm -i ../data/*/*", shell=True)

        elif command is 'p':
            counter = None
            if not os.path.exists("../data/XML"):
                os.makedirs("../data/XML/")
            if not os.path.exists("../data/WAV"):
                os.makedirs("../data/WAV/")
            if f[3] in allowedFormats:
                if f[3] in scanner.allowedFormats:
                    counterScan = 0
                    while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                         str(counterScan) + ".xml"):
                        counterScan += 1
                    scanner.Main(f[0], f[2], str("_Converted-" +
                                                 str(counterScan)))
                    maker.Main(filePath=str("../data/XML/" +
                                            str(f[2] + "_Converted-" +
                                                str(counterScan)) + ".xml"),
                               fileName=f[2], choice="wav",
                               addenda=str("_Converted-" + str(counterScan)))
                    counter = counterScan
                else:
                    counterMake = 0
                    while os.path.exists("../data/WAV/" + f[2] + "_Converted-" +
                                         str(counterMake) + ".wav"):
                        counterMake += 1
                    maker.Main(f[0], f[2], "wav", str("_Converted-" +
                                                      str(counterMake)))
                    counter = counterMake
            elif f[3] not in allowedFormats:
                if f[3] == "wav" or f[3] == "ogg" or f[3] == "mp3":
                    print "It is already in an audio format."
                    raise SystemExit
                else:
                    print "Format not allowed."
                    raise SystemExit
            time.sleep(1)
            if os.path.exists(str("../data/WAV/" + f[2] + "_Converted-" +
                                  str(counter) + ".wav")):
                subprocess.call(str(PLAYER + " ../data/WAV/" + f[2] +
                                    "_Converted-" + str(counter) + ".wav"),
                                shell=True)
            else:
                print "The .wav file is not present in ../data/WAV/"
                raise SystemExit

        elif command is 'v':
            if not os.path.exists("../data/PDF"):
                os.makedirs("../data/PDF/")
            if f[3] in scanner.allowedFormats:
                print ("It is already in a format capable of representing it " +
                       "with visible/readale notes.")
                raise SystemExit
            if f[3] in maker.needToChangeFormats or f[3] == "xml":
                counterMake = 0
                while os.path.exists(str("../data/PDF/" + f[2] + "_Converted-" +
                                         str(counterMake) + ".pdf")):
                    counterMake += 1
                maker.Main(f[0], f[2], "pdf", str("_Converted-" +
                                                  str(counterMake)))
            else:
                print "Format not allowed."
                raise SystemExit
            time.sleep(1)
            subprocess.call(str(PDF + " ../data/PDF/" + f[2] +
                                "_Converted-" + str(counterMake) + ".pdf"),
                            shell=True)

        elif command is 'a':
            # Atonalizer
            scanFlag = None
            makeFlag = None
            counter = 0
            midcounter = 0
            if not os.path.exists("../data/XML"):
                os.makedirs("../data/XML/")
            if f[3] in scanner.allowedFormats:
                counterScan = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterScan) + ".xml"):
                    counterScan += 1
                scanner.Main(f[0], f[2], str("_Converted-" + str(counterScan)))
                scanFlag = True
                midcounter = counterScan
            elif f[3] in maker.needToChangeFormats:
                counterMake = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterMake) + ".xml"):
                    counterMake += 1
                maker.Main(f[0], f[2], "xml", str("_Converted-" +
                                                  str(counterMake)))
                makeFlag = True
                midcounter = counterMake
            while os.path.exists("../data/XML/" + f[2] + "_Atonalized-" +
                                 str(counter) + ".xml"):
                counter += 1
            if scanFlag or makeFlag:
                implementerAtonal.implementer(atonalize.rand12(),
                                              str(f[2] + "_Converted-" +
                                                  str(midcounter) + ".xml"),
                                              addenda=str("_Atonalized-" +
                                                          str(counter)))
            elif not scanFlag and not makeFlag:
                implementerAtonal.implementer(atonalize.rand12(), f[1],
                                              readPath=f[4],
                                              addenda=str("_Atonalized-" +
                                                          str(counter)))

            choice = None
            while choice not in set(['p', 'v', 'n']):
                choice = str(raw_input("\nWhat do you want to do with the " +
                                       "atonalized version? (p)lay or (v)iew " +
                                       "its PDF or (n)othing and just save " +
                                       "the xml file inside ../data/XML\n" +
                                       "Your choice: "))
            if choice is 'p':
                counterP = 0
                if not os.path.exists("../data/WAV"):
                    os.makedirs("../data/WAV/")
                while os.path.exists("../data/WAV/" + f[2] + "_Atonalized-"
                                     + str(counterP) + ".wav"):
                    counterP += 1
                if scanFlag or makeFlag:
                    maker.Main(str("../data/XML/" + f[2] + "_Converted-" +
                                   str(midcounter) + "_Atonalized-" +
                                   str(counter) + ".xml"), f[2], "wav",
                               addenda=str("_Atonalized-" + str(counterP)))
                elif not scanFlag and not makeFlag:
                    maker.Main(str("../data/XML/" + f[2] + "_Atonalized-" +
                                   str(counter) + ".xml"), f[2], "wav",
                               addenda=str("_Atonalized-" + str(counterP)))
                subprocess.call(str(PLAYER + " ../data/WAV/" + f[2] +
                                    "_Atonalized-" + str(counterP) + ".wav"),
                                shell=True)

            elif choice is 'v':
                counterV = 0
                if not os.path.exists("../data/PDF"):
                    os.makedirs("../data/PDF/")
                while os.path.exists("../data/PDF/" + f[2] + "_Atonalized-"
                                     + str(counterV) + ".pdf"):
                    counterV += 1
                if scanFlag or makeFlag:
                    maker.Main(str("../data/XML/" + f[2] + "_Converted-" +
                                   str(midcounter) + "_Atonalized-" +
                                   str(counter) + ".xml"), f[2], "pdf",
                               addenda=str("_Atonalized-" + str(counterV)))
                elif not scanFlag and not makeFlag:
                    maker.Main(str("../data/XML/" + f[2] + "_Atonalized-" +
                                   str(counter) + ".xml"), f[2], "pdf",
                               addenda=str("_Atonalized-" + str(counterV)))
                subprocess.call(str(PDF + " ../data/PDF/" + f[2] +
                                    "_Atonalized-" + str(counterV) + ".pdf"),
                                shell=True)

            elif choice is 'n':
                break

        elif command is 'e':
            # Encoder & Encrypter
            your_message = str(raw_input("What is your message? "))
            your_key = gt.getpass("What is your encryption key? ")
            note_key = str(raw_input(str("What is your 12-note encoding key? " +
                                         "Should be separated with a comma " +
                                         "(,) and only # as accidental i.e. " +
                                         "A,A#,C,C#,B,G,G#,F#,E,F,D#,D\n" +
                                         "Your key? ")))
            note_key = note_key.strip().replace(" ", "").split(",")
            for element in note_key:
                if element is "":
                    del note_key[note_key.index(element)]
            changeflag = None
            for i in range(len(note_key)):
                tempnote = note_key[i]
                while tempnote not in basicMusic.normal_universe:
                    print("You've entered " + str(note_key) + " which has " +
                          str(element) + " in it which is not part of valid " +
                          " notes. Valid notes are: " +
                          str(basicMusic.normal_universe))
                    tempnote = str(raw_input("Enter a valid note instead: "))
                    changeflag = True
                if changeflag:
                    note_key[i] = tempnote
            if changeflag:
                print ("So your note key is: " + str(note_key))
            your_cipher = aes.encrypt(your_message, your_key)
            print ("Encryption successful. Now encoding...")
            time.sleep(1)
            scanFlag = None
            makeFlag = None
            counter = 0
            midcounter = 0
            if not os.path.exists("../data/XML"):
                os.makedirs("../data/XML/")
            if not os.path.exists("../data/AES/"):
                os.makedirs("../data/AES/")
            if f[3] in scanner.allowedFormats:
                counterScan = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterScan) + ".xml"):
                    counterScan += 1
                scanner.Main(f[0], f[2], str("_Converted-" + str(counterScan)))
                scanFlag = True
                midcounter = counterScan
            elif f[3] in maker.needToChangeFormats:
                counterMake = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterMake) + ".xml"):
                    counterMake += 1
                maker.Main(f[0], f[2], "xml", str("_Converted-" +
                                                  str(counterMake)))
                makeFlag = True
                midcounter = counterMake
            while os.path.exists("../data/AES/" + f[2] + "_AES-" +
                                 str(counter) + ".xml"):
                counter += 1
            if scanFlag or makeFlag:
                z = implementerAES.encoder(your_cipher, note_key,
                                           str(f[2] + "_Converted-" +
                                               str(midcounter) + ".xml"),
                                           addenda=str("_AES-" + str(counter)))
            elif not scanFlag and not makeFlag:
                z = implementerAES.encoder(your_cipher, note_key, f[1],
                                           addenda=str("_AES-" + str(counter)),
                                           readPath=f[4])
            if z is False:
                raise SystemExit

            choice = None
            while choice not in set(['p', 'v', 'n']):
                choice = str(raw_input("\nWhat do you want to do with the " +
                                       "encoded file? (p)lay or (v)iew " +
                                       "its PDF or (n)othing and just save " +
                                       "the xml file inside ../data/AES with " +
                                       "the same name as the current file " +
                                       "except an 'AES' added to the end\n" +
                                       "Your choice: "))
            if choice is 'p':
                counterP = 0
                if not os.path.exists("../data/WAV"):
                    os.makedirs("../data/WAV")
                if scanFlag or makeFlag:
                    while os.path.exists("../data/WAV/" + f[2] + "_AES-" +
                                         str(counterP) + ".wav"):
                        counterP += 1
                    maker.Main(str("../data/AES/" + f[2] + "_Converted-" +
                                   str(midcounter) + "_AES-" + str(counter) +
                                   ".xml"), f[2], "wav",
                               addenda=str("_AES-" + str(counterP)))
                elif not scanFlag and not makeFlag:
                    while os.path.exists("../data/WAV/" + f[2] + "_AES-" +
                                         str(counterP)):
                        counterP += 1
                    maker.Main(str("../data/AES/" + f[2] + "_AES-" +
                                   str(counter) + ".xml"), f[2], "wav",
                               addenda=str("_AES-" + str(counterP)))
                subprocess.call(str(PLAYER + " ../data/WAV/" + f[2] + "_AES-" +
                                    str(counterP) + ".wav"), shell=True)

            elif choice is 'v':
                counterV = 0
                if not os.path.exists("../data/PDF"):
                    os.makedirs("../data/PDF")
                while os.path.exists("../data/PDF/" + f[2] + "_AES-"
                                     + str(counterV) + ".pdf"):
                    counterV += 1
                if scanFlag or makeFlag:
                    maker.Main(str("../data/AES/" + f[2] + "_Converted-" +
                                   str(midcounter) + "_AES-" + str(counter) +
                                   ".xml"), f[2], "pdf",
                               addenda=str("_AES-" + str(counterV)))
                elif not scanFlag and not makeFlag:
                    maker.Main(str("../data/AES/" + f[2] + "_AES-" +
                                   str(counter) + ".xml"), f[2], "pdf",
                               addenda=str("_AES-" + str(counterV)))
                subprocess.call(str(PDF + " ../data/PDF/" + f[2] +
                                    "_AES-" + str(counterV) + ".pdf"),
                                shell=True)
            elif choice is 'n':
                pass
            break

        elif command is 'd':
            your_key = gt.getpass("What is your encryption key? ")
            note_key = str(raw_input(str("What is your 12-note encoding key? " +
                                         "Should be separated with a comma " +
                                         "(,) and only # as accidental i.e. " +
                                         "A,A#,C,C#,B,G,G#,F#,E,F,D#,D\n" +
                                         "Your key? ")))
            note_key = note_key.strip().replace(" ", "").split(",")
            for element in note_key:
                if element is "":
                    del note_key[note_key.index(element)]
            changeflag = None
            for i in range(len(note_key)):
                tempnote = note_key[i]
                while tempnote not in basicMusic.normal_universe:
                    print("You've entered " + str(note_key) + " which has " +
                          str(element) + " in it which is not part of valid " +
                          " notes. Valid notes are: " +
                          str(basicMusic.normal_universe))
                    tempnote = str(raw_input("Enter a valid note instead: "))
                    changeflag = True
                if changeflag:
                    note_key[i] = tempnote
            if changeflag:
                print ("So your note key is: " + str(note_key))
            if not os.path.exists("../data/XML/"):
                os.makedirs("../data/XML/")
            scanFlag = None
            makeFlag = None
            midcounter = 0
            if f[3] in scanner.allowedFormats:
                counterScan = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterScan) + ".xml"):
                    counterScan += 1
                scanner.Main(f[0], f[2], str("_Converted-" + str(counterScan)))
                scanFlag = True
                midcounter = counterScan
            if f[3] in maker.needToChangeFormats:
                counterMake = 0
                while os.path.exists("../data/XML/" + f[2] + "_Converted-" +
                                     str(counterMake) + ".xml"):
                    counterMake += 1
                maker.Main(f[0], f[2], "xml", str("_Converted-" +
                                                  str(counterMake)))
                makeFlag = True
                midcounter = counterMake
            if scanFlag or makeFlag:
                your_cipher = implementerAES.decoder(note_key, f[2] +
                                                     "_Converted-" +
                                                     str(midcounter) + ".xml")
            elif not scanFlag and not makeFlag:
                your_cipher = implementerAES.decoder(note_key, f[1], f[4])
            print ("Your ciphertext is: " + your_cipher)
            try:
                message = aes.decrypt(your_cipher, your_key)
                print ("Your message is: " + message)
                break
            except:
                print ("Decryption unsuccessful.")
                break

        else:
            print "\nCommand not understood.\n"
