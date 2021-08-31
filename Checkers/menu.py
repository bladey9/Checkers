import pygame
from checkers.fixedvar import width, height, black, white, brown, dark_brown, light_brown, grey

#file for UI before game

class Menu():
    # main class used by mainmenu and rulesmenu to inherit.
    def __init__(self, game):
        self.width, self.height = 1000, 800
        self.game = game
        self.mid_w, self.mid_h = self.width / 2, self.height / 2
        self.run_display = True
        self.menu_cursor = pygame.Rect(0, 0, 50, 50)
        self.ai_cursor = pygame.Rect(0, 0, 50, 50)
        self.remove = - 90

    def draw_menu_cursor(self):
        # draw the asterisks symbol next to the main menu options
        self.game.draw_text('*', 50, self.menu_cursor.x, self.menu_cursor.y - 50)

    def draw_AI_cursor(self):
        # draw the underscore symbol next to the AI options
        self.game.draw_text('_', 50, self.ai_cursor.x, self.ai_cursor.y - 65)

    def update_screen(self):
        # update the screen after each key is pressed
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    # main menu class - has all the variables for the starting screen- UI
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 20
        self.rulesx, self.rulesy = self.mid_w, self.mid_h + 80
        self.aiwx, self.aiwy = self.mid_w, self.mid_h + 200

        # get the AI positions (easy, medium, hard)
        self.ai1x, self.ai1y = self.mid_w - 250, self.mid_h + 250,
        self.ai2x, self.ai2y = self.mid_w, self.mid_h + 250,
        self.ai3x, self.ai3y = self.mid_w + 250, self.mid_h + 250,

        # get the positions for the cursors
        self.menu_cursor.midtop = (self.startx - 90, self.starty + 10)
        self.ai_cursor.midtop = (self.ai1x + 25, self.ai1y + 10)

        # initialise AI level to 1
        self.ai_level = 1

    def display_menu(self):
        # displays the starting screen
        self.run_display = True
        while self.run_display:
            self.game.input()
            self.check_input()
            self.game.display.fill(dark_brown)
            self.game.draw_text('Checkers Game', 100, self.width / 2, self.height / 2 - 200)
            self.game.draw_text("Start Game", 30, self.startx, self.starty - 50)
            self.game.draw_text("Rules", 30, self.rulesx, self.rulesy - 50)
            self.game.draw_text("Choose Your AI difficulty:", 20, self.aiwx, self.aiwy - 50)
            self.game.draw_text("Easy", 20, self.ai1x, self.ai1y - 50)
            self.game.draw_text("Medium", 20, self.ai2x, self.ai2y - 50)
            self.game.draw_text("Hard", 20, self.ai3x, self.ai3y - 50)
            self.game.draw_text("Use arrow keys : DOWN, RIGHT : to move between options", 15, self.ai2x, self.ai2y + 50,
                                light_brown)
            self.game.draw_text("Use key : ENTER : to choose menu option", 15, self.ai2x, self.ai2y + 80, light_brown)
            self.draw_menu_cursor()
            self.draw_AI_cursor()
            self.update_screen()

    def move_cursor(self):
        # move the cursor
        if self.game.DOWN_KEY:

            if self.state == 'Start':
                self.menu_cursor.midtop = (self.rulesx + self.remove, self.rulesy + 10)
                self.state = 'Options'
            elif self.state == 'Options':
                self.menu_cursor.midtop = (self.startx + self.remove, self.starty + 10)
                self.state = 'Start'
        elif self.game.RIGHT_KEY:

            if self.ai_level == 1:
                self.ai_cursor.midtop = (self.ai2x + 25, self.ai2y + 10)
                self.ai_level = 2
            elif self.ai_level == 2:
                self.ai_cursor.midtop = (self.ai3x + 25, self.ai3y + 10)
                self.ai_level = 3
            elif self.ai_level == 3:
                self.ai_cursor.midtop = (self.ai1x + 25, self.ai1y + 10)
                self.ai_level = 1

    def check_input(self):
        # check what was entered to see whether the game should start or the options menu should be displayed
        self.move_cursor()
        self.game.ai_difficulty = self.ai_level
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            self.run_display = False


class RulesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.x, self.y = self.width / 2, self.height / 10
        self.movedown = 40

    def display_menu(self):
        #draw the rules menu
        self.run_display = True
        while self.run_display:
            self.game.input()
            self.check_input()
            self.game.display.fill(dark_brown)
            self.game.draw_text("Basic Gameplay", 30, self.x, self.y - 25, grey)
            self.game.draw_text("The human player controls the black pieces while the AI player controls the white.",
                                20, self.x, self.y + self.movedown - 25)
            self.game.draw_text("Pieces may only move diagonally forwards.", 20, self.x,
                                self.y + self.movedown * 2 - 25)
            self.game.draw_text("Capturing Pieces", 30, self.x, self.y + self.movedown * 3, grey)
            self.game.draw_text("Pieces can only move one square in a non-capturing move.", 20, self.x,
                                self.y + self.movedown * 4)
            self.game.draw_text("To capture an opponent's piece, a player must jump over their opponents piece", 20,
                                self.x, self.y + self.movedown * 5)
            self.game.draw_text("into an empty square. The captured piece is then removed.  ", 20, self.x,
                                self.y + self.movedown * 6 - 15)
            self.game.draw_text("A piece may make multiple captures in one move if multiple valid jumps can be made.",
                                20, self.x, self.y + self.movedown * 7 - 25)
            self.game.draw_text("A piece is forced to capture an opponent's piece if they are able to.", 20, self.x,
                                self.y + self.movedown * 8 - 25)
            self.game.draw_text("King Piece", 30, self.x, self.y + self.movedown * 9, grey)
            self.game.draw_text(
                "If a player's piece reaches the last row on their opponent's side, the piece is made a king.", 20,
                self.x, self.y + self.movedown * 10)
            self.game.draw_text("King pieces may move diagonally forwards and backwards.", 20, self.x,
                                self.y + self.movedown * 11)
            self.game.draw_text("If a non-king piece captures a king piece, that piece is automatically a king.", 20,
                                self.x, self.y + self.movedown * 12)
            self.game.draw_text("Game Objective", 30, self.x, self.y + self.movedown * 13 + 25, grey)
            self.game.draw_text("A player wins when they have captured all their opponent's pieces.", 20, self.x,
                                self.y + self.movedown * 14 + 25)
            self.game.draw_text("Use key : BACKSPACE : to go back to the menu", 15, 500, 750, )
            self.update_screen()

    def check_input(self):
        #check the input to see whether to go back to the main menu
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
