import json
import struct
#================================#
def create_packet(packet_type: str, data: dict):
    #--------------------------------#
    return json.dumps({
        "type": packet_type,
        "data": data
    }).encode()
#================================#
def read_packet(raw_data: bytes):
    return json.loads(raw_data.decode())
#================================#
def send_packet(conn, packet_type, data):
    packet = json.dumps({
        "type": packet_type,
        "data": data
    }).encode()

    size = struct.pack("!I", len(packet))

    conn.sendall(size + packet)
#--------------------------------#
def recv_exact(conn, size):
    buffer = b""

    while len(buffer) < size:
        data = conn.recv(size - len(buffer))

        if not data:
            return None

        buffer += data

    return buffer

def receive_packet(conn):
    size_data = recv_exact(conn, 4)

    if not size_data:
        return None

    packet_size = struct.unpack("!I", size_data)[0]

    packet_data = recv_exact(conn, packet_size)

    if not packet_data:
        return None

    return json.loads(packet_data.decode())

