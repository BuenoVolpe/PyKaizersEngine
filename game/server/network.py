import socket
import json
import threading
from engine.utils.log import log_error
from game.enums.packet_type import PacketType
from game.server.packets import create_packet, read_packet, receive_packet, send_packet
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
        self.packet_queue = []
        self.queue_lock = threading.Lock()
        self.running = True 
        #--------------------------------#
        packet = receive_packet(self.client)

        if not packet:
            raise Exception("Disconnected")
        
        if packet["type"] == PacketType.SERVER_FULL:
            raise Exception(packet["data"]["message"])

        self.id = packet["data"]["id"]
        #--------------------------------#
        threading.Thread(
            target=self.receive_loop,
            daemon=True
        ).start()
    #================================#
    def send(self, data, packet_type="move"):
        #--------------------------------#
        try:
            #--------------------------------#
            send_packet(
                self.client,
                packet_type,
                data
            )
        #--------------------------------#
        except Exception as e:
            log_error("Network Error:" + str(e))
            return {}
    #================================#
    def receive_loop(self):
        while self.running:
            try:
                packet = receive_packet(self.client)

                if not packet:
                    break

                with self.queue_lock:
                    self.packet_queue.append(packet)

            except Exception as e:
                log_error(e)
                break
        