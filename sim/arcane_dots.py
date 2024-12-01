from sim.dot import Dot
from sim.mage import Spell as MageSpell
from sim.spell_school import DamageType
from sim.warlock import Spell as LockSpell


class MoonfireDot(Dot):
    def __init__(self, owner, env):
        super().__init__(owner, env, DamageType.ARCANE)

        self.coefficient = .1302
        self.time_between_ticks = 3
        self.ticks_left = 6
        self.starting_ticks = 6
        self.base_tick_dmg = 96
        self.name = MageSpell.MOONFIRE.value
