import random
import subprocess
import json
API_URL = "http://api:8080"


NUM_GAMES = 10


def check_five_in_a_row(board, row, col, player_stone):
    if row <= 15 and all(0 <= row + i < len(board) and board[row + i][col] == player_stone for i in range(5)):
        return True  # Vertical win
    if col <= 15 and all(0 <= col + i < len(board[0]) and board[row][col + i] == player_stone for i in range(5)):
        return True  # Horizontal win
    if row <= 15 and col <= 15 and all(0 <= row + i < len(board) and 0 <= col + i < len(board[0]) and board[row + i][col + i] == player_stone for i in range(5)):
        return True  # Diagonal (top-left to bottom-right) win
    if row >= 4 and col <= 15 and all(0 <= row - i < len(board) and 0 <= col + i < len(board[0]) and board[row - i][col + i] == player_stone for i in range(5)):
        return True  # Diagonal (bottom-left to top-right) win
    return False

def check_winner(board, player_stone):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == player_stone:
                if check_five_in_a_row(board, row, col, player_stone):
                    return True
    return False


def play_game(player_x, player_o):
    wins_x_as_x = 0
    wins_x_as_o = 0

    for _ in range(NUM_GAMES):

        useRow = random.randint(0, 19)
        useCol = random.randint(0, 19)
        response = subprocess.check_output(["curl", f"{API_URL}/newgame/{player_x}"])
        response_data = json.loads(response.decode())
        game_id = response_data["ID"]

        current_player = player_x

        while True:
            response = subprocess.check_output(["curl", f"{API_URL}/nextmove/{game_id}/{useRow}/{useCol}"])
            response_data = json.loads(response.decode())

            if "gameState" in response_data:
                game_state_str = response_data["gameState"]
                
                # Split the game state string by '#' to get parts
                game_state_parts = game_state_str.split('#')
                
                # Initialize variables to hold board information
                board_str = ""
                
                # Find the board information in game state parts
                for part in game_state_parts:
                    if part.startswith('board:'):
                        board_str = part[len('board:'):]
                        break
                
                # Debug statement to print the board_str
                print("Board String:", board_str)
                
                # Ensure the length of board_str is exactly 361
                if len(board_str) == 361:
                    # Split the string into rows of 19 characters each
                    board_rows = [board_str[i:i+19] for i in range(0, len(board_str), 19)]
                    
                    # Parse the board information into a 2D list
                    board = [list(row) for row in board_rows]
                    
                    valid_move_found = False
                    for row in range(20):
                        for col in range(20):
                            if board[row][col] == "-":
                                useRow, useCol = row, col
                                valid_move_found = True
                                break
                        if valid_move_found:
                            break

                    winner = check_winner(board, player_x)

                    if winner == player_x:
                        if current_player == 'x':
                            wins_x_as_x += 1
                        else:
                            wins_x_as_o += 1
                        break
                    elif winner == player_o:
                        break
                    elif winner == "draw":
                        break

                    # Switch players
                    current_player = player_x if current_player == player_o else player_o

                    # Update useRow and useCol based on the available empty spots
                    valid_move_found = False
                    for row in range(20):
                        for col in range(20):
                            if board[row][col] == "-":
                                useRow, useCol = row, col
                                valid_move_found = True
                                break
                        if valid_move_found:
                            break

    return wins_x_as_x, wins_x_as_o


if __name__ == "__main__":
    player_x = "x"  
    player_o = "o"    

    alice_wins_as_x, alice_wins_as_o = play_game(player_x, player_o)

    print(f"Total wins for alice as X: {alice_wins_as_x}")
    print(f"Total wins for alice as O: {alice_wins_as_o}")