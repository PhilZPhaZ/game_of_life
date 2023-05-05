""" This is a game of life

This is a game of life
"""
import itertools
import sys
import os
import threading
import time
import termcolor
import pygame
import pygame_gui
from blessings import Terminal


class Board:
    """ Game of life core

    This is the game of life core and you can use whatever render you would like to use
    """

    def __init__(self, width, height):
        """__init__ Init method to create the grid

        The grid is created and it is ready to use
        """
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        self.frame = 0
        self.frames = {}

    def update(self):
        """update Call this method and the grid is updated

        Here is the core of the project and the grid is updated with the rules of the game of life
        """
        self.frames[self.frame] = self._cells
        _new = []
        for x_cell, line in enumerate(self._cells):
            _new_line = []
            for y_cell, _ in enumerate(line):
                cells_alive = self.search_neighbors(x_cell, y_cell)
                if cells_alive == 2:
                    _new_line.append(self._cells[x_cell][y_cell])
                elif cells_alive == 3:
                    _new_line.append(1)
                else:
                    _new_line.append(0)
            _new.append(_new_line)
        self._cells = _new
        self.frame += 1

    def search_neighbors(self, x_cell: int, y_cell: int) -> int:
        """search_neighbors Search for all neighbors around a cell and count it

        For each cell in the grid, I just search for all the neighbors around it and count it

        Args:
            x_cell (int): x coord of the cell
            y_cell (int): y coord of the cell

        Returns:
            int: return the number of neighbors which are alive
        """
        return sum(
            self._cells[k][l]
            for k, l in itertools.product(
                range(max(0, x_cell - 1), min(x_cell + 2, len(self._cells))),
                range(max(0, y_cell - 1),
                      min(y_cell + 2, len(self._cells[0]))),
            )
            if (k, l) != (x_cell, y_cell)
        )

    def back(self):
        if self.frame == 0:
            return self._cells
        self.frame -= 1
        self._cells = self.frames[self.frame]
        self._cells.pop()
        return self._cells

    def setup(self) -> None:
        """basic Here you can pre-configure the grid

        With this method you can configure the grid before it is used in the game of life
        """
        self._cells[5][1] = 1
        self._cells[5][2] = 1
        self._cells[6][1] = 1
        self._cells[6][2] = 1
        self._cells[5][11] = 1
        self._cells[6][11] = 1
        self._cells[7][11] = 1
        self._cells[4][12] = 1
        self._cells[3][13] = 1
        self._cells[3][14] = 1
        self._cells[8][12] = 1
        self._cells[9][13] = 1
        self._cells[9][14] = 1
        self._cells[6][15] = 1
        self._cells[4][16] = 1
        self._cells[5][17] = 1
        self._cells[6][17] = 1
        self._cells[7][17] = 1
        self._cells[6][18] = 1
        self._cells[8][16] = 1
        self._cells[3][21] = 1
        self._cells[4][21] = 1
        self._cells[5][21] = 1
        self._cells[3][22] = 1
        self._cells[4][22] = 1
        self._cells[5][22] = 1
        self._cells[2][23] = 1
        self._cells[6][23] = 1
        self._cells[1][25] = 1
        self._cells[2][25] = 1
        self._cells[6][25] = 1
        self._cells[7][25] = 1
        self._cells[3][35] = 1
        self._cells[4][35] = 1
        self._cells[3][36] = 1
        self._cells[4][36] = 1

    def get_grid(self) -> list:
        """get_grid Return the grid

        The method return the grid

        Returns:
            list: Return the grid
        """
        return self._cells


class GameTerminal:
    """ The game of life is printed on the terminal

    The game of life is printed on the terminal
    """

    def __init__(self, width, height, iter):
        """__init__ The game of life is displayed on the terminal

        When you call the GameTerminal, the game of life is displayed on the terminal
        """
        self.iter = iter
        self.width = width
        self.height = height
        self.board = Board(self.width, self.height)
        self.terminal = Terminal()

    def print_board(self, grid):
        """print_board Print the board

        The board is printed

        Args:
            grid (list): The list to be printed
        """
        # Déplacer le curseur au coin supérieur gauche du terminal
        print(self.terminal.move(0, 0))

        # Parcourir les éléments de la grille
        for row in grid:
            for cell in row:
                # Si la cellule est vivante, la colorer en vert
                if cell == 1:
                    print(termcolor.colored('\u25A0', 'red'), end=' ')
                # Sinon, la laisser en blanc
                else:
                    print('\u25A0', end=' ')
            # Aller à la ligne suivante
            print()
        # Ajouter une pause pour que l'utilisateur ait le temps de voir la grille
        time.sleep(.5)

    def function_app(self):
        """function_app launch the app

        Launch the app
        """
        for _ in range(self.iter):
            cells = self.board.get_grid()
            self.board.update()
            self.print_board(cells)


