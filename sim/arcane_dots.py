from sim.dot import Dot
from sim.mage import Spell as MageSpell
from sim.spell_school import DamageType


class MoonfireDot(Dot):
    def __init__(self, owner, env, cast_time: float):
        super().__init__(MageSpell.MOONFIRE.value, owner, env, DamageType.ARCANE, cast_time, register_cast=False)

        self.coefficient = .1302
        self.time_between_ticks = 3
        self.ticks_left = 6
        self.starting_ticks = 6
        self.base_tick_dmg = 96
