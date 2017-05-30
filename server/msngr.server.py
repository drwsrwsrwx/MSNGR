# Author      : Tom McDowell
# Version     : 1.0.0.1

# Description : Server which forwards messages from multiple msngr clients.
# Requires    : sockets, not much else i think?

class server():
    def __init__(self):
        import hashlib
        import socket
        self.hasher = hashlib.md5()
        self.lport = 55689
        self.lhost = "0.0.0.0"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.lhost, self.lport))
        self.sock.listen(10)
        self.version = "1.0.0.1"
        self.active = {}
        

    def landing(self):
        import threading
        while True:
            print "started..."
            session, addr = self.sock.accept()
            session.sendall("msngr_server_" + self.version)
            pubkey = session.recv(8192).strip()
            self.hasher.update(pubkey)
            uniqueid = self.hasher.hexdigest()
            self.active[uniqueid] = {"addr":addr, "session": session, "public_key":pubkey, "id":uniqueid}
            t = threading.Thread(target=self.sendandreceive, args=(session,))
            self.active[uniqueid]["thread"] = t
            self.active[uniqueid]["thread"].setDaemon(True)
            self.active[uniqueid]["thread"].start()
            
            print repr(self.active)

    def sendandreceive(self, session):
        while session:
            data = session.recv(8192)
            recipient, message = data.split("::")
            if recipient in self.active:
                self.active[recipient]["session"].sendall(message)
            else:
                session.sendall("404::"+recipient)


main = server()
main.landing()

