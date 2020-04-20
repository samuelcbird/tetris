import pygame
import random


class SetupGame:
    """ This class will setup and handle the running of the game. """

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        # The timer is used to regulate the speed of gameplay.
        # self.gameplay_speed can be diminished to increase the speed of gameplay.
        self.timer = pygame.time.get_ticks()

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
        self.main_window_size = (18*self.block_size, 22*self.block_size)
        self.main_window = pygame.display.set_mode(self.main_window_size)
        self.main_window.fill(self.bg_colours.get("light_grey"))

        # Creating surfaces for gameplay and the display window for the next Tetromino.
        self.game_area = pygame.Surface((10*self.block_size, 18*self.block_size))
        self.game_area.fill(self.bg_colours.get("off_white"))
        self.next_tet_window = pygame.Surface((5*self.block_size, 5*self.block_size))
        self.next_tet_window.fill(self.bg_colours.get("off_white"))

        # Set up scoring for game
        self.score = Scoring(self.main_window, self.block_size, self.bg_colours)

        # Set speed by level of game
        self.difficulty = [500, 450, 400, 350, 300, 250, 200, 150, 50]
        self.gameplay_speed = self.difficulty[(self.score.get_level())]
        # For when the down arrow is pressed
        self.increase_speed = False
        self.game_over = False
        self.game_over_text = None

        # Attributes to hold the appropriate Tetromino
        self.current_tet = None
        self.next_tet = None
        # A group to hold all the blocks once they become static
        # -- After the Tetromino is stationary the Blocks will be removed and the Tetromino will be discarded.
        self.static_blocks = pygame.sprite.Group()
        # A group to hold any sprite that has been discarded (blocks, tetrominoes, hitboxes).
        # -- Anything in this group will be deleted during each iteration of the loop.
        self.discarded_sprites = pygame.sprite.Group()

        self.create_tets()

    def loop(self):
        self.event_handling()
        pygame.display.update()

        self.gameplay_speed = self.difficulty[(self.score.get_level())]

        # Draw the game area and fill with background colour.
        self.main_window.fill(self.bg_colours.get('light_grey'))
        self.main_window.blit(self.game_area, (1*self.block_size, 2*self.block_size))
        self.main_window.blit(self.next_tet_window, (12*self.block_size, 2*self.block_size))
        self.game_area.fill(self.bg_colours.get('off_white'))
        self.next_tet_window.fill(self.bg_colours.get('off_white'))

        if self.current_tet.y_collision(self.static_blocks.sprites()):
            self.stop_current_tet()
        self.current_tet.draw(self.game_area)
        self.next_tet.draw(self.next_tet_window)
        for block in self.static_blocks.sprites():
            block.draw(self.game_area)
        self.score.draw()

        self.gravity()

        self.check_line_completion()

        if self.check_for_game_over():
            if self.game_over_text is None:
                self.game_over_text = GameOver(self.game_area, self.block_size, self.bg_colours)
            # todo - not working
            self.game_over_text.draw()

        self.discarded_sprites.empty()
        # Framerate
        self.clock.tick(60)
        return

    def create_tets(self):
        if self.next_tet is None:
            self.next_tet = Tetromino(self.block_size, self.colours)
        if self.current_tet is None:
            self.current_tet = self.next_tet
            self.current_tet.set_starting_coordinates()
            self.next_tet = Tetromino(self.block_size, self.colours)

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
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.increase_speed:
                        pass
                    else:
                        self.toggle_gravity_speed()
                if event.key == pygame.K_SPACE:
                    self.current_tet.rotate()
                elif event.key == pygame.K_o:
                    pass
                elif event.key == pygame.K_p:
                    self.score.increase_level()
                elif event.key == pygame.K_LEFTBRACKET:
                    YHitbox.toggle_draw()
                elif event.key == pygame.K_RIGHTBRACKET:
                    XHitbox.toggle_draw()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not self.current_tet.x_collision('left', self.static_blocks):
                        if self.current_tet.confined('left'):
                            self.current_tet.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not self.current_tet.x_collision('right', self.static_blocks):
                        if self.current_tet.confined('right'):
                            self.current_tet.move_right()

    def gravity(self):
        if self.game_over_text is None:
            if self.timer < (pygame.time.get_ticks() - self.gameplay_speed):
                if self.current_tet.confined("down"):
                    self.current_tet.move_down()
                else:
                    self.stop_current_tet()
                self.timer = pygame.time.get_ticks()

    def toggle_gravity_speed(self):

        # todo - now not working

        if self.increase_speed:
            self.gameplay_speed += 500
            self.increase_speed = False
        else:
            self.gameplay_speed -= 500
            self.increase_speed = True

    def check_line_completion(self):
        """ Checks for line completion. """
        array_of_blocks_in_line = []
        lines_to_clear = 0
        for i in range(18):
            for block in self.static_blocks.sprites():
                if block.get_y() == i:
                    array_of_blocks_in_line.append(block)
                if len(array_of_blocks_in_line) >= 10:
                    lines_to_clear += 1
                    self.remove_blocks(array_of_blocks_in_line)
                    array_of_blocks_in_line.clear()
                    self.move_blocks_down(i)
                    self.score.increase_score(lines_to_clear)
            array_of_blocks_in_line.clear()

    def remove_blocks(self, array_of_blocks):
        """ Removes blocks in the given array from the game. """
        for bloc in array_of_blocks:
            self.discarded_sprites.add(bloc)
            self.static_blocks.remove(bloc)

    def move_blocks_down(self, above_this_line):
        for block in self.static_blocks.sprites():
            y = block.get_y()
            if y <= above_this_line:
                block.move_down()

    def check_for_game_over(self):
        """ Checks if any static block has reached the top of the game area. """
        for block in self.static_blocks.sprites():
            if block.get_y() <= 1:
                self.game_over = True
        return self.game_over

    def stop_current_tet(self):
        """ Shrinks the hitbox, stops the tet, removes the blocks and adds to static_blocks, and discards the tet.
            Set's current_tet to None so when create_tets() is called the game will progress.
            Toggles the fast gravity it the down arrow has been used. """
        self.current_tet.shrink_y_hitbox()
        self.current_tet.add_blocks_to_group(self.static_blocks)
        self.discarded_sprites.add(self.current_tet)
        self.current_tet = None

        self.toggle_gravity_speed()
        self.create_tets()


