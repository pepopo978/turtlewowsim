import random


class ItemProc:
    PERCENT_CHANCE = 0
    COOLDOWN = 0
    PRINT_PROC = False

    def __init__(self, character, callback):
        self.character = character
        self.callback = callback
        self.last_proc_time = 0

        self.proc_rolls = 0
        self.proc_successes = 0

    @property
    def name(self):
        return type(self).__name__

    def _roll_proc(self, num_mobs=1):
        for _ in range(num_mobs):
            if random.randint(1, 100) <= self.PERCENT_CHANCE:
                return True

        return False

    def check_for_proc(self, current_time, num_mobs):
        if self.COOLDOWN and self.last_proc_time + self.COOLDOWN > current_time:
            return

        self.proc_rolls += num_mobs
        if self._roll_proc(num_mobs):
            self.proc_successes += 1

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
    PERCENT_CHANCE = 12
