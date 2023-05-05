
import pygame
from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIHorizontalSlider


class SlideBar():
    def __init__(self, ui_manager, screen, screen_width, screen_height):
        self.ui_manager = ui_manager
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(
            (self.screen_width, self.screen_height))
        self.ui_manager.clear_and_reset()

    def create_slide_bar(self, pos_x, pos_y, init_value, min_v, max_v):
        self.test_slider = UIHorizontalSlider(
            pygame.Rect((int(pos_x),
                         int(pos_y)),
                        (240, 25)), init_value, (min_v, max_v),
            self.ui_manager, object_id='#cool_slider')
        return self.test_slider

    def update_slider(self, slide_bar):
        value_range = slide_bar.value_range[1] -\
            slide_bar.value_range[0]
        scroll_range = slide_bar.right_limit_position -\
            slide_bar.left_limit_position
        if slide_bar.left_button is not None and (
                slide_bar.left_button.held and
                slide_bar.scroll_position >
                slide_bar.left_limit_position):
            slide_bar.scroll_position -= scroll_range / value_range
            slide_bar.current_value -= 1
        elif slide_bar.right_button is not None and (
                slide_bar.right_button.held and
                slide_bar.scroll_position <
                slide_bar.right_limit_position):
            slide_bar.scroll_position += scroll_range / value_range
            slide_bar.current_value += 1


if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    ui_manager = UIManager((screen_width, screen_height),
                           PackageResource(package='data.themes',
                                           resource='theme_2.json'))
    background_surface = pygame.Surface((screen_width, screen_height))
    background_surface.fill(
        ui_manager.get_theme().get_colour('dark_bg'))
    app = SlideBar(ui_manager, screen, screen_width, screen_height)
    app.recreate_ui()
    slide_bar1 = app.create_slide_bar(100, 120, 5, 5, 10)
    running = True
    while running:

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui_manager.process_events(event)
        # respond to input
        ui_manager.update(0.001)
        app.update_slider(slide_bar1)
        print(slide_bar1.scroll_position, slide_bar1.current_value)

        # draw graphics
        screen.blit(background_surface, (0, 0))
        ui_manager.draw_ui(screen)

        pygame.display.update()