# Author      : Tom McDowell
# Version     : 1.0.0.1
# 
# Description : MSNGR is a open source basic end-to-end encrypted messenger completely written in python, using simple first time setup
# Requires    : M2Crypto required, openSSL sockets are required.

import M2Crypto

def sendMessage():
    return True

def createKeys():
    return True

def hostServer():
    return True

class configClass(self):
    def __init__(self):
        
        self.config = {}
        try:
            configFile = open("msngr.conf", "r").read().split("\n")
        except:
            print """
                  [!] Configuration File Error: Not found.
                  Download default config file here: http://invalidpanda.xyz/MSNGR/msngr.conf
                  """
        
        for setting in configFile:
            settingname, settingdetail = setting.split(":")
            self.config[settingname] = settingdetail

