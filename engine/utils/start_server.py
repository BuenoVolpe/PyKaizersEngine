import subprocess
import sys

def start_server(developer_mode=False, player_count=2):
    subprocess.Popen([sys.executable, "-m", "game.server.server"])


    #developer mode: start multiple instances of the game
    if developer_mode:
        for _ in range(player_count):
            subprocess.Popen([sys.executable, "-m", "main"])
