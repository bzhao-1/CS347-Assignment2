import random
import subprocess
import json

API_URL = "http://localhost:8080"


NUM_GAMES = 100

def play_game(player_x, player_o):
    wins_x = 0
    wins_o = 0
    
    for _ in range(NUM_GAMES):
        response = subprocess.check_output(["curl", f"{API_URL}/newgame/{player_x}"])
        response_data = json.loads(response.decode())
        game_id = response_data["ID"]
        
        current_player = player_x
        
        while True:
            valid_moves = [] 
            
            if not valid_moves:
                # No valid moves left, the game is a draw
                break
            
            move = random.choice(valid_moves)
            row, col = move
            subprocess.check_output(["curl", f"{API_URL}/nextmove/{game_id}/{row}/{col}"])
            
            game_state = {}  
            winner = game_state.get("winner")
            if winner == player_x:
                wins_x += 1
                break
            elif winner == player_o:
                wins_o += 1
                break
            elif winner == "draw":
                break
            
            # Switch players
            current_player = player_x if current_player == player_o else player_o
    
    return wins_x, wins_o

if __name__ == "__main__":
    player_x = "alice"  # Replace with the name of the player you want to evaluate
    player_o = "bob"    # Replace with the name of the other player (opponent)
    
    alice_wins_as_x, alice_wins_as_o = play_game(player_x, player_o)
    
    print(f"Total wins for {player_x} as X: {alice_wins_as_x}")
    print(f"Total wins for {player_x} as O: {alice_wins_as_o}")