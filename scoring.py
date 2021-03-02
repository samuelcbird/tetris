from tet_two import DisplayText


class Scoring:

    def __init__(self, surface):
        self.surface = surface
        self.score = 0
        self.score_text = DisplayText((8, 1))
        self.level = 1
        self.level_text = DisplayText((1, 1))

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
            self.score += self.scores.get(str(self.level))[lines_cleared-1]

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
