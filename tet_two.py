import pygame
import random
import constants
import scoring
from typing import Union, Any, List, Set, Dict, Tuple, Optional


class SetupGame:
    """ This class will setup and handle the running of the game. """

    def __init__(self):
        pygame.init()

        self.clock: pygame.time.Clock = pygame.time.Clock()
        # The timer is used to regulate the speed of gameplay.
        # self.gameplay_speed can be diminished to increase the speed of gameplay.
        self.timer: int = pygame.time.get_ticks()

        # Defining size of application window; includes peripherals eg, score and upcoming Tetromino
        self.main_window_size: Tuple = (18*constants.BLOCK_SIZE, 22*constants.BLOCK_SIZE)
        self.main_window: pygame.Surface = pygame.display.set_mode(self.main_window_size)
        self.main_window.fill(constants.BG_COLOURS.get("light_grey"))
        pygame.display.set_caption("Tetris")

        # Creating surfaces for gameplay and the display window for the next Tetromino.
        self.game_area: pygame.Surface = pygame.Surface((10*constants.BLOCK_SIZE, 18*constants.BLOCK_SIZE))
        self.game_area.fill(constants.BG_COLOURS.get("off_white"))
        self.next_tetromino_window: pygame.Surface = pygame.Surface((5*constants.BLOCK_SIZE, 5*constants.BLOCK_SIZE))
        self.next_tetromino_window.fill(constants.BG_COLOURS.get("off_white"))

        # Set up scoring for game
        self.score: scoring.Scoring = scoring.Scoring(self.main_window)

        # Set speed by level of game
        self.difficulty: List[int] = [500, 450, 400, 350, 300, 250, 200, 150, 50]
        self.gameplay_speed: int = self.difficulty[(self.score.get_level())]
        # For when the down arrow is pressed
        self.increase_speed: bool = False
        self.game_over: bool = False
        self.game_over_text: Optional[str] = None

        # Attributes to hold the appropriate Tetromino
        self.current_tetromino: Optional[Tetromino] = None
        self.next_tetromino: Optional[Tetromino] = None
        # A group to hold all the blocks once they become static
        # -- After the Tetromino is stationary the Blocks will be removed and the Tetromino will be discarded.
        self.static_blocks: pygame.sprite.Group = pygame.sprite.Group()
        # A group to hold any sprite that has been discarded (blocks, tetrominoes, hitboxes).
        # -- Anything in this group will be deleted during each iteration of the loop.
        self.discarded_sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.create_tets()

    def loop(self) -> None:
        self.event_handling()
        pygame.display.update()

        self.gameplay_speed = self.difficulty[(self.score.get_level())]

        # Draw the game area and fill with background colour.
        self.main_window.fill(constants.BG_COLOURS.get('light_grey'))
        self.main_window.blit(self.game_area, (1*constants.BLOCK_SIZE, 2*constants.BLOCK_SIZE))
        self.main_window.blit(self.next_tetromino_window, (12 * constants.BLOCK_SIZE, 2 * constants.BLOCK_SIZE))
        self.game_area.fill(constants.BG_COLOURS.get('off_white'))
        self.next_tetromino_window.fill(constants.BG_COLOURS.get('off_white'))

        if self.current_tetromino.y_collision(self.static_blocks.sprites()):
            self.stop_current_tet()
        self.current_tetromino.draw(self.game_area)
        self.next_tetromino.draw(self.next_tetromino_window)
        for block in self.static_blocks.sprites():
            block.draw(self.game_area)
        self.score.draw()

        self.gravity()

        self.check_line_completion()

        if self.check_for_game_over():
            if self.game_over_text is None:
                self.game_over_text = GameOver(self.game_area)
            # todo - not working
            self.game_over_text.draw()

        self.discarded_sprites.empty()
        # Framerate
        self.clock.tick(60)
        return

    def create_tets(self):
        if self.next_tetromino is None:
            self.next_tetromino = Tetromino()
        if self.current_tetromino is None:
            self.current_tetromino = self.next_tetromino
            self.current_tetromino.set_starting_coordinates()
            self.next_tetromino = Tetromino()

    def event_handling(self):
        """ This handles all keyboard and mouse events from user """

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.increase_speed:
                        pass
                    else:
                        self.toggle_gravity_speed()
                if event.key == pygame.K_SPACE:
                    self.current_tetromino.rotate()
                elif event.key == pygame.K_o:
                    pass
                elif event.key == pygame.K_p:
                    self.score.increase_level()
                elif event.key == pygame.K_LEFTBRACKET:
                    # Used for debugging
                    # YHitbox.toggle_draw()
                    pass
                elif event.key == pygame.K_RIGHTBRACKET:
                    # Used for debugging
                    # XHitbox.toggle_draw()
                    pass
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not self.current_tetromino.x_collision('left', self.static_blocks):
                        if self.current_tetromino.confined('left'):
                            self.current_tetromino.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not self.current_tetromino.x_collision('right', self.static_blocks):
                        if self.current_tetromino.confined('right'):
                            self.current_tetromino.move_right()

    def gravity(self):
        if self.game_over_text is None:
            if self.timer < (pygame.time.get_ticks() - self.gameplay_speed):
                if self.current_tetromino.confined("down"):
                    self.current_tetromino.move_down()
                else:
                    self.stop_current_tet()
                self.timer = pygame.time.get_ticks()

    def toggle_gravity_speed(self):

        if self.increase_speed:
            self.difficulty[(self.score.get_level())] += 500
            self.increase_speed = False
        else:
            self.difficulty[(self.score.get_level())] -= 500
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

    def check_for_game_over(self) -> bool:
        """ Checks if any static block has reached the top of the game area. """
        for block in self.static_blocks.sprites():
            if block.get_y() <= 1:
                self.game_over = True
        return self.game_over

    def stop_current_tet(self):
        """ Shrinks the hitbox, stops the tet, removes the blocks and adds to static_blocks, and discards the tet.
            Set's current_tet to None so when create_tets() is called the game will progress.
            Toggles the fast gravity it the down arrow has been used. """
        self.current_tetromino.shrink_y_hitbox()
        self.current_tetromino.add_blocks_to_group(self.static_blocks)
        self.discarded_sprites.add(self.current_tetromino)
        self.current_tetromino = None

        self.toggle_gravity_speed()
        self.create_tets()


