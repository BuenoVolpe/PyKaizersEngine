import random
import socket
import json
from _thread import start_new_thread
from engine.configs.serversettings import serversettings


server = serversettings.get("server", "0.0.0.0")
port = serversettings.get("port", 5555)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()

print("Server started")

players = {}
current_player = 0


def threaded_client(conn, player_id):
    global players

    players[player_id] = {
        "pos": [100, 100],
        "dir": [0, 0]
    }

    conn.send(json.dumps({"id": player_id}).encode())

    while True:
        try:
            data = conn.recv(4096)

            if not data:
                break

            data = json.loads(data.decode())

            players[player_id]["pos"] = data["pos"]
            players[player_id]["dir"] = data["dir"]

            conn.sendall(json.dumps(players).encode())

        except Exception as e:
            print("Erro:", e)
            break

    print(f"Player {player_id} disconnected")

    if player_id in players:
        del players[player_id]

    conn.close()


while True:
    conn, addr = s.accept()

    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))

    current_player += 1

    