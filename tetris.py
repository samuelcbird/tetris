import pygame


class SetupGame:

    def __init__(self):
        pygame.init()

        self.block = 40
        self.main_window_width_height = (20*self.block, 20*self.block)
        self.main_window = pygame.display.set_mode(self.main_window_width_height)
        pygame.display.set_caption("Tetris")

        # define colours
        self.default_grey = (192, 192, 192)

        self.main_window.fill(self.default_grey)
        self.game_display = pygame.Surface((10*self.block, 18*self.block))
        self.game_display.fill((89, 89, 89))

        self.loop_stuff = []

    def add_to_loop(self, item):
        self.loop_stuff.append(item)

    def loop(self):
        pygame.display.update()
        self.main_window.blit(self.game_display, (5*self.block, 1*self.block))

        if len(self.loop_stuff) <= 0:
            return
        else:
            for stuff in self.loop_stuff:
                stuff()

    @staticmethod
    def event_handling():
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


class Block(pygame.sprite.Sprite):

    def __init__(self, colour, identification):
        pygame.sprite.Sprite.__init__(self)
        self.ID = identification
        self.image = pygame.Surface([40, 40])
        self.rect = self.image.get_rect()
        self.image.fill(colour)

    def draw(self, xy, surface):
        self.rect.x, self.rect.y, = xy
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)


class Tetromino(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([160, 160])
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 20
        self.blocks = pygame.sprite.Group()
        self.create_blocks()
        self.shape_dictionary = {"L": [["-----",
                                        "-B---",
                                        "-B---",
                                        "-BB--",
                                        "-----"],
                                       ["-----",
                                        "-----",
                                        "BBB--",
                                        "B----",
                                        "-----"],
                                       ["-----",
                                        "-BB--",
                                        "--B--",
                                        "--B--",
                                        "-----"],
                                       ["-----",
                                        "-----",
                                        "---B-",
                                        "-BBB-",
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
                                        "-----",
                                        "--B--",
                                        "-BBB-",
                                        "-----"],
                                       ["-----",
                                        "--B--",
                                        "--BB-",
                                        "--B--",
                                        "-----"]]
                                 }

    def create_blocks(self):
        for i in range(4):
            new_block = Block((2, 2, 2), i)
            self.blocks.add(new_block)

    def draw(self, surface):
        x, y = self.rect.x, self.rect.y
        block_size = 40
        i = 0
        for string in self.shape_dictionary.get("T")[0]:
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
