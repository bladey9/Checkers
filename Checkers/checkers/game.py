from .fixedvar import space
from checkers.board import Board, Piece
from menu import *
pygame.font.init


class Game:
    # has all the functions for the gameplay
    def __init__(self, window, surface):
        pygame.init()
        self.running, self.playing = True, False
        self.ai_difficulty = 1  # initial AI difficulty
        # initialise all keys to False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY = False, False, False, False, False
        self.display = pygame.Surface((width + 200,height))
        self.font_name = pygame.font.get_default_font() # initial pygame font
        self.main_menu = MainMenu(self)
        self.options = RulesMenu(self)
        self.curr_menu = self.main_menu
        self.window = window
        self._init()
        self.surface = surface # used for displaying extra text
        self.padding = 40
        self.outline = 2

    def update(self):
        # updates the board
        self.board.draw(self.window)
        self.draw_faded_move(self.valid_moves, self.piece)
        pygame.display.update()

    def _init(self):
        # initialise these variables
        self.selected = None
        self.board = Board()
        self.turn = black
        self.valid_moves = {}
        self.piece = Piece(0, 0, black)

    def game_loop(self):
        # loop the game and choose between menu and actual game
        # @return self.playing - to decide whether the game shall start
        while self.playing:
            self.input()
            # if pressed, the game moves menu
            if self.START_KEY:
                self.playing = False
            self.display.fill(black)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
            return self.playing

    def input(self):
        # gets the input from the window to determine where the window should move to
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        # resets the keys everytime after one is pressed
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y, colour = brown):
        # draws the text for the menu
        # @params text - the text chosen, size, x - x position, y - y position, colour
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def winner(self):
        # @return the board winner
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        # select the row and column the player has chosen
        # @params - the row and col of the selected spot
        # return True if selection is possible. e.g if a piece is chosen, false otherwise, if out of board,
        # then no selection

        # stay within the boundaries for selection
        if row <=8 and col <= 8:
            no_int = True
            piece = self.board.get_piece(row, col)

            # if piece is not a instance of int, e.g if it is an object and not nothing
            if not isinstance(piece, int):
                forced_cap, other_capture = self.board.forced_capture(piece)[0], self.board.forced_capture(piece)[1]
                no_int = False
            if self.selected:
                result = self._move(row, col)
                if not result and not no_int:

                    # if forced capture available select another piece is not available
                    if forced_cap and not other_capture:
                        self.selected = None
                        self.select(row, col)

            if piece != 0 and piece.colour == self.turn and forced_cap:
                self.selected = piece
                self.valid_moves, self.piece = self.board.generate_moves(piece)

                return True

            return False

        else:
            None

    def _move(self, row, col):
        # move the actual piece
        # @params row, col
        # @return true if piece is able to have moved
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            piece_jumped = self.valid_moves[(row, col)]

            # if the piece jumped is a king, the piece that jumped over automatically becomes a king
            if piece_jumped:
                for skip in piece_jumped:
                    if skip.king:
                        self.board.move(self.selected, row, col, 1)
                self.board.remove_piece(piece_jumped)
            self.switch_turn()
        else:
            return False

        return True

    def draw_faded_move(self, moves, piece):
        # draw the possible moves when a piece is selected
        # @params moves - the potential moves a piece can do
        # @params piece - the piece chosen to do the move

        for move in moves:
            row, col = move

            # create a smaller checker in the proposed space with a highlighted box

            self.window.blit(self.surface, (col * space + space // 2 - 50, row * space + space // 2 - 50))
            radius = space // 2 - self.padding
            pygame.draw.circle(self.window, piece.colour, (col * space + space // 2, row * space + space // 2), radius + 24 * 0.5 + self.outline)
            pygame.draw.circle(self.window, grey, (col * space + space // 2, row * space + space // 2), radius + 20 * 0.5 + self.outline)
            pygame.draw.circle(self.window, piece.colour, (col * space + space // 2, row * space + space // 2), radius + 16 * 0.5 + self.outline)
            pygame.draw.circle(self.window, grey, (col * space + space // 2, row * space + space // 2), radius + 12 * 0.5 + self.outline)
            pygame.draw.circle(self.window, piece.colour, (col * space + space // 2, row * space + space // 2), radius + 8 * 0.5 + self.outline)
            pygame.draw.circle(self.window, grey, (col * space + space // 2, row * space + space // 2), radius + 4 * 0.5 + self.outline)
            pygame.draw.circle(self.window, grey, (col * space + space // 2, row * space + space // 2), radius + self.outline)

    def switch_turn(self):
        # change the turn of the game
        self.valid_moves = {}
        if self.turn == black:
            self.turn = white
        else:
            self.turn = black

    def get_board(self):
        #@return the board object
        return self.board

    def ai_turn(self, board):
        # ai moves
        # @params board object
        self.board = board
        self.switch_turn()




