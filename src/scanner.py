# Needs to check whether xml is valid musicxml

import os
import subprocess
import ConfigParser

allowedFormats = frozenset(["pdf", "PDF", "jpg", "jpeg", "JPG", "JPEG"])

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config.txt'
configParser.read(configFilePath)
AUDIVERIS = configParser.get('System', 'AUDIVERIS_PATH')


def Main(filePath, fileName, addenda="", writePath="../data/XML/"):
    p = subprocess.Popen(str(AUDIVERIS + " -batch -input " + filePath +
                             " -export " + writePath + fileName +
                             addenda + ".xml"), shell=True)
    p.communicate()
    if not os.path.exists("../data/XML/" + fileName + addenda + ".xml"):
        print "**********************************************************"
        print "* Something went wrong. Your MusicXML was not generated. *"
        print "**********************************************************"
        return False
