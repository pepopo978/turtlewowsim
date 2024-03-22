from sim.dot import Dot
from sim.mage import Spell as MageSpell
from sim.warlock import Spell as LockSpell


class FireDot(Dot):
    def _do_dmg(self):
        tick_dmg = self._get_effective_tick_dmg()
        tick_dmg *= self.dmg_multiplier

        if self.env.debuffs.has_coe:
            tick_dmg *= 1.1

        if self.env.debuffs.has_nightfall:
            tick_dmg *= 1.15

        tick_dmg *= self.owner.dmg_modifier

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

        self.coefficient = 0
        self.time_between_ticks = 2
        self.ticks_left = 4
        self.starting_ticks = 4
        self.dmg_multiplier = 1.1 if has_firepower else 1
        self.base_tick_dmg = 19
        self.name = MageSpell.FIREBALL.value


class PyroblastDot(FireDot):
    def __init__(self, owner, env, has_firepower=True):
        super().__init__(owner, env)

        self.coefficient = 0.15
        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.dmg_multiplier = 1.1 if has_firepower else 1
        self.base_tick_dmg = 67
        self.name = MageSpell.PYROBLAST.value


class ImmolateDot(FireDot):
    def __init__(self, owner, env, has_emberstorm=True):
        super().__init__(owner, env)

        self.coefficient = 0.15
        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.dmg_multiplier = 1.1 if has_emberstorm else 1
        self.base_tick_dmg = 102
        self.name = LockSpell.IMMOLATE.value
