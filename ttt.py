"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Single random trial of a tictactoe game given an existing
    board and a current player.  Recursively and randomly selects 
    moves until complete 
    """
    if board.check_win():
        return

    empties = board.get_empty_squares()
    row, col = empties[random.randrange(0, len(empties))]
    board.move(row, col, player)
    # recurse
    mc_trial(board, provided.switch_player(player))


def mc_update_scores(scores, board, player):
    """
    update the scores list based on the played board and current player
    """
    current_player_score = 0
    other_player_score = 0

    # assign score deltas
    if board.check_win() == player:
        current_player_score = SCORE_CURRENT
        other_player_score = -(SCORE_OTHER)
    elif board.check_win() == provided.switch_player(player):
        current_player_score = -(SCORE_CURRENT)
        other_player_score = SCORE_OTHER

    # now update scores
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += current_player_score
            elif board.square(row, col) == provided.switch_player(player):
                scores[row][col] += other_player_score
     
   
def get_best_move(board, scores):
    """
    Given projected scores and current board, select move with
    maximum score
    """
    max_val = -9223372036854775807 
    max_tuples = []
    # find all tuples with max value
    for row, col in board.get_empty_squares():
        if scores[row][col] > max_val:
            max_val = scores[row][col]
            max_tuples = [(row, col)]
        elif scores[row][col] == max_val:
            max_tuples.append((row, col))

    return max_tuples[random.randrange(0, len(max_tuples))]


def mc_move(board, player, trials):
    """
    select the best move given the current board and number of trials
    with which to examine random outcomes for scoring moves
    """
    # initialize scores
    scores = [[0 for _ in range(board.get_dim())]
              for _ in range(board.get_dim())]

    # run through trials
    for _ in range(0, trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

