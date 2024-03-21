from sim.character import Character
from sim.env import Environment


class Dot:
    def __init__(self, owner: Character, env: Environment):
        self.owner = owner
        self.env = env

        self.coefficient = 0
        self.time_between_ticks = 0
        self.starting_ticks = 0
        self.ticks_left = 0
        self.base_tick_dmg = 0
        self.dmg_multiplier = 1
        self.name = ""

    def _get_effective_tick_dmg(self):
        return self.base_tick_dmg + self.owner.sp * self.coefficient

    # This method is overridden in the child class
    def _do_dmg(self):
        pass

    def refresh(self):
        self.ticks_left = self.starting_ticks

    def is_active(self):
        return self.ticks_left > 0

    def run(self):
        while self.ticks_left > 0:
            yield self.env.timeout(self.time_between_ticks)
            self.ticks_left -= 1
            self._do_dmg()
