""" This is a game of life

This is a game of life
"""
import itertools
import sys
import time
import termcolor
import pygame
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
        self.basic()

    def update(self):
        """update Call this method and the grid is updated

        Here is the core of the project and the grid is updated with the rules of the game of life
        """
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
                range(max(0, y_cell - 1), min(y_cell + 2, len(self._cells[0]))),
            )
            if (k, l) != (x_cell, y_cell)
        )

    def basic(self) -> None:
        """basic Here you can pre-configure the grid

        With this method you can configure the grid before it is used in the game of life
        """
        self._cells[5+10][6+10] = 1
        self._cells[5+10][7+10] = 1
        self._cells[5+10][8+10] = 1
        self._cells[6+10][5+10] = 1
        self._cells[6+10][8+10] = 1
        self._cells[7+10][4+10] = 1
        self._cells[7+10][8+10] = 1
        self._cells[8+10][4+10] = 1
        self._cells[8+10][7+10] = 1
        self._cells[9+10][4+10] = 1
        self._cells[9+10][5+10] = 1
        self._cells[9+10][6+10] = 1

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
    def __init__(self):
        """__init__ The game of life is displayed on the terminal

        When you call the GameTerminal, the game of life is displayed on the terminal
        """
        self.board = Board(30, 30)
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
        time.sleep(.05)

    def function_app(self):
        """function_app launch the app

        Launch the app
        """
        for _ in range(100):
            cells = self.board.get_grid()
            self.board.update()
            self.print_board(cells)

class GameWindow:
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
        self.display = pygame.display.set_mode((width*self.grid_cell_width, height*self.grid_cell_height))
        pygame.display.get_surface().fill((200, 200, 200))
        pygame.display.update()

    def create_square(self, xpos, ypos, color):
        """create_square create a square

        This method create a square on the pygame display with the grid of the game of life

        Args:
            xpos (int): position x of the cell
            ypos (int): position y of the cell
            color (tuple): the color of the cell
        """
        pygame.draw.rect(self.display, color, [xpos, ypos, self.grid_cell_width, self.grid_cell_height])

    def visualization(self, grid):
        """visualization Visualize 1 frame of the grid

        This method draw 1 frame of the game of life grid

        Args:
            grid (list): grid of the game of life
        """
        y_screen = 0  # we start at the top of the screen
        for row in grid:
            x_screen = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.create_square(x_screen, y_screen, (255, 255, 255))
                else:
                    self.create_square(x_screen, y_screen, (0, 0, 0))
                x_screen += self.grid_cell_width # for ever item/number in that row we move one "step" to the right
            y_screen += self.grid_cell_height   # for every new row we move one "step" downwards
        pygame.display.update()
        time.sleep(.05)

    def function_app(self):
        """function_app launch the app

        Launch the app
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            cells = self.board.get_grid()
            self.visualization(cells)
            self.board.update()

game = GameWindow(80, 80)
game.function_app()
