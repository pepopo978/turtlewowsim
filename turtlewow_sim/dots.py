from turtlewow_sim.character import Character
from turtlewow_sim.env import Environment


class FireDot:
    def __init__(self, owner: Character, env: Environment):
        self.owner = owner
        self.env = env

        self.time_between_ticks = 0
        self.starting_ticks = 0
        self.ticks_left = 0
        self.base_tick_dmg = 0
        self.name = ""

    def refresh(self):
        self.ticks_left = self.starting_ticks

    def active(self):
        return self.ticks_left > 0

    def _do_dmg(self):
        tick_dmg = self.base_tick_dmg

        if self.env.debuffs.coe:
            tick_dmg *= 1.1

        if self.env.debuffs.nightfall:
            tick_dmg *= 1.15

        if self.owner.cds.power_infusion.is_active():
            tick_dmg *= 1.2

        tick_dmg *= 1 + self.env.debuffs.scorch_stacks * 0.03
        tick_dmg = int(tick_dmg)
        if self.env.print_dots:
            self.env.p(
                f"{self.env.time()} - ({self.owner.name}) {self.name} dot tick {tick_dmg} ticks remaining {self.ticks_left}")
        self.env.total_dot_dmg += tick_dmg
        self.env.meter.register(self.owner.name, tick_dmg)

    def run(self):
        while self.ticks_left > 0:
            yield self.env.timeout(self.time_between_ticks)
            self.ticks_left -= 1
            self._do_dmg()


class FireballDot(FireDot):
    def __init__(self, owner, env, has_firepower=True):
        super().__init__(owner, env)

        self.time_between_ticks = 2
        self.ticks_left = 4
        self.starting_ticks = 4
        self.firepower_multiplier = 1.1 if has_firepower else 1
        self.base_tick_dmg = 19 * self.firepower_multiplier
        self.name = "Fireball"


class PyroblastDot(FireDot):
    def __init__(self, owner, env, has_firepower=True):
        super().__init__(owner, env)

        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.firepower_multiplier = 1.1 if has_firepower else 1
        self.base_tick_dmg = (67 + self.owner.sp * 0.15) * self.firepower_multiplier
        self.name = "Pyroblast"
