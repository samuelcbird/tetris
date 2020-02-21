import pygame
import random


class SetupGame:
    """ This class manages the all game events and configures Pygame. """

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.block = 40
        self.main_window_width_height = (22*self.block, 20*self.block)
        self.main_window = pygame.display.set_mode(self.main_window_width_height)
        pygame.display.set_caption("Tetris")

        # define colours
        self.dark_blue, self.light_blue = (40, 63, 128), (156, 182, 255)
        self.dark_purple, self.light_purple = (77, 48, 128), (202, 171, 255)
        self.dark_pink, self.light_pink = (128, 29, 93), (255, 135, 213)
        self.dark_orange, self.light_orange = (204, 65, 18), (255, 138, 99)
        self.default_grey = (192, 192, 192)
        self.off_white = (240, 240, 240)
        self.dark_grey = (10, 10, 10)
        self.colour_list = [(self.dark_blue, self.light_blue), (self.dark_purple, self.light_purple), (self.dark_pink,
                            self.light_pink), (self.dark_orange, self.light_orange)]

        # create surfaces for different displays
        self.main_window.fill(self.default_grey)
        self.game_display = pygame.Surface((10*self.block, 18*self.block))
        self.game_display.fill((240, 240, 240))
        self.next_tetromino_display = pygame.Surface((4*self.block, 5*self.block))
        self.next_tetromino_display.fill(self.dark_grey)

        # gameplay variables
        self.current_tetromino = None
        self.next_tetromino = None
        self.static_tetrominoes = pygame.sprite.Group()
        self.gameplay()

    def loop(self):
        self.event_handling()
        pygame.display.update()
        self.main_window.blit(self.game_display, (6*self.block, 1*self.block))
        self.main_window.blit(self.next_tetromino_display, (17*self.block, 1*self.block))

        self.game_display.fill(self.off_white)
        self.next_tetromino_display.fill(self.dark_grey)

        self.current_tetromino.draw(self.game_display)
        # self.current_tetromino.gravity()
        self.next_tetromino.draw(self.next_tetromino_display)

        self.clock.tick(60)

    def gameplay(self):
        if self.current_tetromino is None:
            self.current_tetromino = Tetromino(self.colour_list)
            self.current_tetromino.next_tetromino = False
            self.current_tetromino.current_tetromino = True
            self.current_tetromino.set_play_coordinates()
            self.next_tetromino = Tetromino(self.colour_list)
            # while self.current_tetromino is not None:
            #     pass

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # todo - configure space bar rotation
                self.current_tetromino.rotate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass


class Block(pygame.sprite.Sprite):
    """ Creates one of the four 39*39 pixel blocks which a Tetromino is made up of. """

    def __init__(self, colour, identification):
        pygame.sprite.Sprite.__init__(self)
        self.ID = identification
        self.image = pygame.Surface([39, 39])
        self.border = pygame.Surface([35, 35])
        self.rect = self.image.get_rect()
        self.light_colour, self.dark_colour = colour
        self.image.fill(self.light_colour)
        self.border.fill(self.dark_colour)

    def draw(self, xy, surface):
        self.rect.x, self.rect.y, = xy
        surface_blit = surface.blit
        self.image.blit(self.border, (2, 2))
        surface_blit(self.image, self.rect)


class Tetromino(pygame.sprite.Sprite):
    """ By creating four instances of Block this class builds the random Tetromino. """

    def __init__(self, colours):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = 40
        self.image = pygame.Surface([160, 160])
        self.rect = self.image.get_rect()
        self.colour = random.choice(colours)
        self.next_tetromino = True
        self.current_tetromino = False

        # set co-ordinates for preview box
        self.rect.x = -20
        self.rect.y = -20
        self.blocks = pygame.sprite.Group()
        self.create_blocks()
        # holds the current rotation
        self.current_rotation = 0

        # get the random shape
        self.shape = random.choice(["L", "J", "I", "T", "S", "Z", "O"])
        self.shape_dictionary = {"L": [["-----",
                                        "-B---",
                                        "-B---",
                                        "-BB--",
                                        "-----"],
                                       ["-----",
                                        "BBB--",
                                        "B----",
                                        "-----",
                                        "-----"],
                                       ["-----",
                                        "-BB--",
                                        "--B--",
                                        "--B--",
                                        "-----"],
                                       ["-----",
                                        "---B-",
                                        "-BBB-",
                                        "-----",
                                        "-----"]],
                                 "J": [["-----",
                                        "---B-",
                                        "---B-",
                                        "--BB-",
                                        "-----"],
                                       ["-----",
                                        "-----",
                                        "B----",
                                        "BBB--",
                                        "-----"],
                                       ["-----",
                                        "-BB--",
                                        "-B---",
                                        "-B---",
                                        "-----"],
                                       ["-----",
                                        "-----",
                                        "-BBB-",
                                        "---B-",
                                        "-----"]],
                                 "I": [["-----",
                                        "--B--",
                                        "--B--",
                                        "--B--",
                                        "--B--"],
                                       ["-----",
                                        "-----",
                                        "-----",
                                        "-BBBB",
                                        "-----"]],
                                 "T": [["-----",
                                        "-BBB-",
                                        "--B--",
                                        "-----",
                                        "-----"],
                                       ["-----",
                                        "--B--",
                                        "-BB--",
                                        "--B--",
                                        "-----"],
                                       ["-----",
                                        "--B--",
                                        "-BBB-",
                                        "-----",
                                        "-----"],
                                       ["-----",
                                        "--B--",
                                        "--BB-",
                                        "--B--",
                                        "-----"]],
                                 "S": [["-----",
                                        "--BB-",
                                        "-BB--",
                                        "-----",
                                        "-----"],
                                       ["-B---",
                                        "-BB-",
                                        "--B--",
                                        "-----",
                                        "-----"]],
                                 "Z": [["-----",
                                        "-BB--",
                                        "--BB-",
                                        "-----",
                                        "-----"],
                                       ["---B-",
                                        "--BB-",
                                        "--B--",
                                        "-----",
                                        "-----"]],
                                 "O": [["-----",
                                        "-BB--",
                                        "-BB--",
                                        "-----",
                                        "-----"]]
                                 }

    def create_blocks(self):
        for i in range(4):
            new_block = Block(self.colour, i)
            self.blocks.add(new_block)

    def set_play_coordinates(self):
        self.rect.x = random.choice(range(0, 8*self.block_size, self.block_size))
        self.rect.y = 20
        self.next_tetromino = False
        self.current_tetromino = True

    def rotate(self):
        if not self.next_tetromino:
            if self.current_rotation == len(self.shape_dictionary.get(self.shape)) - 1:
                self.current_rotation = 0
            else:
                self.current_rotation += 1
        else:
            pass

    def gravity(self):
        self.rect.y += self.block_size

    def draw(self, surface):
        x, y = self.rect.x, self.rect.y
        block_size = 40
        i = 0
        for string in self.shape_dictionary.get(self.shape)[self.current_rotation]:
            for char in string:
                if char == '-':
                    x += block_size
                elif char == "B":
                    for block in self.blocks.sprites():
                        if block.ID == i:
                            block.draw((x, y), surface)
                            x += block_size
                    i += 1
            x = self.rect.x
            y += block_size


if __name__ == "__main__":

    new_game = SetupGame()

    while True:
        new_game.loop()
