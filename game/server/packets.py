import json
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

