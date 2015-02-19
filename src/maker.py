# Needs to check whether xml is valid musicxml

import os
import subprocess
import ConfigParser

needToChangeFormats = frozenset(["mxl", "mscz"])

configParser = ConfigParser.RawConfigParser()
configFilePath = r'../config.txt'
configParser.read(configFilePath)
MUSESCORE = configParser.get('System', 'MUSESCORE_PATH')


def Main(filePath, fileName, choice, addenda=""):
    p = subprocess.Popen(str(MUSESCORE + " " + filePath + " -o ../data/" +
                             choice.upper() + "/" + fileName + addenda + "." +
                             choice), shell=True)
    p.communicate()
    if not os.path.exists(str("../data/" + choice.upper() + "/" +
                              fileName + addenda + "." + choice)):
        print "*****************************************************"
        print str("* Something went wrong. Your " + choice +
                  " was not generated. *")
        print "*****************************************************"
        return False
