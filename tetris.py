import pygame
import random


class SetupGame:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.block = 40
        self.main_window_width_height = (20*self.block, 20*self.block)
        self.main_window = pygame.display.set_mode(self.main_window_width_height)
        pygame.display.set_caption("Tetris")

        self.draw_array = []

        # define colours
        self.dark_blue, self.light_blue = (40, 63, 128), (156, 182, 255)
        self.dark_purple, self.light_purple = (77, 48, 128), (202, 171, 255)
        self.dark_pink, self.light_pink = (128, 29, 93), (255, 135, 213)
        self.dark_orange, self.light_orange = (204, 65, 18), (255, 138, 99)
        self.default_grey = (192, 192, 192)
        self.off_white = (240, 240, 240)

        self.main_window.fill(self.default_grey)
        self.game_display = pygame.Surface((10*self.block, 18*self.block))
        self.game_display.fill((240, 240, 240))

    def loop(self):
        pygame.display.update()
        self.main_window.blit(self.game_display, (5*self.block, 1*self.block))

        self.game_display.fill(self.off_white)
        self.clock.tick(60)

    @staticmethod
    def event_handling():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tet.rotate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass


class Block(pygame.sprite.Sprite):

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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = 40
        self.image = pygame.Surface([160, 160])
        self.rect = self.image.get_rect()
        self.colour = random.choice([(new_game.dark_blue, new_game.light_blue),
                                     (new_game.dark_pink, new_game.light_pink),
                                     (new_game.dark_purple, new_game.light_purple),
                                     (new_game.dark_orange, new_game.light_orange)])

        # get random x coordinate
        self.rect.x = random.choice(range(0, 8*self.block_size, self.block_size))
        self.rect.y = 20
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
                                        "--B--",
                                        "--B--",
                                        "-BB--",
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
                                        "-----",
                                        "-BBB-",
                                        "--B--",
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
                                        "--BB-",
                                        "--BB-",
                                        "-----",
                                        "-----"]]
                                 }

    def create_blocks(self):
        for i in range(4):
            new_block = Block(self.colour, i)
            self.blocks.add(new_block)

    def rotate(self):
        if self.current_rotation == len(self.shape_dictionary.get(self.shape)) - 1:
            self.current_rotation = 0
        else:
            self.current_rotation += 1

    def gravity(self):
        self.rect.y += self.block_size

    def draw(self, surface):
        self.gravity()

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

    tet = Tetromino()

    while True:
        new_game.loop()
        new_game.event_handling()

        tet.draw(new_game.game_display)

