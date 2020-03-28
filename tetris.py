import pygame
import random


class SetupGame:
    """ This class manages the all game events and configures Pygame. """

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.timer = pygame.time.get_ticks()
        # define speed for tetromino frame rate
        self.framerate = 500
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
        # display for gameplay
        self.main_window.blit(self.game_display, (6*self.block, 1*self.block))
        # display for upcoming tetromino
        self.main_window.blit(self.next_tetromino_display, (17*self.block, 1*self.block))

        # fill displays with background colour
        self.game_display.fill(self.off_white)
        self.next_tetromino_display.fill(self.dark_grey)

        # draw current, upcoming tetromino and stationary tetrominoes
        self.current_tetromino.draw(self.game_display)
        self.next_tetromino.draw(self.next_tetromino_display)
        for tetromino in self.static_tetrominoes.sprites():
            tetromino.draw(self.game_display)

        # check for collision with current tetromino
        if self.current_tetromino.collision_detection(self.static_tetrominoes):
            self.stop_tetromino(self.current_tetromino)

        if self.timer < (pygame.time.get_ticks() - self.framerate):
            if self.current_tetromino.gravity():
                self.stop_tetromino(self.current_tetromino)
            self.timer = pygame.time.get_ticks()

        self.clock.tick(60)

    def gameplay(self):
        # todo - fix upcoming tetromino bug

        if self.current_tetromino is None:
            if self.next_tetromino is None:
                self.current_tetromino = Tetromino(self.colour_list)
                self.current_tetromino.set_play_coordinates()

                # create a upcoming tetromino
                self.next_tetromino = Tetromino(self.colour_list)
            else:
                self.current_tetromino = self.next_tetromino
                self.current_tetromino.set_play_coordinates()
                # create a upcoming tetromino
                self.next_tetromino = Tetromino(self.colour_list)


    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.current_tetromino.rotate()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.current_tetromino.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.current_tetromino.move_right()

    def stop_tetromino(self, tetromino):
        """ Stops the current tet and moves the gameplay on. """

        # todo - when a tet stops, break down to just the blocks

        if not tetromino.stationary:
            tetromino.stationary = True
        self.static_tetrominoes.add(tetromino)
        self.current_tetromino = None
        self.gameplay()


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
        # hitbox will check for collision

    def draw(self, xy, surface):
        self.rect.x, self.rect.y, = xy
        surface_blit = surface.blit
        self.image.blit(self.border, (2, 2))
        surface_blit(self.image, self.rect)

    def collision_detection(self, group) -> bool:
        """ Will check group of tetrominoes to see if we collide with any. """

        for tetromino in group.sprites():
            for block in tetromino.blocks.sprites():
                if block.rect.x == self.rect.x and block.rect.y == self.rect.y + 1:
                    # todo - fix collision detection
                    return True


class Tetromino(pygame.sprite.Sprite):
    """ By creating four instances of Block this class builds the random Tetromino. """

    def __init__(self, colours):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = 40
        self.image = pygame.Surface([160, 160])
        self.rect = self.image.get_rect()
        self.colour = random.choice(colours)
        self.current_tetromino = False
        self.stationary = False

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
        self.rect.y = -40
        self.current_tetromino = True

    def rotate(self):
        if self.current_tetromino:
            if self.current_rotation == len(self.shape_dictionary.get(self.shape)) - 1:
                self.current_rotation = 0
            else:
                self.current_rotation += 1
        else:
            pass

    def move_left(self):
        if self.current_tetromino:
            for block in self.blocks.sprites():
                if block.rect.x <= 0:
                    return
            else:
                self.rect.x -= self.block_size

    def move_right(self):
        if self.current_tetromino:
            for block in self.blocks.sprites():
                if block.rect.x + 40 >= 10 * self.block_size:
                    return
            else:
                self.rect.x += self.block_size

    def gravity(self) -> bool:
        for block in self.blocks.sprites():
            if block.rect.y + 40 >= 18 * self.block_size:
                return True
        if not self.stationary:
            self.rect.y += self.block_size

    def collision_detection(self, group):
        for block in self.blocks.sprites():
            if block.collision_detection(group):
                self.stationary = True
                return self.stationary

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
