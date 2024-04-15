import sys
#implementing the main minmax function
def min_max_with_alpha_beta(state_current, depth_till, alpha, beta, p_max, ver):
    if depth_till == 0 or game_at_terminal_state(state_current): #for when state reaches end of depth or terminal state ,this is how  the progrma returns the evaluated value
        return evaluate(state_current, ver, not p_max), None

    moves_given = moves_to_be_followed(state_current, ver) #follows suggested order
    if p_max:
        maximum_of_evaluated = float('-inf')
        most_optimal_move = None
        for move in moves_given:
            temp_state = state_current.copy()
            play_move(temp_state, move)
            evaluated_value, _ = min_max_with_alpha_beta(temp_state, depth_till - 1, alpha, beta, False, ver)
            if evaluated_value > maximum_of_evaluated:
                maximum_of_evaluated = evaluated_value
                most_optimal_move = move
            alpha = max(alpha, evaluated_value)#generating alpha of current state
            if beta <= alpha:#pruning condition
                break
        return maximum_of_evaluated, most_optimal_move
    else:
        minimum_of_evaluated = float('inf')
        most_optimal_move = None
        for move in moves_given:
            temp_state = state_current.copy()
            play_move(temp_state, move)
            evaluated_value, _ = min_max_with_alpha_beta(temp_state, depth_till - 1, alpha, beta, True, ver)
            if evaluated_value < minimum_of_evaluated:
                minimum_of_evaluated = evaluated_value
                most_optimal_move = move
            beta = min(beta, evaluated_value) #assigning value for beta of current state
            if beta <= alpha:#pruning condition
                break
        return minimum_of_evaluated, most_optimal_move

def moves_to_be_followed(game_state, version): #giving pre defined move ordering to be followed
    list_of_given_moves_in_order = []
    if version == 'standard':#for standard checking if moves or possible and then appending the order to a list to be followed
        if game_state['num_red'] >= 2:
            list_of_given_moves_in_order.append(('red', 2))
        if game_state['num_blue'] >= 2:
            list_of_given_moves_in_order.append(('blue', 2))
        if game_state['num_red'] >= 1:
            list_of_given_moves_in_order.append(('red', 1))
        if game_state['num_blue'] >= 1:
            list_of_given_moves_in_order.append(('blue', 1))
    else: #checking moves are possible and then appending to the list for misere version
        if game_state['num_blue'] >= 1:
            list_of_given_moves_in_order.append(('blue', 1))
        if game_state['num_red'] >= 1:
            list_of_given_moves_in_order.append(('red', 1))
        if game_state['num_blue'] >= 2:
            list_of_given_moves_in_order.append(('blue', 2))
        if game_state['num_red'] >= 2:
            list_of_given_moves_in_order.append(('red', 2))

    return list_of_given_moves_in_order

def play_move(state_of_game, move):#changing state upon entries of values for color and quantity
    color_selected, amount_entered = move
    if color_selected in ['red', 'blue']:
        if color_selected == 'red':
            state_of_game['num_red'] = max(0, state_of_game['num_red'] - amount_entered)
        else:
            state_of_game['num_blue'] = max(0, state_of_game['num_blue'] - amount_entered)

def game_at_terminal_state(state_of_game):#defining terminal state
    return state_of_game['num_red'] == 0 or state_of_game['num_blue'] == 0

def evaluate(game_state, version, last_move_made_by_max):#evaluation function
    if game_at_terminal_state(game_state):
        if version == 'standard':
            return float('inf') if last_move_made_by_max else float('-inf')
        else:
            return float('-inf') if last_move_made_by_max else float('inf')
    else:
        return game_state['num_red'] * 2 + game_state['num_blue'] * 3

def parse_arguments(args):#checking the entries from terminal command and parsing them adding defaults for missing entries for version , first_player  as directed . For depth default is set at 5
    num_red = int(args[0]) if args[0].isdigit() and int(args[0]) >= 0 else 0
    num_blue = int(args[1]) if args[1].isdigit() and int(args[1]) >= 0 else 0
    version = args[2] if len(args) > 2 and args[2] in ['standard', 'misere'] else 'standard'
    first_player = args[3] if len(args) > 3 and args[3] in ['computer', 'human'] else 'computer'
    depth = int(args[4]) if len(args) > 4 and args[4].isdigit() and int(args[4]) > 0 else 5
    return num_red, num_blue, version, first_player, depth

def print_winner(last_player, version, game_state): #printing iwnner function
    remaining_score = game_state['num_red'] * 2 + game_state['num_blue'] * 3#calculating score as directed of current state or last player
    if version == 'standard':#identification of winner  based on who made the last play.since its standard , we are declaring the last player as winner.
        winner = last_player
        print(f"\nGame over. {winner} wins with a score of {remaining_score}.")

    else:#identification of loser based on last player. Since it is misere, the last player is the loser.  
        print(f"\nGame over. {last_player} loses with a score of {(-1)*remaining_score}.")


def main():
    num_red, num_blue, version, first_player, depth = parse_arguments(sys.argv[1:])
    game_state = {'num_red': num_red, 'num_blue': num_blue}
    player_turn = first_player

    while not game_at_terminal_state(game_state):
        print(f"\nCurrent state: Red : {game_state['num_red']}, Blue : {game_state['num_blue']}") #to print current state at every iteration of play
        if player_turn == 'computer':
            _, best_move = min_max_with_alpha_beta(game_state, depth, float('-inf'), float('inf'), True, version)
            if best_move is None and not game_at_terminal_state(game_state):
                best_move = moves_to_be_followed(game_state, version)[0]
            print(f"Computer played: {best_move}")
            play_move(game_state, best_move)
        else:
            valid_move = False
            while not valid_move:
                move = input("Your move (color amount): ").split()
                if len(move) == 2 and move[0].lower() in ['red', 'blue'] and move[1].isdigit(): #checking validity of human entry for each move.
                    color = move[0].lower()
                    amount = int(move[1])
                    if amount in [1, 2] and ((color == 'red' and amount <= game_state['num_red']) or (color == 'blue' and amount <= game_state['num_blue'])): #further checking validity by checking if enough marbles are left to pick
                        play_move(game_state, (color, amount))
                        valid_move = True
                    else:
                        print(f"Invalid move. You can only take 1 or 2 marbles, and there are {game_state['num_red']} red and {game_state['num_blue']} blue marbles left.")#printing prompts to enable the user/human to correct their entries
                else:
                    print("Please enter a valid move in the format 'color amount' (e.g., 'red 2').")#enabling correct entry of colors through prompt messages

        if game_at_terminal_state(game_state):
            break
        player_turn = 'human' if player_turn == 'computer' else 'computer' #at terminal state , changing value of player turn to previous player as the winning decisions are based on player whose move resulted in terminal state.

    print_winner(player_turn, version, game_state)

if __name__ == "__main__":
    main()