class GameWindow():
    """ The game of life is display on a pygame display

    The game of life is display on a pygame display
    """

    def __init__(self, width, height) -> None:
        """__init__ The game of life is display on a pygame window

        The game of life is display in a pygame window

        Args:
            width (int): number of cells on x axis
            height (int): number of cells on y axis
        """
        self.width = width
        self.height = height
        self.board = Board(self.width, self.height)
        self.grid_cell_width = 10
        self.grid_cell_height = 10
        # Initialisation de pygame
        pygame.init()
        self.logo = pygame.image.load(
            os.path.join(os.getcwd(), 'assets', 'logo.png'))
        self.display = pygame.display.set_mode(
            (width*self.grid_cell_width+400, height*self.grid_cell_height))
        pygame.display.get_surface().fill((100, 100, 100))
        pygame.display.set_caption("Game of life")
        pygame.display.set_icon(self.logo)
        self.clock = pygame.time.Clock()
        self.gui()
        self.visualize = threading.Thread(target=self.update_screen).start()
        self.auto_update = threading.Thread(target=self.auto_update)

    def update_screen(self):
        while True:
            cells = self.board.get_grid()
            self.visualization(cells)
            pygame.display.flip()

    def auto_update(self):
        while self.run:
            self.board.update()

    def gui(self):
        self.manager = pygame_gui.UIManager(
            (self.width*self.grid_cell_width+400, self.height*self.grid_cell_height))

        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 0), (300, 50)),
            text="Game of life",
            manager=self.manager
        )

        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 50), (300, 50)),
            text='Generation precedente',
            manager=self.manager,
        )

        self.number_generation_button = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 110), (300, 50)),
            manager=self.manager
        )

        self.start_generation_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 170), (300, 50)),
            text='Lancer la generation automatique',
            manager=self.manager,
        )

        self.start_auto_generation = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 230), (300, 50)),
            text='Generation en continue',
            manager=self.manager,
        )
        
        self.stop_auto_generation = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.width*self.grid_cell_width+50, 290), (300, 50)),
            text='Arreter la generation en continue',
            manager=self.manager,
        )

    def create_square(self, xpos, ypos, color):
        """create_square create a square

        This method create a square on the pygame display with the grid of the game of life

        Args:
            xpos (int): position x of the cell
            ypos (int): position y of the cell
            color (tuple): the color of the cell
        """
        pygame.draw.rect(self.display, color, [
                         xpos, ypos, self.grid_cell_width, self.grid_cell_height])

    def visualization(self, grid):
        """visualization Visualize 1 frame of the grid

        This method draw 1 frame of the game of life grid

        Args:
            grid (list): grid of the game of life
        """
        y_screen = 0  # we start at the top of the screen
        for row in grid:
            x_screen = 0  # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.create_square(x_screen, y_screen, (255, 255, 255))
                else:
                    self.create_square(x_screen, y_screen, (0, 0, 0))
                # for ever item/number in that row we move one "step" to the right
                x_screen += self.grid_cell_width
            # for every new row we move one "step" downwards
            y_screen += self.grid_cell_height
        time.sleep(.05)

    def setup(self):
        self.board.setup()

    def listen_event(self, event):
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            self.board.update()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) or (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.back_button):
            cells = self.board.back()
            # self.visualization(cells)
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.number_generation_button:
            self.number_of_generation = event.text
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_generation_button:
            try:
                for _ in range(int(self.number_of_generation)):
                    self.board.update()
            except (TypeError, AttributeError):
                print('erreur')
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_auto_generation:
            self.run = True
            self.auto_update.start()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.stop_auto_generation:
            self.run = False
        self.manager.process_events(event)

    def function_app(self):
        """function_app Start the application

        Start the application
        """
        while True:
            time_delta = self.clock.tick(60)/1000
            for event in pygame.event.get():
                self.listen_event(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.display)


game = GameWindow(80, 80)
game.setup()
game.function_app()
