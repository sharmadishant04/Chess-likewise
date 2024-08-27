import asyncio
import websockets
import json

board = [
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '']
]

player_a_start = ['A-P1', 'A-H1', 'A-H2', '', '']
player_b_start = ['B-H2', 'B-H1', 'B-P1', '', '']

board[0] = player_a_start
board[4] = player_b_start

current_player = 'A'

def process_move(player, move):
    char_name, direction = move.split(':')
    found = False

    for row in range(5):
        for col in range(5):
            if board[row][col] == f"{player}-{char_name}":
                found = True
                target_row, target_col = row, col

                if 'P' in char_name or 'H1' in char_name:
                    if direction == 'L':
                        target_col -= 1
                    elif direction == 'R':
                        target_col += 1
                    elif direction == 'F':
                        target_row -= 1 if player == 'A' else 1
                    elif direction == 'B':
                        target_row += 1 if player == 'A' else -1

                elif 'H2' in char_name:
                    if direction == 'FL':
                        target_row -= 2 if player == 'A' else 2
                        target_col -= 2
                    elif direction == 'FR':
                        target_row -= 2 if player == 'A' else 2
                        target_col += 2
                    elif direction == 'BL':
                        target_row += 2 if player == 'A' else -2
                        target_col -= 2
                    elif direction == 'BR':
                        target_row += 2 if player == 'A' else -2
                        target_col += 2

                if not (0 <= target_row < 5 and 0 <= target_col < 5):
                    return False, "Move out of bounds."

                if board[target_row][target_col] != '':
                    if board[target_row][target_col].startswith(player):
                        return False, "Cannot move to a position occupied by a friendly piece."
                    else:
                        board[target_row][target_col] = ''
                
                board[target_row][target_col] = board[row][col]
                board[row][col] = ''
                return True, "Move successful."

    if not found:
        return False, "Character does not exist."

async def handle_client(websocket, path):
    global current_player

    while True:
        message = await websocket.recv()
        data = json.loads(message)

        player = data['player']
        move = data['move']

        if player != current_player:
            await websocket.send(json.dumps({"status": "error", "message": "It's not your turn."}))
            continue

        success, msg = process_move(player, move)
        if success:
            current_player = 'B' if current_player == 'A' else 'A'
            game_state = {
                "status": "success",
                "message": msg,
                "board": board,
                "current_player": current_player
            }
        else:
            game_state = {
                "status": "error",
                "message": msg,
                "board": board,
                "current_player": current_player
            }

        await websocket.send(json.dumps(game_state))

start_server = websockets.serve(handle_client, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
