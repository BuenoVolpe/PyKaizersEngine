import socket
import json
#--------------------------------#
from _thread import start_new_thread
#================================#
from engine.configs.serversettings import serversettings
from engine.utils.log import log, log_error, log_success
#================================#
class GameServer:
    #================================#
    def __init__(self, host="0.0.0.0", port=5555):
        #--------------------------------#
        self.host = host
        self.port = port
        #--------------------------------#
        self.players = {}
        self.current_player = 0
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
            #--------------------------------#
            log(f"Connected to: {addr}", "CYAN", ["bright"])
            #--------------------------------#
            player_id = self.current_player
            self.current_player += 1
            #--------------------------------#
            start_new_thread(
                self.handle_client,
                (conn, player_id)
            )
    #================================#
    def handle_client(self, conn, player_id):
        #--------------------------------#
        self.players[player_id] = {
            "pos": [100, 100],
            "dir": [0, 0],
            "color": "standard"
        }
        #--------------------------------#
        conn.send(json.dumps({
            "id": player_id
        }).encode())
        #--------------------------------#
        while True:
            #--------------------------------#
            try:
                #--------------------------------#
                data = conn.recv(4096)
                #--------------------------------#
                if not data:
                    break
                #--------------------------------#
                data = json.loads(data.decode())
                #--------------------------------#
                self.players[player_id]["pos"] = data["pos"]
                self.players[player_id]["dir"] = data["dir"]
                #--------------------------------#
                conn.sendall(
                    json.dumps(self.players).encode()
                )
            #================================#
            except Exception as e:
                log_error(f"Error occurred while handling client {player_id}: {e}")
                break
        #--------------------------------#
        log(f"Player {player_id} disconnected", "MAGENTA", ["bright"])
        #--------------------------------#
        if player_id in self.players:
            del self.players[player_id]
        #--------------------------------#
        conn.close()

#================================#
# if __name__ == "__main__":
server = GameServer()
server.start()
        