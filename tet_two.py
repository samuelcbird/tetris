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

        # Defining colours used for the background of the games windows
        self.bg_colours = {"off_white": (240, 240, 240),
                           "light_grey": (192, 192, 192),
                           "dark_grey": (10, 10, 10)}
        # Defining colours - { "colour": ((dark), (light)) }
        self.colours = {"blue": ((40, 63, 128), (156, 182, 255)),
                        "purple": ((77, 48, 128), (202, 171, 255)),
                        "pink": ((128, 29, 93), (255, 135, 213)),
                        "orange": ((204, 65, 18), (255, 138, 99))}

        # The block size is the size of each individual block of the Tetromino
        self.block_size = 40

        # Defining size of application window; includes peripherals eg, score and upcoming Tetromino
        self.main_window_size = (30*self.block_size, 20*self.block_size)
        self.main_window = pygame.display.set_mode(self.main_window_size)
        self.main_window.fill(self.bg_colours.get("light_grey"))

        # Creating surfaces for gameplay and the display window for the next Tetromino.
        # todo - create these surfaces
        self.game_area = pygame.Surface((28*self.block_size, 16*self.block_size))
        self.game_area.fill(self.bg_colours.get("light_grey"))

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

        self.a_tet = Tetromino(self.block_size, self.colours)
        self.a_tet.set_x(10)
        self.a_tet.set_y(5)
        self.current_tet = self.a_tet

    def loop(self):
        self.event_handling()
        pygame.display.update()

        # Draw the game area and fill with background colour.
        self.main_window.blit(self.game_area, (1*self.block_size, 2*self.block_size))
        self.game_area.fill(self.bg_colours.get("off_white"))

        self.a_tet.draw(self.game_area)

        # Framerate
        self.clock.tick(60)
        return

    def gameplay(self):
        return

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
                    self.current_tet.rotate()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pass
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pass

    def gravity(self):
        return


class XHitbox(pygame.sprite.Sprite):
    """ Used for X-Axis collision detection. """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 20))
        self.rect = self.image.get_rect()
        self.image.fill((152, 251, 152))
        self.draw_hitbox = False

        print("Hitbox created.")

    def toggle_draw(self):
        """ When called will toggle the self.draw_hitbox bool. """
        if self.draw_hitbox:
            self.draw_hitbox = False
        else:
            self.draw_hitbox = True

    def draw(self, surface, xy):
        """ Draws the Hitbox onto the given surface.
            --- Used only for testing. """
        if self.draw_hitbox:
            surface.blit(self.image, (xy[0], xy[1]))
        else:
            return

    def get_hitbox_rect(self) -> object:
        return self.rect

    def get_x(self) -> int:
        """ Returns the X co-ordinate of the Hitbox. """
        return self.rect.x

    def get_y(self) -> int:
        """ Returns the Y co-ordinate of the Hitbox. """
        return self.rect.y

    def set_x(self, x):
        """ Sets the X co-ordinate of the Hitbox. """
        self.rect.x = x

    def set_y(self, y):
        """ Sets the Y co-ordinate of the Hitbox. """
        self.rect.y = y


class YHitbox(XHitbox):
    """ Used for Y-Axis collision detection. """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 60))
        self.image.fill((43, 169, 255))


class Block(pygame.sprite.Sprite):

    def __init__(self, colour, identification, block_size):
        pygame.sprite.Sprite.__init__(self)
        # self.ID used to identify blocks when they're being drawn.
        self.ID = identification

        self.block_size = block_size

        # Block is (39, 39) so that there is a 2px gap between each block.
        self.image = pygame.Surface((39, 39))
        # self.center is filled with a different colour to self image to create a border.
        self.center = pygame.Surface((35, 35))
        self.rect = self.image.get_rect()
        # Unpacking the colour tuple and filling the two surfaces.
        self.dark, self.light = colour
        self.image.fill(self.dark)
        self.center.fill(self.light)

        # Create the hitboxes.
        # -- Adjusted X and Y for their initialisation, so they're in the correct position.
        self.x_hitbox = XHitbox()
        self.y_hitbox = YHitbox()

        print("Block created.")

    def draw(self, surface, x_and_y=None):
        """ Draws the block on the given surface and at the given co-ordinates.
            --- If the x_and_y argument is None, the block is no longer part of a Tetromino,
                and should be drawn at the co-ordinates it currently occupies.
            --- Here we also call the draw() method on the two Hitboxes. """

        if x_and_y is None:
            # Drawing the center surface onto the image surface to create the border.
            self.image.blit(self.center, (2, 2))
            # Now draw the whole image to the given surface.
            surface.blit(self.image, self.rect)
        else:
            self.set_x(x_and_y[0], True)
            self.set_y(x_and_y[1], True)
            self.image.blit(self.center, (2, 2))
            surface.blit(self.image, self.rect)

        # Draw the hitboxes
        self.x_hitbox.draw(surface, [self.get_x(True)-10, self.get_y(True)+10])
        self.y_hitbox.draw(surface, [self.get_x(True)+10, self.get_y(True)-10])

    def x_collision_detection(self, group) -> bool:
        """ Iterates through a group of blocks, and returns true if the block has collided with any
            other other block on the X axis. """
        for block in group:
            if self.x_hitbox.rect.colliderect(block.x_hitbox.get_hitbox_rect()):
                return True

    def y_collision_detection(self, group) -> bool:
        """ Iterates through a group of blocks, and returns true if the block has collided with any
            other other block on the Y axis. """
        for block in group:
            if self.y_hitbox.rect.colliderect(block.y_hitbox.get_hitbox_rect()):
                return True

    def move_down(self):
        return

    def get_x(self, return_raw_data=False) -> int:
        """ Returns the X co-ordinate of the Block. """
        if return_raw_data:
            return self.rect.x
        else:
            return self.rect.x // self.block_size

    def get_y(self, return_raw_data=False) -> int:
        """ Returns the Y co-ordinate of the Block. """
        if return_raw_data:
            return self.rect.y
        else:
            return self.rect.y // self.block_size

    def set_x(self, x, parse_raw_data=False):
        """ Sets the X co-ordinate of the Block. """
        if parse_raw_data:
            self.rect.x = x
        else:
            self.rect.x = x * self.block_size

    def set_y(self, y, parse_raw_data=False):
        """ Sets the Y co-ordinate of the Block. """
        if parse_raw_data:
            self.rect.y = y
        else:
            self.rect.y = y * self.block_size

    def get_block_id(self) -> int:
        """ Returns the Block ID. """
        return self.ID


