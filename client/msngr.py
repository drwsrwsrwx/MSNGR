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
    from ast import literal_eval
except:
    print """
          [!] MSNGR Requirements not met. please install:\n
              
              - M2Crypto  (Available on python-pip2)
              - threading (Pretty sure you should have this?)
              - ast       (Available on python-pip2)\n
          """

def encryptMessage(message):
    #sends a message to the connected server for distribution
    try:
        key = open(config.config["public_location"],"rb").read()
        bio = M2Crypto.BIO.MemoryBuffer(key)
        rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        encryptedMessage = (rsa.public_encrypt(message, M2Crypto.RSA.pkcs1_oaep_padding)).encode("base64")
        del rsa, bio
        return encryptedMessage
    except Exception as e:
        print "An Error Occurred:\n" + e

def decryptMessage(message):
    try:
        rsa = M2Crypto.RSA.load_key_string(open(config.config["private_location"],"r").read())
        decryptedMessage = rsa.private_decrypt(message.decode("base64"), M2Crypto.RSA.pkcs1_oaep_padding)
        del rsa
        return decryptedMessage
    except Exception as e:
        print "An Error Occurred:\n" + e


def listener(sock):
    while config.chatstatus:
        data = sock.recv(4096)
        print decryptMessage(data)

def chatter(sock):
    while config.chatstatus:
        message = config.config['nick'] + " | " + raw_input("> ")
        sock.send(encryptMessage(message))


class configClass():
    def __init__(self):
        
        self.chatstatus = False
        self.config = {}
        try:
            configFile = open("msngr.conf", "r").read().strip().split("\n")

            for value in configFile:
                var1, var2 = value.split(":")
                self.config[var1] = var2
        except:
            print """
                  [!] Configuration File Error

                      Please check that a msngr.conf file is in the same location as msngr.py
                      Download default config file here: http://invalidpanda.xyz/MSNGR/msngr.conf
                  """

#  print msngr_msgs["welcome"]
config = configClass()
msngr = True

while msngr:
    for x in config.config:
        print "{}: {}".format(x, config.config[x])
    usrinput = raw_input("Are these settings correct?\n[y/n]>")
    if usrinput == "y":
        print "Continuing..."
    else:
        exit()
    print "Trying keys..."

    try:
        key = open(config.config['public_location'], "rb").read()
        bio = M2Crypto.BIO.MemoryBuffer(key)
        rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        del bio
        del rsa
    except Exception as e:
        print "Error loading public key. Please make sure the location is correct."
        print "Current Setting: {}".format(config.config['public_location'])
        print "Exception: " + str(e)

    try:
        rsa = M2Crypto.RSA.load_key_string(open(config.config['private_location'],"r").read())
        del rsa
    except Exception as e:
        print "Error loading private key. Please make sure the location is correct."
        print "Current Setting: {}".format(config.config['private_location'])
        print "Exception: " + str(e)

    print "Keys loaded successfully."
    usrinput = raw_input("Connect to Server?\n[y/n]>")
    if usrinput[:-1] == "y":
        config.config["server"] = raw_input("Example: 0.0.0.0:0000\n>").strip()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((config.config['server'].split(":")))
            config.chatstatus = True
            print "Starting listener..."
            t = threading.Thread(target=listener, args=(sock))
            t.setDaemon(True)
            t.start()
        except:
            print "Connection Error."
            exit()
    else:
        exit()

    while config.chatstatus:
        #  have the server send it's public key.
        #  have client send in public key
        #  have the server send all public keys of attached clients.
        print repr(config.chatstatus)
        exit()
