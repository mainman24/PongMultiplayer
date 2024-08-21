import socket
import pickle


class Network:

    def __init__(self):
        self.ip = "192.168.1.8"
        self.port = 5555
        self.addr = (self.ip, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.P = self.connect()
        # print(self.P)

    def getP(self):
        return self.P

    def connect(self):
        try:
            try:
                self.client.connect(self.addr)
            except:
                self.client.connect((self.ip, self.port + 1))
            # self.client.setblocking(False)  # Prevent blocking since code blocks at recv code
            # return pickle.loads(self.client.recv(2048))
            data = b''
            # I Think send all fixes it
            x = self.client.recv(2048)
            #print("hey", x, pickle.loads(x))
            # try:
            #    x = self.client.recv(1024)
            #    print("hey", x, pickle.loads(x))
            # except socket.error as e:
            #    print(str(e))

            data += x  # MAYBE THIS LINE

            data_fin = pickle.loads(data)
            # print(data_fin)
            return data_fin
        except socket.error as e:
            print(str(e))

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))  # sendall sends the entire object
            return pickle.loads(self.client.recv(2048*16))
        except socket.error as e:
            print(e)


#n = Network()
# print(n.P)