class DisplayText:

    def __init__(self, block_size, colours, xy):
        self.colours = colours
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font, 20)

        self.text = self.display('')
        self.rect = self.text.get_rect()
        x, y = xy
        self.rect.x = x * block_size
        self.rect.y = y * block_size

    def display(self, text):
        return self.font.render(text, True, self.colours.get('dark_grey'))

    def draw(self, surface, text_obj):
        self.text = text_obj
        surface.blit(self.text, self.rect)


class Scoring:

    def __init__(self, surface, block_size, colours):
        self.surface = surface
        self.score = 0
        self.score_text = DisplayText(block_size, colours, (8, 1))
        self.level = 1
        self.level_text = DisplayText(block_size, colours, (1, 1))

        self.lines_cleared_iterator = 0

        self.scores = {'1': [40, 100, 300, 1200],
                       '2': [80, 200, 600, 2400],
                       '9': [400, 1000, 3000, 3600]}

    def increase_score(self, lines_cleared):
        """ Increases score depending on level and lines cleared. """

        # Increases level after 10 lines have been cleared.
        self.lines_cleared_iterator += lines_cleared
        if self.lines_cleared_iterator >= 10:
            self.increase_level()
            self.lines_cleared_iterator = 0

        # Code a little arbitrary, needs closer inspection
        if self.level == 1 or self.level == 2:
            if lines_cleared >= len(self.scores.get('1'))+1:
                self.score += self.scores.get(str(self.get_level))[3]
            else:
                self.score += self.scores.get(str(self.level))[lines_cleared-1]
        elif 2 < self.level < 10:
            self.score += self.scores.get(str(self.level))[lines_cleared+1]

    def increase_level(self):
        """ Increases level by 1. """
        self.level += 1

    def draw(self):
        score_obj = self.score_text.display(str(self.score))
        level_obj = self.level_text.display(str(self.level))

        self.score_text.draw(self.surface, score_obj)
        self.level_text.draw(self.surface, level_obj)

    def get_level(self) -> int:
        return self.level


class GameOver:

    def __init__(self, surface, block_size, colours):
        self.block_size = block_size
        self.colours = colours
        self.surface = surface

        self.text = DisplayText(self.block_size, self.colours, (10, 9))

    def draw(self):
        text_obj = self.text.display("GAME OVER")


class YHitbox(pygame.sprite.Sprite):
    """ Used for Y-Axis collision detection. """

    draw_hitbox = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 54))
        self.rect = self.image.get_rect()
        self.image.fill((152, 251, 152))
        # self.draw_hitbox = False

    @classmethod
    def toggle_draw(cls):
        """ When called will toggle the self.draw_hitbox bool. """
        if cls.draw_hitbox:
            cls.draw_hitbox = False
        else:
            cls.draw_hitbox = True

    def draw(self, surface, xy):
        """ Draws the Hitbox onto the given surface.
            --- Sets the correct position.
            --- Draw used only for testing. """
        self.set_x(xy[0])
        self.set_y(xy[1])
        if self.draw_hitbox:
            surface.blit(self.image, self.rect)
        else:
            return

    def shrink_size(self):
        """ Reduces the size of the hitbox so that the underneath of a block won't stop the moving Tet. """
        x, y = self.rect.x, self.rect.y
        self.image = pygame.Surface((20, 27))
        self.rect = self.image.get_rect()
        self.set_x(x)
        self.set_y(y)
        self.image.fill((152, 251, 152))

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


