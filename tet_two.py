import pygame
import random


class SetupGame:
    """ This class will setup and handle the running of the game. """

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        # The timer is used to regulate the speed of gameplay.
        # self.gameplay_speed can be diminished to increase the speed of gameplay.
        self.time = pygame.time.get_ticks()
        self.gameplay_speed = 500

        # Defining size of application window; includes peripherals eg, score and upcoming Tetromino
        self.main_window_size = (14*self.block_size, 19*self.block_size)
        self.main_window = pygame.display.set_mode(self.main_window_size)

        # Creating surfaces for gameplay and the display window for the next Tetromino.
        # todo - create these surfaces

        # The block size is the size of each individual block of the Tetromino
        self.block_size = 40

        # Defining colours used for the background of the games windows
        self.bg_colours = {"off_white": (240, 240, 240),
                           "light_grey": (192, 192, 192),
                           "dark_grey": (10, 10, 10)}
        # Defining colours - { "colour": ((dark), (light)) }
        self.colours = {"blue": ((40, 63, 128), (156, 182, 255)),
                        "purple": ((77, 48, 128), (202, 171, 255)),
                        "pink": ((128, 29, 93), (255, 135, 213)),
                        "orange": ((204, 65, 18), (255, 138, 99)),
                        "grey": ((10, 10, 10), (192, 192, 192))}

        # Attributes to hold the appropriate Tetromino
        self.current_tet = None
        self.next_tet = None
        # A group to hold all the blocks once they become static
        # -- After the Tetromino is stationary the Blocks will be removed and the Tetromino will be discarded.
        self.static_blocks = pygame.sprite.Group()
        # A group to hold any sprite that has been discarded (blocks, tetrominoes, hitboxes).
        # -- Anything in this group will be deleted during each iteration of the loop.
        self.discarded_sprites = pygame.sprite.Group()

        # An integer attribute to hold the points for the current game
        # A list attribute to control the increasing difficulty of the game
        # -- Integers will be used as the self.gameplay_speed attribute.
        # todo - think through the logistics of points and increasing difficulty
        points = 0
        difficulty = [500, 450, 400, 350, 300, 250, 200, 150, 50]

        def loop():
            return

        def gameplay():
            return

        def event_handling():
            return

        def gravity():
            return


if __name__ == "__main__":
    pass
