import socket
import json
from game.server.packets import create_packet, read_packet
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
    def send(self, data, packet_type="move"):
        #--------------------------------#
        try:
            #--------------------------------#
            packet = create_packet(packet_type, data)
            self.client.send(packet)
            #--------------------------------#
            response = self.client.recv(4096)
            #--------------------------------#
            packet = read_packet(response)

            return packet
        #--------------------------------#
        except Exception as e:
            print("Network Error:", e)
            return {}
        
        