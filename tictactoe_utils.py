"""
Tic Tac Toe Bot
"""

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    # Returns starting state of the board.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Returns player who has the next turn on a board.
    turn = 0
    for rows in board:
        for state in rows:
            if state == EMPTY:
                turn+=1
    
    return O if turn%2==0 else X
    

def actions(board):
    # Returns set of all possible actions (i, j) available on the board.
    action = set()
    for i, rows in enumerate(board):
        for j in range(len(rows)):
            if board[i][j] == EMPTY:
                action.add((i,j))
    
    return action
                

def result(board, action):
    # Returns the board that results from making move (i, j) on the board.
    nboard = deepcopy(board)
    if board[action[0]][action[1]] == EMPTY:
        nboard[action[0]][action[1]] = player(board)
        return nboard
    else:
        raise Exception("Invalid Action")
        

def check_win(size):
    # Returns win conditions for the game.
    for row in range(size):
        yield [(row, col) for col in range(size)]   # Check Rows
    for col in range(size):
        yield [(row, col) for row in range(size)]   # Check Columns
    
    yield [(i, i) for i in range(size)]             # Diagonal top left to bottom right
    yield [(i, size - 1 - i) for i in range(size)]  # Diagonal top right to bottom left
    
def winner(board):
    # Returns the winner of the game, if there is one.
    size = len(board)
    for move in [X,O]:
        for wins in check_win(size):
            if all(board[row][col] == move for row, col in wins):
                return move
        
    else:
        return None
    

def terminal(board):
    # Returns True if game is over, False otherwise.
    return winner(board) != EMPTY or all(EMPTY not in row for row in board)


def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    # Returns the optimal action for the current player on the board.
    if terminal(board):
        return None
    
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
            
        value = -1
        alpha, beta = -1, 1
        for action in actions(board):
            value = max(value,min_value(result(board, action), alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
           
        value = 1
        alpha, beta = -1, 1
        for action in actions(board):
            value = min(value,max_value(result(board, action), alpha, beta))
            alpha = min(alpha, value)
            if alpha >= beta:
                break
        return value

    if player(board) == X:
        score = -1
        alpha, beta = -1, 1
        best_move = None
        for action in actions(board):
            minv = min_value(result(board, action), alpha, beta)
            if minv >= score:
                score = minv
                best_move = action
        return best_move
    elif player(board) == O:
        score = 1
        alpha, beta = -1, 1
        best_move = None
        for action in actions(board):
            maxv = max_value(result(board, action), alpha, beta)
            if maxv <= score:
                score = maxv
                best_move = action
        return best_move