class DisplayText:

    def __init__(self, xy: tuple):
        pygame.font.init()
        default_font: str = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font, 20)

        self.text = self.display('')
        self.rect = self.text.get_rect()
        x, y = xy
        self.rect.x = x * constants.BLOCK_SIZE
        self.rect.y = y * constants.BLOCK_SIZE

    def display(self, text):
        return self.font.render(text, True, constants.BG_COLOURS.get('dark_grey'))

    def draw(self, surface, text_obj):
        self.text = text_obj
        surface.blit(self.text, self.rect)


class GameOver:

    # TODO - this still doesn't work
    def __init__(self, surface):
        self.surface = surface

        self.text = DisplayText((10, 9))

    def draw(self):
        text_obj = self.text.display("GAME OVER")
        self.text.draw(self.surface, text_obj)


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

    def set_x(self, x) -> None:
        """ Sets the X co-ordinate of the Hitbox. """
        self.rect.x = x

    def set_y(self, y) -> None:
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

    def __init__(self, colour, identification):
        pygame.sprite.Sprite.__init__(self)
        # self.ID used to identify blocks when they're being drawn.
        self.ID = identification

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

    def draw(self, surface: pygame.Surface, x_and_y: Optional[list] = None):
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

    def y_collision_detection(self, group: pygame.sprite.Group) -> bool:
        """ Iterates through a group of blocks, and returns true if the block has collided with any
            other other block on the Y axis. """
        for block in group:
            if self.y_hitbox.rect.colliderect(block.y_hitbox.get_hitbox_rect()):
                return True

    def x_collision_detection(self, direction: str, group: pygame.sprite.Group) -> bool:
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

    def move_down(self) -> None:
        self.rect.y += constants.BLOCK_SIZE

    def shrink_hitbox(self) -> None:
        """ Calls the Y hitbox's shrink_size() method. """
        self.y_hitbox.shrink_size()

    def get_x(self, return_raw_data: bool = False) -> int:
        """ Returns the X co-ordinate of the Block. """
        if return_raw_data:
            return self.rect.x
        else:
            return self.rect.x // constants.BLOCK_SIZE

    def get_y(self, return_raw_data: bool = False) -> int:
        """ Returns the Y co-ordinate of the Block. """
        if return_raw_data:
            return self.rect.y
        else:
            return self.rect.y // constants.BLOCK_SIZE

    def set_x(self, x, parse_raw_data: bool = False) -> None:
        """ Sets the X co-ordinate of the Block. """
        if parse_raw_data:
            self.rect.x = x
        else:
            self.rect.x = x * constants.BLOCK_SIZE

    def set_y(self, y, parse_raw_data: bool = False) -> None:
        """ Sets the Y co-ordinate of the Block. """
        if parse_raw_data:
            self.rect.y = y
        else:
            self.rect.y = y * constants.BLOCK_SIZE

    def get_block_id(self) -> int:
        """ Returns the Block ID. """
        return self.ID


