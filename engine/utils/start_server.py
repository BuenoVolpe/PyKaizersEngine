import subprocess
import sys

def start_server():
    subprocess.Popen([sys.executable, "-m", "engine.server.server"])
