# Author      : Tom McDowell
# Version     : 1.0.0.1

# Description : Server which forwards messages from multiple msngr clients.
# Requires    : sockets, not much else i think?

class server():
    def __init__(self):
        from collections import deque
        import socket
        import hashlib
        self.hasher = hashlib.md5()
        self.lport = 55689
        self.lhost = "0.0.0.0"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.lhost, self.lport))
        self.sock.listen(10)
        self.version = "1.0.0.1"
        self.active = {}
        self.lastToJoin = str()
        self.distlist = dict()
        self.waiting = deque()

    def landing(self):
        import pickle
        import threading
        import hashlib
        md5 = hashlib.md5()
        while True:
            print "started..."
            session, addr = self.sock.accept()
            session.sendall("msngr_server_" + self.version)
            print addr[0], "Sent Version"
            pubkey = session.recv(8192).strip()
            self.lastToJoin = pubkey
            md5.update(pubkey)
            print "Received Pubkey:\n{}".format(md5.hexdigest())
            self.hasher.update(pubkey)
            uniqueid = self.hasher.hexdigest()
            self.active[uniqueid] = {"addr":addr, "session": session, "public_key":pubkey, "id":uniqueid, "active": True}
            self.distlist[uniqueid] = pubkey
            t = threading.Thread(target=self.receive, args=(session,))
            self.active[uniqueid]["rthread"] = t
            self.active[uniqueid]["rthread"].setDaemon(True)
            self.active[uniqueid]["rthread"].start()
            t = threading.Thread(target=self.send, args=())
            t.setDaemon(1)
            t.start()
            print "Trying to update clients..."
            try:
                for user in self.active:
                    print "{} : in self.active".format(user)
                for user in self.active:
                    print "Sending to: {}".format(user)
                    self.active[user]["session"].send("active_users::" + pickle.dumps(self.distlist))
            except Exception as e:
                print "\r[!] landing() Error:\n{}".format(str(e))
            print "Started send Thread..."
            print "Started receive Thread..."

    def sendandreceive(self, session, active_list, addr):
        import pickle
        while session:
            print "Sending Initial Pubkeys --> {}".format(addr[0] + ":" + str(addr[1]))
            session.send(pickle.dumps(self.distlist))
            print "Sent distlist"
            while session:
                print "Waiting for data in thread...\n" + str(repr(session))
                data = session.recv(8192)
                print data
                if data == "request::active_users":
                    session.sendall("active_users::" + pickle.dumps(self.distlist))
                    print "Sent list --> {}:{}".format(addr[0], str(addr[1]))
                try:
                    recipient, message = data.split("::")
                    if recipient in self.active:
                        self.active[recipient]["session"].sendall(message)
                    else:
                        continue
                except:
                    continue
    def send(self):
        print "Started sender..."
        while True:
            if len(self.waiting) > 0:
                clientmsg = self.waiting.popleft()
                print repr(clientmsg)
                print repr(clientmsg).split("::")
                keyid, msg = clientmsg.split("::")
                self.active[keyid]['session'].send(msg)

    def receive(self, session):
        import pickle
        print "Started receive..."
        while True:
            data = session.recv(8192)
            if data == "request::active_users":
                session.send("active_users::" + pickle.dumps(self.distlist))
                print "Send Distlist --> " + str(session)
            elif "request" not in data:
                self.waiting.appendleft(data)

main = server()
main.landing()

