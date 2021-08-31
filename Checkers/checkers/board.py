import pygame
from checkers.fixedvar import brown, black, white, space, columns, rows, dark_brown, black_winner, white_winner
from .piece import Piece


class Board:
    # This board holds all the functions for drawing, amending and evaluating the board and the pieces inside

    def __init__(self):
        self.board = []
        self.black_pieces = 12  # number of black pieces remaining
        self.white_pieces = 12  # number of white pieces remaining
        self.black_kings = 0  # number of black king pieces remaining
        self.white_kings = 0  # number of white king pieces remaining
        self.append_pieces()  # creates board object

    def evaluate(self):
        # Evaluates the Board, used for the Minimax function
        # @return score = the evaluation score

        column_pieces_w = 0
        column_pieces_b = 0
        end_pieces = 0.25
        white_checkers = self.iterpieces(white)
        for row in self.board:
            for piece in white_checkers:
                if row[0] == piece or row[7] == piece:
                    column_pieces_w += 0.2

        black_checkers = self.iterpieces(black)
        for row in self.board:
            for piece in black_checkers:
                if row[0] == piece or row[7] == piece:
                    column_pieces_b += 0.2

        # How many pieces are on the wall
        wall_score = column_pieces_w - column_pieces_b

        # How many kings remain
        king_score = (self.white_kings - self.black_kings) * 2

        # How many pieces remain
        remaining_pieces = self.white_pieces - self.black_pieces

        score = remaining_pieces + king_score + wall_score

        return score

    def draw_checkers(self, window):
        # Draws the Checkers Board
        # @params window - this is the window itself where the squares are drawn onto
        window.fill(dark_brown)

        # loop through rows and columns to generate each square
        for row in range(rows):
            for col in range(row % 2, rows, 2):
                pygame.draw.rect(window, brown, (row * space, col * space, space, space))

    def iterpieces(self, colour):
        # Goes through all the pieces and returns all pieces of a colour
        # @params colour - this is used to determine which colour is present
        # @return - returns the pieces
        pieces = []

        # iterates through the board
        for row in self.board:
            for piece in row:
                # Piece is present if piece returns an object and not 0
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col, regicide=0):
        # move the actual piece with the selected square
        # @params piece - the piece chosen
        # @params row - the row where the piece will move to
        # @params col - the col where the piece will move to
        # @params regicide - if regicide = 1, the piece will automatically become a king upon its move

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # check if piece has reached the final row to determine if it is a king or not
        if row == 7 or row == 0:
            piece.make_king()
            if piece.colour == black:
                self.black_kings += 1
            else:
                self.white_kings += 1

        # make king if regicide carried out
        if regicide == 1:
            piece.make_king()

    def get_piece(self, row, col):
        # get one piece
        # @params row - the row
        # @params col - the col
        # @return piece object

        # stay within the limits as side of window can be theoretically selected
        if row <= 8 and col <= 8:
            return self.board[row][col]


    def append_pieces(self):
        # create the board - add each piece to a valid starting square, add object not drawing
        for row in range(rows):
            self.board.append([])
            for col in range(columns):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, white))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, black))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        # draw the actual piece object onto the board by calling piece.draw_piece function
        # @params - window - the window
        self.draw_checkers(window)
        for row in range(rows):
            for col in range(columns):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(window)

        # See if a player has won - if so display the images on the side of the window
        if self.white_pieces == 0:
            window.blit(black_winner, (500, 0))
        if self.black_pieces == 0:
            window.blit(white_winner, (500, 0))

    def remove_piece(self, pieces):
        # remove the pieces from the board if jumped
        # @params pieces - the pieces that have been jumped

        # multiple incase a multi-leg jump was made
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == black:
                    self.black_pieces -= 1
                else:
                    self.white_pieces -= 1

    def generate_moves(self, piece):
        # generate all possible moves that a piece may do. Includes forced capture.
        # @params piece - piece object chosen
        # @return all possible moves in a dictionary, and the object moved

        possible_moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.colour == black or piece.king:
            possible_moves.update(self._move_left(row - 1, max(row - 3, -1), -1, piece.colour, left))
            possible_moves.update(self._move_right(row - 1, max(row - 3, -1), -1, piece.colour, right))

        if piece.colour == white or piece.king:
            possible_moves.update(self._move_left(row + 1, min(row + 3, rows), 1, piece.colour, left))
            possible_moves.update(self._move_right(row + 1, min(row + 3, rows), 1, piece.colour, right))

        # loops through all the available moves, if a forced capture is possible, only give this option
        move = {}
        for init_pos, end_pos in possible_moves.items():
            if len(end_pos) > 0:
                move[init_pos] = end_pos
        if len(move) != 0:
            possible_moves = move

        return possible_moves, piece

    def forced_capture(self, piece):
        # This method takes the possible moves and decides if a forced capture is possible
        # @pararms - a piece object
        # @return forced cap - the forced capture of the piece
        # @return other_forced_cap - there is another forced capture avaialble
        all_pieces = self.iterpieces(piece.colour)
        forced_cap = True
        other_forced_cap = False
        current_piece_capture = False
        for temp_piece in all_pieces:
            valid_moves = self.generate_moves(temp_piece)
            for move, capture_list in valid_moves[0].items():
                if len(capture_list) > 0:
                    if temp_piece.row != piece.row or temp_piece.col != piece.col:
                        other_forced_cap = True
                    if temp_piece.row == piece.row and temp_piece.col == piece.col:
                        current_piece_capture = True

        if other_forced_cap and not current_piece_capture:
            forced_cap = False

        return forced_cap, other_forced_cap

    def _move_left(self, init, end, step, colour, left, jumped=[]):
        # This method takes a piece and generates the moves to the left of it diagonally
        # @pararms - init - start position
        # @pararms - end - stop position
        # @pararms - step - if jumped over
        # @pararms - colour - colour of piece
        # @pararms - left - moving left
        # @pararms - jumped - if a piece has been jumped - used for multi-leg
        # @return moves - the available moves to the left

        moves = {}
        last = []

        # check if within bounds
        for r in range(init, end, step):
            if left < 0:
                break

            # get current position
            current = self.board[r][left]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moves[(r, left)] = last + jumped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, rows)
                    moves.update(self._move_left(r + step, row, step, colour, left - 1, jumped=last))
                    moves.update(self._move_right(r + step, row, step, colour, left + 1, jumped=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _move_right(self, init, end, step, colour, right, jumped=[]):
        # This method takes a piece and generates the moves to the left of it diagonally
        # @pararms - init - start position
        # @pararms - end - end position
        # @pararms - step - if jumped over
        # @pararms - colour - colour of piece
        # @pararms - left - moving right
        # @pararms - jumped - if a piece has been jumped - used for multi-leg
        # @return moves - the available moves to the right
        moves = {}
        last = []

        # check if within bounds
        for r in range(init, end, step):
            if right >= columns:
                break

            # get current position
            current = self.board[r][right]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moves[(r, right)] = last + jumped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, rows)
                    moves.update(self._move_left(r + step, row, step, colour, right - 1, jumped=last))
                    moves.update(self._move_right(r + step, row, step, colour, right + 1, jumped=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]

            right += 1

        return moves

    def winner(self):
        # determines if there is a winner or not
        # @return the colour of the winner - if no winner - returns none
        if self.black_pieces <= 0:
            return white
        if self.white_pieces <= 0:
            return black
        return None

