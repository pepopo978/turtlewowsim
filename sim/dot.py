from sim.character import Character
from sim.env import Environment
from sim.spell_school import DamageType


class Dot:
    def __init__(self, owner: Character, env: Environment, dmg_type: DamageType):
        self.owner = owner
        self.env = env
        self.dmg_type = dmg_type

        self.sp = self.owner.sp # snapshot sp
        self.coefficient = 0
        self.time_between_ticks = 0
        self.starting_ticks = 0
        self.ticks_left = 0
        self.base_tick_dmg = 0
        self.name = ""

    def _get_effective_tick_dmg(self):
        dmg = self.base_tick_dmg + self.sp * self.coefficient
        return self.owner.modify_dmg(dmg, self.dmg_type, is_periodic=True)

    # This method is overridden in the child class
    def _do_dmg(self):
        tick_dmg = self._get_effective_tick_dmg()
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

    def refresh(self):
        self.ticks_left = self.starting_ticks

    def is_active(self):
        return self.ticks_left > 0
