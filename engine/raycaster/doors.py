import math

def update_doors(doors, player_pos, dt):
    for i in range(doors.shape[0]):

        state = int(doors[i, 7])

        if state == 1:  # abrindo
            doors[i, 5] += doors[i, 6] * dt
            if doors[i, 5] >= 0.9:
                doors[i, 5] = 1
                doors[i, 7] = 2  # aberto

        elif state == 3:  # fechando
            # checa se player está na porta
            px, py = player_pos  # você precisa passar isso

            if abs(px - doors[i,0]) < 0.5 and abs(py - doors[i,1]) < 0.5:
                continue  # não fecha

            doors[i, 5] -= doors[i, 6] * dt
            if doors[i, 5] <= 0.0:
                doors[i, 5] = 0.0
                doors[i, 7] = 0  # fechado

        # 0 = fechado
        # 1 = abrindo
        # 2 = aberto
        # 3 = fechando

def toggle_door(doors, i):
    state = int(doors[i, 7])

    if state in (0, 3):  # fechado ou fechando
        doors[i, 7] = 1  # abrir
    elif state in (2, 1):  # aberto ou abrindo
        doors[i, 7] = 3  # fechar
    return doors[i, 7]

def can_open_door(cam, door):
    dx = door[0] - cam.pos[0]
    dy = door[1] - cam.pos[1]

    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 2.0:
        return False

    # normaliza
    dx /= dist
    dy /= dist

    # dot product
    dot = dx * cam.dir[0] + dy * cam.dir[1]

    return dot > 0.5  # ~60° cone