class Tetromino(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Surface is (160, 160) because the shape templates are that big.
        self.image = pygame.Surface((160, 160))
        self.rect = self.image.get_rect()
        self.set_x(0)
        self.set_y(0)

        # Pick a random colour for the Tetromino
        self.colour: tuple = constants.COLOURS.get(random.choice(list(constants.COLOURS.keys())))

        # Integer to hold current rotation of Tetromino.
        self.current_rotation: int = 0

        # Group to hold the blocks with make up the Tetromino
        self.blocks: pygame.sprite.Group = pygame.sprite.Group()

        # Randomly assign the shape of the Tetromino.
        self.shape: str = random.choice(list(constants.TETROMINO_SHAPES.keys()))

        # Create the blocks
        self.create_blocks()

    def create_blocks(self) -> None:
        """ Creates a block and give it an ID. """
        for i in range(4):
            new_block = Block(self.colour, i)
            self.blocks.add(new_block)

    def set_starting_coordinates(self) -> None:
        """ Randomly chooses the X coordinate and sets the Tetrominoes coordinates. """
        done: bool = False
        while not done:
            self.set_x(random.choice(range(-1, 9)))
            # todo - something really wrong here...
            if self.is_outside_game_area():
                continue
            else:
                done = True
        self.set_y(-3)

    def y_collision(self, static_tetrominoes: pygame.sprite.Group) -> bool:
        for block in self.blocks.sprites():
            if block.y_collision_detection(static_tetrominoes):
                return True

    def x_collision(self, direction: str, static_tetrominoes: pygame.sprite.Group) -> bool:
        for block in self.blocks.sprites():
            if block.x_collision_detection(direction, static_tetrominoes):
                return True

    def shrink_y_hitbox(self) -> None:
        """ Calls the shrink method of the Y hitbox for each block. """
        for block in self.blocks.sprites():
            block.shrink_hitbox()

    def add_blocks_to_group(self, group: pygame.sprite.Group) -> None:
        for block in self.blocks.sprites():
            group.add(block)

    def rotate(self) -> None:
        """ Increases and resets the current_rotation integer accordingly. """
        if self.current_rotation == len(constants.TETROMINO_SHAPES.get(self.shape)) - 1:
            self.current_rotation = 0
        else:
            self.current_rotation += 1

    def move_left(self) -> None:
        """ Moves the Tetromino to the left on the grid. """
        self.rect.x -= 1 * constants.BLOCK_SIZE

    def move_right(self) -> None:
        """ Moves the Tetromino to the right on the grid. """
        self.rect.x += 1 * constants.BLOCK_SIZE

    def move_down(self) -> None:
        """ Moves the Tetromino down the grid. """
        self.rect.y += constants.BLOCK_SIZE

    def is_outside_game_area(self) -> bool:
        # todo - something really wrong here...
        for block in self.blocks.sprites():
            if block.get_x(True) >= 360:
                return True

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

    def draw(self, surface: pygame.Surface) -> None:
        """ Calculates the where to draw each block, and then calls the blocks own draw() method. """

        # i will be iterated, and will draw the correct block according to each block's ID.
        i = 0
        x, y = self.get_x(True), self.get_y(True)

        for string in constants.TETROMINO_SHAPES.get(self.shape)[self.current_rotation]:
            for char in string:
                if char == '-':
                    x += constants.BLOCK_SIZE
                elif char == 'B':
                    for block in self.blocks.sprites():
                        if i == block.get_block_id():
                            block.draw(surface, [x, y])
                            x += constants.BLOCK_SIZE
                    i += 1
            x = self.get_x(True)
            y += constants.BLOCK_SIZE

    def get_x(self, return_raw_data: bool = False) -> int:
        """ Returns the X co-ordinate of the Tetromino. """
        if return_raw_data:
            return self.rect.x
        else:
            return self.rect.x // constants.BLOCK_SIZE

    def get_y(self, return_raw_data: bool = False) -> int:
        """ Returns the Y co-ordinate of the Tetromino. """
        if return_raw_data:
            return self.rect.y
        else:
            return self.rect.y // constants.BLOCK_SIZE

    def set_x(self, x: int, parse_raw_data: bool = False):
        """ Sets the X co-ordinate of the Tetromino. """
        if parse_raw_data:
            self.rect.x = x
        else:
            self.rect.x = x * constants.BLOCK_SIZE

    def set_y(self, y: int, parse_raw_data: bool = False):
        """ Sets the Y co-ordinate of the Tetromino. """
        if parse_raw_data:
            self.rect.y = y
        else:
            self.rect.y = y * constants.BLOCK_SIZE


if __name__ == "__main__":
    play_tetris = SetupGame()

    while True:
        play_tetris.loop()
