from connectfour import *
from basicplayer import *
from util import *
import tree_searcher
import time

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)


#run_game(basic_player, human_player)
#from basicplayer import nodesExpandedMiniMax
#print ("Nodes expanded :", nodesExpandedMiniMax)

## Running new player vs basic player.
#*************************************************************************************************

run_game(new_player, basic_player)
from basicplayer import nodesExpandedMiniMax
print ("Nodes expanded :", nodesExpandedMiniMax)


#run_game(human_player, basic_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return currentnodeval >= 1000 means that the current player has won;
    a return currentnodeval <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.


# This is the function that that invokes the inner alpha beta
# search method that inolves actual pruning

nodesExpandedAlphaBeta = 0

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn = is_terminal):

    # to find out which column bas been changed. This statemen
    # provides a call to internal AlphaBeta pruning function
    changedcolumnno = getChangedColumn(board, (AphaBetaPruning(board, depth, NEG_INFINITY, INFINITY, True)[1]))

    return changedcolumnno

# This method is adapter from the aplha beta pruning algorithm found on wikipedia.
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode

def AphaBetaPruning(board, depth, alpha, beta, isMax, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal):
    # we are on final depth, use the evaluation function to evaluate the heursitic of the
    # board and return the score and board as a tuple
    if depth == 0:
        return (eval_fn(board),board)

    #Create a temporary empty object of board
    tempBoard = copy.deepcopy(board)
    global nodesExpandedAlphaBeta

    if isMax:
        # Operation is now on maximum node
        currentnodeval = NEG_INFINITY

        # Generate the child node for the current board
        for childBoard in get_next_moves_fn(board):

            # Recursive call to self. Note that the next level is supposed to be Min
            childTuple = AphaBetaPruning(childBoard[1], depth-1, alpha, beta, False)
            nodesExpandedAlphaBeta = nodesExpandedAlphaBeta + 1

            # We have found a board with higher score. Hence the node value and aplha
            # value should be updated succesfully
            if (childTuple[0] > currentnodeval):
                currentnodeval = childTuple[0]
                tempBoard = childTuple[1]

            if (currentnodeval > alpha):
                alpha = currentnodeval
            
            if beta <= alpha:
                # Pruning on the basis of max node
                break

        return (currentnodeval, tempBoard)

    else:
        # Operation is now on minimum node
        currentnodeval = INFINITY

        # Generate the child node for current board
        for childBoard in get_next_moves_fn(board):

            # Recursive call to self. Note that the next leve is supposed to be Max
            childTuple = AphaBetaPruning(childBoard[1], depth-1, alpha, beta, True)

            nodesExpandedAlphaBeta = nodesExpandedAlphaBeta + 1

            # we have found a board with lower score. Hence the node value and beta value
            # should be updated successfully
            if (childTuple[0] < currentnodeval):
                currentnodeval = childTuple[0]
                tempBoard = childTuple[1]

            if (currentnodeval < beta):
                beta = currentnodeval
                
            if beta <= alpha:
                # Pruning on the basis of min node
                break

        return (currentnodeval, tempBoard)


## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth = 4, eval_fn=new_evaluate(board))


## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)


# Alpha beta vs NewPlayer # same heuristic but alphabeta has pruning.
#**********************************************************************************************************************
#run_game(alphabeta_player, new_player)
#print ("Nodes Expanded :", nodesExpandedAlphaBeta)


#Finally, We run aplabeta player vs basic player,
#**********************************************************************************************************************
#run_game(basic_player, alphabeta_player)
#print ("Nodes Expanded :", nodesExpandedAlphaBeta)



#run_game(alphabeta_player, basic_player)
#print ("Nodes Expanded :", nodesExpandedAlphaBeta)


## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""