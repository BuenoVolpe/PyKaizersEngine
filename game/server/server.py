import socket
import json
#--------------------------------#
import threading
import time
#================================#
from engine.configs.serversettings import serversettings
from engine.utils.log import log, log_error, log_success
#--------------------------------#
from game.server.packets import create_packet, read_packet, receive_packet, send_packet
from game.server.objects.player import Player
#--------------------------------#
from game.enums.packet_type import PacketType
#================================#
class GameServer:
    #================================#
    def __init__(self, host="0.0.0.0", port=5555):
        #--------------------------------#
        self.host = host
        self.port = port
        #--------------------------------#
        self.players = {}
        self.players_lock = threading.Lock()
        self.current_player = 0
        #--------------------------------#
        self.max_players = serversettings.get("max_players", 4)
        #--------------------------------#
        self.packet_handlers = {
            PacketType.PLAYERS_INPUT: self.handle_player_packet,
            PacketType.BATCH: self.handle_batch_packet,
        }
        #--------------------------------#
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    #================================#
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        #--------------------------------#
        log(f"Server started on {self.host}:{self.port}", "CYAN", ["bright"])
        #--------------------------------#
        while True:
            conn, addr = self.socket.accept()

            with self.players_lock:
                if len(self.players) >= self.max_players:
                    send_packet(conn, PacketType.SERVER_FULL, {"message": "Server is full"})
                    time.sleep(0.1)
                    conn.close()
                    continue

            log(f"Connected to: {addr}", "CYAN", ["bright"])

            with self.players_lock:
                player_id = self.current_player
                self.current_player += 1

            threading.Thread(
                target=self.handle_client,
                args=(conn, player_id),
                daemon=True
            ).start()
    #================================#
    def handle_player_packet(self, conn, player_id, data):
        with self.players_lock:
            #--------------------------------#
            player = self.players[player_id]
            #--------------------------------#
            player.update(data)
            #--------------------------------#
            serialized_players = {
                pid: p.serialize()
                for pid, p in self.players.items()
            }
        #--------------------------------#
        send_packet(
            conn,
            PacketType.PLAYERS_OUTPUT,
            serialized_players
        )
    #================================#
    def handle_batch_packet(self, conn, player_id, data):
        #--------------------------------#
        for packet in data:
            #--------------------------------#
            packet_type = packet["type"]
            packet_data = packet["data"]
            #--------------------------------#
            handler = self.packet_handlers.get(packet_type)
            #--------------------------------#
            if handler:
                handler(conn, player_id, packet_data)
    #================================#
    def handle_client(self, conn, player_id):
        #--------------------------------#
        with self.players_lock:
            self.players[player_id] = Player(player_id)

        #--------------------------------#
        #inital packet
        send_packet(conn, PacketType.INIT, {
            "id": player_id
        })
        #================================#
        while True:
            #--------------------------------#
            try:
                #--------------------------------#
                packet = receive_packet(conn)
                #--------------------------------#
                if not packet:
                    break
                #--------------------------------#
                packet_type = packet["type"]
                packet_data = packet["data"]
                #--------------------------------#
                handler = self.packet_handlers.get(packet_type)
                if handler:
                    handler(conn, player_id, packet_data)
                #--------------------------------#
            except Exception as e:
                log_error(e)
                break
        #================================#
        log(f"Player {player_id} disconnected", "CYAN")
        #--------------------------------#
        with self.players_lock:
            if player_id in self.players:
                del self.players[player_id]
        #--------------------------------#
        conn.close()
#================================#
# if __name__ == "__main__":
server = GameServer()
server.start()
        