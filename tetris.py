import pygame
import random


class SetupGame:
    """ This class manages the all game events and configures Pygame. """

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.timer = pygame.time.get_ticks()
        # define speed for tetromino frame rate
        # usually 500
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
        self.static_blocks = pygame.sprite.Group()
        self.gameplay()

    def loop(self):
        """ The game loop. """

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
        for blocks in self.static_blocks.sprites():
            blocks.draw(self.game_display)

        # check for collision with current tetromino
        if self.current_tetromino.collision_detection(self.static_blocks.sprites()):
            self.stop_tetromino(self.current_tetromino)

        # check to see if current tetromino has stopped moving
        if self.timer < (pygame.time.get_ticks() - self.framerate):
            if self.current_tetromino.gravity():
                # if tetromino is stopped
                self.stop_tetromino(self.current_tetromino)
                for block in self.current_tetromino.blocks.sprites():
                    print("added block to static_blocks")
                    self.static_blocks.add(block)
                self.gameplay()
            self.timer = pygame.time.get_ticks()

        self.clock.tick(60)

    def gameplay(self):
        """ Puts the upcoming Tetromino into play, and creates a new upcoming tetromino. """

        self.current_tetromino = None
        if self.current_tetromino is None:
            if self.next_tetromino is None:
                self.current_tetromino = Tetromino(self.colour_list, self.game_display)
                self.current_tetromino.set_play_coordinates()

                # create a upcoming tetromino
                self.next_tetromino = Tetromino(self.colour_list, self.game_display)
            else:
                self.current_tetromino = self.next_tetromino
                self.current_tetromino.set_play_coordinates()
                # create a upcoming tetromino
                self.next_tetromino = Tetromino(self.colour_list, self.game_display)

    def event_handling(self):
        """ This handles all keyboard and mouse events from user """

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

    @staticmethod
    def stop_tetromino(tetromino):
        """ Stops the current tet and moves the gameplay on. """

        # todo - when a tet stops, break down to just the blocks
        if not tetromino.stationary:
            tetromino.current_tetromino = False
            tetromino.stationary = True
        # todo - also need to be added to static_blocks group


class Hitbox(pygame.sprite.Sprite):
    """ Used for collision detection. """

    def __init__(self, width, height, xy, surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill((10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.game_display = surface

    def draw(self):
        surface_blit = self.game_display.blit
        surface_blit(self.image, self.rect)


class Block(pygame.sprite.Sprite):
    """ Creates one of the four 39*39 pixel blocks which a Tetromino is made up of. """

    def __init__(self, colour, identification, surface):
        pygame.sprite.Sprite.__init__(self)
        self.ID = identification
        self.image = pygame.Surface([39, 39])
        self.border = pygame.Surface([35, 35])
        self.rect = self.image.get_rect()
        self.light_colour, self.dark_colour = colour
        self.image.fill(self.light_colour)
        self.border.fill(self.dark_colour)

        # create the hitboxes
        self.y_hitbox = Hitbox(20, 50, (40, 40), surface)
        # self.x_hitbox = Hitbox(50, 20, (self.rect.x-5, self.rect.y+20), surface)

    def set_hitbox_position(self, xy):
        x, y = xy
        self.y_hitbox.rect.x = x+20
        self.y_hitbox.rect.y = y-5

        # todo - add other hitbox

    def draw(self, surface, xy=None):
        """ Draws the block to the given surface at the given co-ordinates. """

        print(self.y_hitbox.rect.x, self.y_hitbox.rect.y)

        surface_blit = surface.blit
        if xy is None:
            self.image.blit(self.border, (2, 2))
            surface_blit(self.image, self.rect)
        else:
            self.rect.x, self.rect.y, = xy
            self.image.blit(self.border, (2, 2))
            surface_blit(self.image, self.rect)

        self.y_hitbox.draw()

    def collision_detection(self, group) -> bool:
        """ Will check group of tetrominoes to see if we collide with any. """

        # todo - this is breaking the game...

        for block in group:
            if self.y_hitbox.rect.colliderect(block.y_hitbox.rect):
                print("Hit...")
                return True


class Tetromino(pygame.sprite.Sprite):
    """ By creating four instances of Block this class builds the random Tetromino. """

    def __init__(self, colours, surface):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = 40
        self.image = pygame.Surface([160, 160])
        self.rect = self.image.get_rect()
        self.colour = random.choice(colours)
        self.current_tetromino = False
        self.stationary = False
        self.game_display = surface

        # set co-ordinates for preview box
        self.rect.x = -20
        self.rect.y = -20
        self.blocks = pygame.sprite.Group()
        self.create_blocks(self.game_display)
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

    def create_blocks(self, surface):
        for i in range(4):
            new_block = Block(self.colour, i, surface)
            self.blocks.add(new_block)

    def set_play_coordinates(self):
        """ Generates the first co-ordinates for the tetromino. """

        # while loop stops tetromino being placed outside the box
        done = False
        while not done:
            temporary_x = random.choice(range(0, 8 * self.block_size, self.block_size))
            for block in self.blocks.sprites():
                if block.rect.x < 0:
                    continue
                if block.rect.x + self.block_size >= 10 * self.block_size:
                    continue
                self.rect.x = temporary_x
                done = True

        self.rect.y = -40
        self.current_tetromino = True

    def rotate(self):
        """ Rotates the tetromino. """

        if self.current_tetromino:
            if self.current_rotation == len(self.shape_dictionary.get(self.shape)) - 1:
                self.current_rotation = 0
            else:
                self.current_rotation += 1
        else:
            pass

    def move_left(self):
        """ Moves the tetromino to the left, to the left. """

        if self.current_tetromino:
            for block in self.blocks.sprites():
                # Don't go outside the box
                if block.rect.x <= 0:
                    return
            else:
                self.rect.x -= self.block_size

    def move_right(self):
        """ Moves the tetromino to the right. """

        if self.current_tetromino:
            for block in self.blocks.sprites():
                # Don't go outside the box
                if block.rect.x + self.block_size >= 10 * self.block_size:
                    return
            else:
                self.rect.x += self.block_size

    def gravity(self) -> bool:
        """ Moves the tetromino down the screen.
            Returns True if the tetromino is stationary. """

        for block in self.blocks.sprites():
            if block.rect.y + 40 >= 18 * self.block_size:
                return True
        if not self.stationary:
            self.rect.y += self.block_size

    def collision_detection(self, group):

        # todo - fix collision detection
        if self.stationary:
            return
        elif not self.current_tetromino:
            return

        for block in self.blocks:
            if block.collision_detection(group):
                return True

    def draw(self, surface):
        """ Places the blocks according to the tetrominoes shape, and calls the blocks draw() method. """

        # set the position of the hitbox
        for block in self.blocks.sprites():
            block.set_hitbox_position((self.rect.x, self.rect.y))

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
                            block.draw(surface, (x, y))
                            x += block_size
                    i += 1
            x = self.rect.x
            y += block_size


if __name__ == "__main__":

    new_game = SetupGame()

    while True:
        new_game.loop()