class Tetromino(pygame.sprite.Sprite):

    def __init__(self, block_size, colours):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = block_size

        # Surface is (160, 160) because the shape templates are that big.
        self.image = pygame.Surface((160, 160))
        self.rect = self.image.get_rect()

        # Pick a random colour for the Tetromino
        self.colour = colours.get(random.choice(list(colours.keys())))

        # Integer to hold current rotation of Tetromino.
        self.current_rotation = 0

        # Group to hold the blocks with make up the Tetromino
        self.blocks = pygame.sprite.Group()

        # Randomly assign the shape of the Tetromino.
        self.shape = random.choice(["L", "J", "I", "T", "S", "Z", "O"])
        print(self.shape)

        # Dictionary containing Tetromino shapes, and their rotations.
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
                                        "-B---",
                                        "-BBB-",
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

        # Create the blocks
        self.create_blocks()

        print("Tet created.")

    def create_blocks(self):
        """ Creates a block and give it an ID. """
        for i in range(4):
            new_block = Block(self.colour, i, self.block_size)
            self.blocks.add(new_block)

    def x_collision_detection(self, static_tetrominoes) -> bool:
        for block in self.blocks:
            if block.x_collision_detection(static_tetrominoes):
                return True

    def y_collision_detection(self, static_tetrominoes) -> bool:
        for block in self.blocks:
            if block.y_collision_detection(static_tetrominoes):
                return True

    def rotate(self):
        """ Increases and resets the current_rotation integer accordingly. """
        if self.current_rotation == len(self.shape_dictionary.get(self.shape)) - 1:
            self.current_rotation = 0
        else:
            self.current_rotation += 1

    def move_left(self):
        """ Moves the Tetromino to the left on the grid. """
        self.rect.x -= 1 * self.block_size

    def move_right(self):
        """ Moves the Tetromino to the right on the grid. """
        self.rect.x += 1 * self.block_size

    def move_down(self, movement_amount):
        """ Moves the Tetromino down the grid. """
        # todo - try using the argument to speed up the descent
        self.rect.y += movement_amount * self.block_size

    def draw(self, surface):
        """ Calculates the where to draw each block, and then calls the blocks own draw() method. """

        # i will be iterated, and will draw the correct block according to each block's ID.
        i = 0
        x, y = self.get_x(True), self.get_y(True)

        for string in self.shape_dictionary.get(self.shape)[self.current_rotation]:
            for char in string:
                if char == '-':
                    x += self.block_size
                elif char == 'B':
                    for block in self.blocks.sprites():
                        if i == block.get_block_id():
                            block.draw(surface, [x, y])
                            x += self.block_size
                    i += 1
            x = self.get_x(True)
            y += self.block_size

    def get_x(self, return_raw_data=False) -> int:
        """ Returns the X co-ordinate of the Tetromino. """
        if return_raw_data:
            return self.rect.x
        else:
            return self.rect.x // self.block_size

    def get_y(self, return_raw_data=False) -> int:
        """ Returns the Y co-ordinate of the Tetromino. """
        if return_raw_data:
            return self.rect.y
        else:
            return self.rect.y // self.block_size

    def set_x(self, x, parse_raw_data=False):
        """ Sets the X co-ordinate of the Tetromino. """
        if parse_raw_data:
            self.rect.x = x
        else:
            self.rect.x = x * self.block_size

    def set_y(self, y, parse_raw_data=False):
        """ Sets the Y co-ordinate of the Tetromino. """
        if parse_raw_data:
            self.rect.y = y
        else:
            self.rect.y = y * self.block_size


if __name__ == "__main__":
    play_tetris = SetupGame()

    while True:
        play_tetris.loop()
