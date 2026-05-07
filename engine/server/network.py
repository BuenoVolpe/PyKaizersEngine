import socket
import json

#================================#
class Network:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #--------------------------------#
        self.addr = ("127.0.0.1", 5555)
        #--------------------------------#
        self.client.connect(self.addr)
        #--------------------------------#
        data = json.loads(self.client.recv(2048).decode())
        #--------------------------------#
        self.id = data["id"]
    #================================#
    def send(self, data):
        #--------------------------------#
        try:
            #--------------------------------#
            self.client.send(json.dumps(data).encode())
            #--------------------------------#
            response = self.client.recv(4096)
            #--------------------------------#
            return json.loads(response.decode())
        #--------------------------------#
        except Exception as e:
            print("Network Error:", e)
            return {}
        
        