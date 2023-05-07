""" This is a game of life

This is a game of life
"""
import itertools
import sys
import os
import threading
import pygame
import pygame_gui

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
        self.speed_generation = 1
        self.run = threading.Event()
        # Initialisation de pygame
        pygame.init()
        self.logo = pygame.image.load(
            os.path.join(os.getcwd(), 'assets', 'logo.png'))
        self.display = pygame.display.set_mode(
            (width*self.grid_cell_width+400, height*self.grid_cell_height))
        self.background = pygame.Surface((width*self.grid_cell_width+400, height*self.grid_cell_height))
        pygame.display.set_caption("Game of life")
        pygame.display.set_icon(self.logo)
        self.clock = pygame.time.Clock()
        self.gui()
        # On creer le thread pour gerer l'affichage de la grille
        self.visualize_thread = threading.Thread(target=self.update_screen)
        self.visualize_thread.start()

    def update_screen(self):
        while True:
            cells = self.board.get_grid()
            self.visualization(cells)

    def auto_update(self):
        while self.run.is_set():
            self.board.update()
            pygame.time.wait(self.speed_generation)

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
            manager=self.manager
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
        self.set_speed_slider = pygame_gui.elements.UIHorizontalSlider(
            start_value=1,
            value_range=(1, 100),
            relative_rect=pygame.Rect((self.width*self.grid_cell_width+50, 350), (300, 50)),
            manager=self.manager
        )
        self.set_speed_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width*self.grid_cell_width+175, 410), (50, 50)),
            text=str(self.set_speed_slider.get_current_value()),
            manager=self.manager
        )

    def create_square(self, xpos, ypos, color):
        """create_square create a square

        This method create a square on the pygame display with the grid of the game of life

        Args:
            xpos (int): position x of the cell
            ypos (int): position y of the cell
            color (tuple): the color of the cell
        """
        pygame.draw.rect(self.background, color, [
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
        pygame.time.wait(50)

    def setup(self):
        self.board.setup()

    def listen_event_auto_generation(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_auto_generation:
            self.run = threading.Event()
            self.run.set()
            self.auto_update_thread = threading.Thread(target=self.auto_update)
            self.auto_update_thread.start()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.stop_auto_generation:
            self.run.clear()

    def listen_event(self, event):
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.back_button:
            self.board.back()
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == self.number_generation_button:
            self.number_of_generation = event.text
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_generation_button:
            try:
                for _ in range(int(self.number_of_generation)):
                    self.board.update()
            except (TypeError, AttributeError):
                print('erreur')
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == self.set_speed_slider:
            self.speed_generation = event.value
            self.set_speed_text.set_text(str(event.value))
        self.manager.process_events(event)

    def listen_event_key_holded(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RIGHT]:
            self.board.update()
            pygame.time.wait(100)
        if keys[pygame.K_LEFT]:
            self.board.back()
            pygame.time.wait(100)

    def function_app(self):
        """function_app Start the application

        Start the application
        """
        self.running = True
        time_delta = self.clock.tick(60)/1000
        while self.running:
            for event in pygame.event.get():
                self.listen_event(event)
                self.listen_event_auto_generation(event)
            self.listen_event_key_holded()

            self.manager.update(time_delta=time_delta)
            
            self.display.blit(self.background, (0, 0))
            self.manager.draw_ui(self.display)
            
            pygame.display.update()

        pygame.quit()
        sys.exit()

game = GameWindow(80, 80)
game.setup()
game.function_app()
