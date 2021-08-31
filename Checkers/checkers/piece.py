import pygame
from .fixedvar import black, space, grey, king, black_winner
# piece class

class Piece:
    #class handles all the piece object functions
    def __init__(self, row, col, colour):
        self.padding = 40
        self.outline = 2
        self.row = row
        self.col = col
        self.colour = colour
        self.king = False

        # used for determining the direction a piece can move
        if self.colour == black:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.piece_position()

    def piece_position(self):
        # determine the piece position
        self.x = space * self.col + space // 2
        self.y = space * self.row + space // 2

    def make_king(self):
        # make the piece a king
        self.king = True

    def draw_piece(self, window, n=1, hint=0):
        # draw the actual piece in the window
        # @params window - the window
        # @params n - a int to determine how smaller the circle radius should go - visual purposes

        # draw the piece
        radius = space // 2 - self.padding
        pygame.draw.circle(window, self.colour, (self.x, self.y), radius + 24 * n + self.outline)
        pygame.draw.circle(window, grey, (self.x, self.y), radius + 20 * n + self.outline)
        pygame.draw.circle(window, self.colour, (self.x, self.y), radius + 16 * n+ self.outline)
        pygame.draw.circle(window, grey, (self.x, self.y), radius + 12* n + self.outline)
        pygame.draw.circle(window, self.colour, (self.x, self.y), radius + 8 * n+ self.outline)

        # if not king, draw extra circles
        if not self.king:
            pygame.draw.circle(window, grey, (self.x, self.y), radius + 4 * n + self.outline)
            pygame.draw.circle(window, grey, (self.x, self.y), radius + self.outline)

        # if king, draw the image on top
        if self.king:
            window.blit(king, (self.x - king.get_width() // 2, self.y - king.get_height() // 2))



    def move(self, row, col):
        # method to move the piece to that row, col and calc the position afterwards
        self.row = row
        self.col = col
        self.piece_position()

    def __repr__self(self):
        return str(self.colour)



