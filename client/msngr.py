# Author      : Tom McDowell
# Version     : 1.0.0.12
# 
# Description : MSNGR is a open source basic end-to-end encrypted messenger completely written in python, using simple first time setup
# Requires    : M2Crypto required, openSSL sockets are required.

#        msngr_msgs = {
#            "welcome": "Welcome to MSNGR\n{}".format(msngr_msgs["version"]),
#            "version": "Version: 1.0.0.12"
#            }

try:
    import M2Crypto
    import threading
    import socket
    import pickle
    from ast import literal_eval
except:
    print """
          [!] MSNGR Requirements not met. please install:\n
              
              - M2Crypto  (Available on python-pip2)
              - threading (Pretty sure you should have this?)
              - ast       (Available on python-pip2)\n
          """

def encryptMessage(message, keyid):
    #sends a message to the connected server for distribution
    try:
        msg = config.config['nick'] + " | " + message
        key = config.publist[keyid]
        bio = M2Crypto.BIO.MemoryBuffer(key)
        rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        encryptedMessage = (rsa.public_encrypt(msg, M2Crypto.RSA.pkcs1_oaep_padding)).encode("base64")
        del rsa, bio
        return "{}::{}".format(keyid, encryptedMessage)
    except Exception as e:
        print "encryptMessage()\nAn Error Occurred:\n" + str(e)

def decryptMessage(message):
    try:
        if "::" not in message:
            rsa = M2Crypto.RSA.load_key_string(open(config.config["private_location"],"r").read())
            decryptedMessage = rsa.private_decrypt(message.decode("base64"), M2Crypto.RSA.pkcs1_oaep_padding)
            del rsa
            return decryptedMessage
    except Exception as e:
        if config.debug:
            print "decryptMessage()\nAn Error Occurred:\n" + str(e)


def listener():
    import hashlib
    import pickle
    md5 = hashlib.md5()
    md5.update(open(config.config['public_location'], "rb").read())

    #print "Starting listener..."
    while config.chatstatus:
        try:
            data = config.sock.recv(4096)
            if config.debug:
                print """
                \r----- RECEIVED ----
                \r{}
                \r-----   END    ----
                """.format(repr(data))
            if "::" in data:
                key, value = data.split("::")
                if key == "active_users":
                    config.publist = pickle.loads(value)
                    if config.debug:
                        print "Updated Active users..."
            else:
                #print "Attempting to decrypt message> " + data
                print decryptMessage(data)
        except Exception as e:
            if config.debug:
                print "[!] Listener() Error: \n{}".format(str(e))

def hasher(key):
    import hashlib
    md5 = hashlib.md5()
    md5.update(key)
    return md5.hexdigest()

def testPrivateKey(key_location):
    try:
        rsa = M2Crypto.RSA.load_key_string(open(config.config["private_location"],"r").read())
        del rsa
    except:
        print """
              \r[!] Error
              \r    Unable to load private key. Is the location correct in msngr.conf?\n
              \r    Error: {}\n
              \r    Current Setting: {}\n
              """.format(str(e), config.config['private_location'])
        exit()


def testPublicKey(key_location):
    try:
        key = open(config.config['public_location'], "rb").read()
        bio = M2Crypto.BIO.MemoryBuffer(key)
        rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        del key, bio, rsa
    except Exception as e:
        print """
              \r[!] Error
              \r    Unable to load public key. Is the location correct in msngr.conf?\n
              \r    Error: {}\n
              \r    Curent Setting: {}\n
              """.format(str(e), config.config['public_location'])
        exit()


class configClass():
    def __init__(self):
        import hashlib
        self.chatstatus = False
        self.config = {}
        self.publist = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.debug = False 
        try:
            configFile = open("msngr.conf", "r").read().strip().split("\n")

            for value in configFile:
                var1, var2 = value.split(":")
                self.config[var1] = var2
            
        except:
            print """
                  \n
                  \r[!] Configuration File Error
                  \r
                  \r    Please check that a msngr.conf file is in the same location as msngr.py
                  \r    Download default config file here: http://invalidpanda.xyz/MSNGR/msngr.conf
                  """
        md5 = hashlib.md5()
        md5.update(open(self.config['public_location'], "rb").read())
        self.myid = md5.hexdigest()
        print "My ID: {}".format(self.myid)

#  print msngr_msgs["welcome"]
config = configClass()
msngr = True
import threading
while msngr:

    print "[+] Importing settings from msngr.conf"
    testPublicKey(config.config['public_location'])
    testPrivateKey(config.config['private_location'])
    print "[+] Keys imported successfully."

    io = raw_input("[+] Connect to Server?\n[y/n]>")
    if io[:1] == "y":
        rhost, rport = raw_input("\r\nExample: 0.0.0.0:00000\n>").split(":")
        config.sock.connect((rhost, int(rport)))
        config.chatstatus = True

        print config.sock.recv(1024)
        config.sock.sendall(open(config.config['public_location'],"rb").read())
        print "Sent public key"
        print "Waiting for public keys from server..."
        config.sock.send("request::active_users")
        activeList = config.sock.recv(8192).split("::")
        if config.debug:
            print repr(activeList)
        config.publist = pickle.loads(activeList[1])
        print "Setup complete. Welcome to the chat!"
        print "Starting Listener..."
        t = threading.Thread(target=listener, args=())
        t.setDaemon(1)
        t.start()

    else:
        exit()

    while config.chatstatus:
        # config.sock.sendall("request::active_users")
        message = raw_input("[{}]> ".format(config.config['nick']))
        for keyid in config.publist:
            if keyid != config.myid:
                encMsg = encryptMessage(message, keyid)
                if config.debug:
                    print encMsg
                config.sock.sendall(encMsg)
        if config.debug:
            print len(config.publist)

        
