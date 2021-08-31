from copy import deepcopy
import pygame
from .fixedvar import black, white

def minimax(curr_board, depth, alpha, beta, max_player, game):
    # method to perform the minimax function
    # @params curr_board - the board position
    # @params depth - the depth chosen for the evaluation to go through
    # @params alpha
    # @params beta
    # @params max_player - the player wanting to get the best move
    # @params game - the current game
    # @return the evaluation score and the best move for the player chosen

    if depth == 0 or curr_board.winner() is not None:
        return curr_board.evaluate(), curr_board

    if max_player:
        # set the max player to - infinity
        maxEval = float('-inf')
        best_move = None
        # iterate through all moves recursively
        for move in get_all_moves(curr_board, white, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            # perform pruning
            if beta <= alpha:
                break
            # if score is better, change best move
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        # set the min player to + infinity
        minEval = float('inf')
        best_move = None
        # iterate through all moves recursively
        for move in get_all_moves(curr_board, black, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            # perform pruning
            if beta <= alpha:
                break
            # if score is better, change best move
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, jumped_piece):
    # simulate move method to see where the piece would go and what it would entail
    # @params piece - the piece to move
    # @params move - the move itself
    # @params board - the board position
    # @params jumped_piece - if a piece was jumped or not
    # @return the board to see the "possible" position
    board.move(piece, move[0], move[1])
    if jumped_piece:
        for skip in jumped_piece:
            # perform regicide
            if skip.king:
                board.move(piece, move[0], move[1], 1)
        board.remove_piece(jumped_piece)

    return board


def get_all_moves(board, colour, game):
    # get all the moves from the board
    # @params piece - the piece to move
    # @params colour - is it black or white which all moves are being retrieved for
    # @return the moves possible for all pieces
    moves = []
    for piece in board.iterpieces(colour):
        # Piece is not available for AI if forced cap is available
        if not board.forced_capture(piece)[0]:
            continue
        valid_moves = board.generate_moves(piece)
        for move, skip in valid_moves[0].items():
            # make a deepcopy of the board
            temp_board = deepcopy(board)
            # temporary copies are made of the pieces in the board to see the possible moves
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    return moves
