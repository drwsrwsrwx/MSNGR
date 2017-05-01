# Author      : Tom McDowell
# Version     : 1.0.0.2
# 
# Description : MSNGR is a open source basic end-to-end encrypted messenger completely written in python, using simple first time setup
# Requires    : M2Crypto required, openSSL sockets are required.

try:
    import M2Crypto
    import threading
    from ast import literal_eval
except:
    print """
          [!] MSNGR Requirements not met. please install:\n
              
              - M2Crypto (Available on python-pip2)
              - ast      (Available on python-pip2)
          """

def sendMessage():
    #sends a message to the connected server for distribution
    return True

def startServer():
    return True

def hostServer():
    # hosts a server for msngr clients.
    return True

def connectServer():
    # sends public key to server, for distribution.
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

