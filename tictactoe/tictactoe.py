"""
Tic Tac Toe Player
"""

import copy
import math
import operator

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    n = 0
    for row in board:
        for square in row:
            if square != EMPTY:
                n += 1
    p = X if n % 2 == 0 else O
    return p


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        row = board[i]
        for j in range(len(row)):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 0 or i > len(board) - 1 or j < 0 or j > len(board) - 1:
        raise Exception("invalid move")
    if board[i][j] != EMPTY:
        raise Exception("that square is not empty")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(3):
        if board[row][0] != EMPTY and (board[row][0] == board[row][1] == board[row][2]):
            return board[row][0]
    for col in range(3):
        if board[0][col] != EMPTY and (board[0][col] == board[1][col] == board[2][col]):
            return board[0][col]
    if board[0][0] != EMPTY and (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    if board[0][2] != EMPTY and (board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for square in row:
            if square == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    if the_winner == X:
        return 1
    if the_winner == O:
        return -1
    return 0


def minimax(board):
    _, action = minimax_proper(board)
    return action


def minimax_proper(board):
    if terminal(board):
        return utility(board), None
    value, op = (-2, operator.gt) if player(board) == X else (2, operator.lt)
    for action in actions(board):
        new_board = result(board, action)
        score, _ = minimax_proper(new_board)
        if op(score, value):
            value = score
            best_action = action
    return value, best_action



def minimax_old(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        value = -2
        for action in actions(board):
            new_board = result(board, action)
            score = min_value(new_board)
            if score > value:
                value = score
                best_action = action
    if player(board) == O:
        value = 2
        for action in actions(board):
            new_board = result(board, action)
            score = max_value(new_board)
            if score < value:
                value = score
                best_action = action
    return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    value = -2
    for action in actions(board):
        new_board = result(board, action)
        value = max(value, min_value(new_board))
    return value


def min_value(board):
    if terminal(board):
        return utility(board)
    value = 2
    for action in actions(board):
        new_board = result(board, action)
        value = min(value, max_value(new_board))
    return value
