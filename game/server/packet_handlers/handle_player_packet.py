from game.enums.packet_type import PacketType
from game.server.packets import send_packet


def handle_player_packet(obj, conn, player_id, data):
        with obj.players_lock:
            #--------------------------------#
            player = obj.world.players[player_id]
            #--------------------------------#
            player.update(data)
            #--------------------------------#
            serialized_players = {
                pid: p.serialize()
                for pid, p in obj.world.players.items()
            }
        #--------------------------------#
        send_packet(
            conn,
            PacketType.PLAYERS_OUTPUT,
            serialized_players
        )