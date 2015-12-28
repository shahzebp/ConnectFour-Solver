from util import memoize, run_search_function
import copy

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
         # If the game has been won, we know that it must have been
         # won or ended by the previous move.
         # The previous move was made by our opponent.
         # Therefore, we can't have won, so return -1000.
         # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


# THis is the new evaluation function
# For every column, it will find out the largest possible
# sequence for the current node in all directions.
# it will return the length of longest number of consequence nodes
# in all directions. We do this for every column.
# If the top node is current player's node, it is added to current
# player's score, else it is added to the other player's score


def new_evaluate(board):
    winningLengthsforCurrent = 0
    winningLengthsforOther   = 0

    for j in range(0,7):
        # Get the height of column
        i = board.get_height_of_column(j);

        # -1 means the column is completely filled
        if -1 == i - 1:
            continue;

        # The function returns board height if the column is empty
        # In this case we reassign the height to 5
        if i == board.board_height:
            i = 5
        else:
            # The number is actually the first empty space from top
            # so we increment to go to first filled node from the top
            i = i + 1

        # We calculate the maximum sequence for current node
        # if the current node is of current player, we add it to current player's score
        # else we add it the oppponent's score
        if (board.get_cell(i, j) == board.get_current_player_id()):
            maxLen = board._max_length_from_cell(i, j)
            if maxLen == 4:
                winningLengthsforCurrent += maxLen + 1000
            elif maxLen == 3:
                winningLengthsforCurrent += maxLen + 100
            elif maxLen == 2:
                winningLengthsforCurrent += maxLen + 50
            else:
                winningLengthsforCurrent += maxLen + 10

            #winningLengthsforCurrent += score

        elif (board.get_cell(i, j) == board.get_other_player_id()):
            maxLen = board._max_length_from_cell(i, j)

            if maxLen == 4:
                winningLengthsforOther += maxLen + 1000
            elif maxLen == 3:
                winningLengthsforOther += maxLen + 100
            elif maxLen == 2:
                winningLengthsforOther += maxLen + 50
            else:
                winningLengthsforOther += maxLen + 10

            #winningLengthsforOther +=  score

    # The final score is score of current player - score of opponent
    return (winningLengthsforCurrent - winningLengthsforOther)



def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

nodesExpandedMiniMax = 0

def minimax(board, depth, eval_fn = basic_evaluate, get_next_moves_fn = get_all_next_moves, is_terminal_fn = is_terminal):
    """
    Call recursive function with basic_evaluate as an argument.
    Check at the end depending upon the last move, which column to pick
    and return the column.

    Reference: https://en.wikipedia.org/wiki/Minimax
    """

    valueSet = minimaxRecurse(board, depth, True, eval_fn, get_next_moves_fn, is_terminal_fn)

    return getChangedColumn(board, valueSet[1])

def findMinimumMaximum(boardConfig, max):
    """
    Finds maximum evaluated value of a node and returns the corresponding board
    and evaluation and locally expanded nodes.

    """

    evaluation = boardConfig[0][0]
    board = boardConfig[0][1]

    if max:
        for valueSet in boardConfig:
            if valueSet[0] > evaluation:
                board = valueSet[1]
                evaluation = valueSet[0]

    else:
        for valueSet in boardConfig:
            if valueSet[0] < evaluation:
                board = valueSet[1]
                evaluation = valueSet[0]


    return (evaluation, board)

def getChangedColumn(oldBoard, changedBoard):

    """
    Crosschecks two board states with each other and finds the offending column.
    This column is the move made. Return column number.
    """
    for i in range(0, 5):
        for j in range(0, 6):
            cell1 = oldBoard.get_cell(i, j)
            cell2 = changedBoard.get_cell(i, j)
            if cell1 != cell2:
                return j

def minimaxRecurse(board, depth, Max, eval_fn, get_next_moves_fn = get_all_next_moves, is_terminal_fn = is_terminal):
    """
    See if the depth is reaced, which would mean leafnode.
    If leafnode, then return eval_fn value for that leafnode.
    If the node is not leafnode, then it is either max node or min node.
    If max node, return recursive call of all the rest nodes with depth decremented.
    If min node, return recursive call of all the rest nodes with depth decremented.
    """

    global nodesExpandedMiniMax

    boardConfig = []
    if depth == 0:
        return (eval_fn(board), board)

    for currentBoard in get_next_moves_fn(board):
        nodesExpandedMiniMax += 1
        boardConfig.append(minimaxRecurse(currentBoard[1], depth-1, not Max, eval_fn))

    if not Max:
        return findMinimumMaximum(boardConfig, False)
    else:
        return findMinimumMaximum(boardConfig, True)


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]



random_player = lambda board: rand_select(board)
basic_player  = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player    = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)