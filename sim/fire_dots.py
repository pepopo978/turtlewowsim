from sim.dot import Dot
from sim.mage import Spell as MageSpell
from sim.spell_school import DamageType
from sim.warlock import Spell as LockSpell


class FireballDot(Dot):
    def __init__(self, owner, env):
        super().__init__(owner, env, DamageType.Fire)

        self.coefficient = 0
        self.time_between_ticks = 2
        self.ticks_left = 4
        self.starting_ticks = 4
        self.base_tick_dmg = 19
        self.name = MageSpell.FIREBALL.value


class PyroblastDot(Dot):
    def __init__(self, owner, env):
        super().__init__(owner, env, DamageType.Fire)

        self.coefficient = 0.175
        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.base_tick_dmg = 67
        self.name = MageSpell.PYROBLAST.value


class ImmolateDot(Dot):
    def __init__(self, owner, env):
        super().__init__(owner, env, DamageType.Fire)

        self.coefficient = 0.15
        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.base_tick_dmg = 102
        self.name = LockSpell.IMMOLATE.value
