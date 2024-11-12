import random


class ItemProc:
    PERCENT_CHANCE = 0
    COOLDOWN = 0
    PRINT_PROC = False

    def __init__(self, character, callback):
        self.character = character
        self.callback = callback
        self.last_proc_time = 0

    @property
    def name(self):
        return type(self).__name__

    def _roll_proc(self):
        return random.randint(1, 100) <= self.PERCENT_CHANCE

    def check_for_proc(self, current_time):
        if self.COOLDOWN and self.last_proc_time + self.COOLDOWN > current_time:
            return

        if self._roll_proc():
            self.last_proc_time = current_time
            if self.PRINT_PROC:
                self.character.print(f"{self.name} triggered")
            self.callback()


class BladeOfEternalDarkness(ItemProc):
    PERCENT_CHANCE = 10


class OrnateBloodstoneDagger(ItemProc):
    PERCENT_CHANCE = 20


class WrathOfCenarius(ItemProc):
    PERCENT_CHANCE = 5


class EndlessGulch(ItemProc):
    PERCENT_CHANCE = 20
