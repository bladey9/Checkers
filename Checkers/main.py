
import pygame
from checkers.fixedvar import space, white, surface, black
from checkers.game import Game
from checkers.minimax import minimax

# set the window of the game
window = pygame.display.set_mode((1000, 800))
# set the title
pygame.display.set_caption('Checkers Game')
FPS = 60
# set the surface
surface = surface


def main():
    # method to run the game

    # display menu
    run = False
    game = Game(window, surface)
    while game.running:

        game.curr_menu.display_menu()
        game.game_loop()
        if game.playing:
            run = True
            break

    clock = pygame.time.Clock()

    # if run is True, the game should start
    while run:
        clock.tick(FPS)

        # minimax set on the white colour
        if game.turn == white:
            value, new_board = minimax(game.get_board(), game.ai_difficulty + 1, float('-inf'), float('inf'), white, game)
            game.ai_turn(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_position(pos)
                if row <8 and col <8:
                    game.select(row, col)

        game.update()

    pygame.quit()

def get_position(pos):
    # get the position of the mouse on the board
    x, y = pos
    row = y // space
    col = x // space
    return row, col

main()
