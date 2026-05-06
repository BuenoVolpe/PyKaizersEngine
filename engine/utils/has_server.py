import socket

def has_server(host="127.0.0.1", port=5555):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False
    