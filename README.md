#Red_Blue_Nim
By : Jayadev Mandava  Mav_ID : 1002062733
File named : red_blue_nim.py

Steps for running the program :
Download the python file. Now using terminal, you need to navigate to the file appropriately.
In terminal , use the command python3 red_blue_nim.py [number of red] [number of blue] [version] [first_player] [depth] , filling in the arguments right for number of red marbles followed by number of blue marbles(numbers >0 for both red and blue),version (standard/misere) , first_player(computer/human) and depth(any number >0) .
5. Defaults for version : standard , first_player : computer and depth : 5.
6. If first_player = computer , the computer plays it move and asks you to enter your play .
Example :  When it gives you the prompt , give your [COLOR] [Quantity] response.
Ex : red 2 // red 1//blue 2// blue 1.

red_blue_nim.py 6 6 standard human 5

The following is the way inputs are perceived :
State created with Red : 6 Blue : 6 , version : Standard , First player : human and Depth : 5 
Example for play :
Blue 2 “Removes 2 blue from pile blue” New state will be red 6 blue 4
For versions with first_player as human , the program directly gives : “Your move(color amount)” and waits for your response. (Ex : red 2, red1 , blue 2, blue 1)
7. Keep giving valid input as above until the game lands on a terminal state.
8. Based on the version and current state the game prints a message declaring the winner/loser and gives their score.

Notes : 
Any possible cases for red and blue are accepted. : red / Red / RED & blue/Blue/BLUE
Any input with red or blue is converted to lower case utilizing “.lower( )” . 
Any inputs other red and blue forms are not accepted . 

Similarly with count inputs , only 1 or 2 are accepted (given that there are two marbles to picks as well if input 2) .

I have implemented efficient input validation methods to cover all invalid cases to the best of my knowledge.


Evaluation Function :
def evaluate(game_state, version, last_move_made_by_max):
    if game_at_terminal_state(game_state):
        if version == 'standard':
            return float('inf') if last_move_made_by_max else float('-inf')
        else:
            return float('-inf') if last_move_made_by_max else float('inf')
    else:
        return game_state['num_red'] * 2 + game_state['num_blue'] * 3

This is the evaluation function I have utilized . 

The reason for selecting “inf” and “-inf” for terminals states is to directly identify the winning or losing scenarios in each version respectively.  
In case of standard if last move is made by max player it returns an “inf” or winning/favourable condition for play in a terminal state.
In case of misere version , if last move is played by max player it returns an “-inf” or losing/unfavourable condition for play in a terminal state.

Further, since the program is utilizing depth as a parameter for minimax, when depth is reached the score for current state is evaluated and then minimax continues normally storing this score if it suits the conditions and carries ti forwards for further comparisons.
The evaluation score is given by  “return game_state['num_red'] * 2 + game_state['num_blue'] * 3”.
This uses the directed scores at end if game. This is quite easy as it directly plays for higher of those scores. Inertly a trend that can be observed is that in all equal scenarios it tends to pick red more often as it tries to leave more blues remaining scenarios intact as blues hold greater score weightage than reds.
This is automatically reflected as even though it only considers the sum of blue and red states , the states with more blues generate higher scores and hence gain priority acting as an added benefit to optimality of picking the best move.

One reason for selecting inf or -inf for terminal states is the ease with which the program will be able to distinctively play both versions . I have tried with using the same multiplication of red and blue scores for even terminal states but that version of evaluation is making the code too complicated as well as increasing the overhead of computation for large entries for red and blue while not adding much efficiency in any of the cases I have tried.





References : 
https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/
https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
https://crystal.uta.edu/~gopikrishnav/classes/common/4308_5360/slides/alpha_beta.pdf
https://mathspp.com/blog/minimax-algorithm-and-alpha-beta-pruning
https://realpython.com/python-minimax-nim/
https://www.youtube.com/watch?v=trKjYdBASyQ
https://thecodingtrain.com/challenges/154-tic-tac-toe-minimax