class XHitbox(YHitbox):
    """ Used for X-Axis collision detection. """

    draw_hitbox = False

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
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
        self.y_hitbox = YHitbox()
        self.left_x_hitbox = XHitbox()
        self.right_x_hitbox = XHitbox()

    def draw(self, surface, x_and_y=None):
        """ Draws the block on the given surface and at the given co-ordinates.
            --- If the x_and_y argument is None, the block is no longer part of a Tetromino,
                and should be drawn at the co-ordinates it currently occupies.
            --- Here we also call the draw() method on the two Hitboxes. """

        if x_and_y is None:
            # Drawing the center surface onto the image surface to create the border.
            self.image.blit(self.center, (2, 2))
            # Now draw the whole image to the given surface.
            x, y = self.get_x(True), self.get_y(True)
            surface.blit(self.image, [x, y])
        else:
            self.set_x(x_and_y[0], True)
            self.set_y(x_and_y[1], True)
            self.image.blit(self.center, (2, 2))
            surface.blit(self.image, self.rect)

        # Draw the hitboxes
        self.y_hitbox.draw(surface, [self.get_x(True)+10, self.get_y(True)-7])
        self.left_x_hitbox.draw(surface, [self.get_x(True) - 7, self.get_y(True) + 10])
        self.right_x_hitbox.draw(surface, [self.get_x(True) + 28, self.get_y(True) + 10])

    def y_collision_detection(self, group) -> bool:
        """ Iterates through a group of blocks, and returns true if the block has collided with any
            other other block on the Y axis. """
        for block in group:
            if self.y_hitbox.rect.colliderect(block.y_hitbox.get_hitbox_rect()):
                return True

    def x_collision_detection(self, direction, group) -> bool:
        """ Iterates through a group of blocks, and returns true if the block has collided with any
            other other block on the Y axis. """
        if direction == "left":
            for block in group:
                if self.left_x_hitbox.rect.colliderect(block.right_x_hitbox.get_hitbox_rect()):
                    return True
        elif direction == "right":
            for block in group:
                if self.right_x_hitbox.rect.colliderect(block.left_x_hitbox.get_hitbox_rect()):
                    return True

    def move_down(self):
        self.rect.y += self.block_size

    def shrink_hitbox(self):
        """ Calls the Y hitbox's shrink_size() method. """
        self.y_hitbox.shrink_size()

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
        self.set_x(0)
        self.set_y(0)

        # Pick a random colour for the Tetromino
        self.colour = colours.get(random.choice(list(colours.keys())))

        # Integer to hold current rotation of Tetromino.
        self.current_rotation = 0

        # Group to hold the blocks with make up the Tetromino
        self.blocks = pygame.sprite.Group()

        # Randomly assign the shape of the Tetromino.
        self.shape = random.choice(["L", "J", "I", "T", "S", "Z", "O"])

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

    def create_blocks(self):
        """ Creates a block and give it an ID. """
        for i in range(4):
            new_block = Block(self.colour, i, self.block_size)
            self.blocks.add(new_block)

    def set_starting_coordinates(self):
        """ Randomly chooses the X coordinate and sets the Tetrominoes coordinates. """
        done = False
        while not done:
            self.set_x(random.choice(range(-1, 9)))
            for block in self.blocks.sprites():
                if block.get_x() >= 9:
                    continue
                else:
                    done = True
        self.set_y(-3)

    def y_collision(self, static_tetrominoes) -> bool:

        for block in self.blocks.sprites():
            if block.y_collision_detection(static_tetrominoes):
                return True

    def x_collision(self, direction, static_tetrominoes) -> bool:
        for block in self.blocks.sprites():
            if block.x_collision_detection(direction, static_tetrominoes):
                return True

    def shrink_y_hitbox(self):
        """ Calls the shrink method of the Y hitbox for each block. """
        for block in self.blocks.sprites():
            block.shrink_hitbox()

    def add_blocks_to_group(self, group):
        for block in self.blocks.sprites():
            group.add(block)

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

    def move_down(self):
        """ Moves the Tetromino down the grid. """
        self.rect.y += self.block_size

    def confined(self, direction) -> bool:
        """ Returns true unless a block is heading outside of the game area. """
        for block in self.blocks.sprites():
            x, y = block.get_x(), block.get_y()
            if direction == "down" and y >= 17:
                return False
            elif direction == "left" and x <= 0:
                return False
            elif direction == "right" and x >= 9:
                return False
        return True

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
