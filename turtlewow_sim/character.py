import random
from dataclasses import fields, dataclass
from typing import Optional

from turtlewow_sim.env import Environment
from turtlewow_sim.mage_options import MageOptions, MageTalents


@dataclass(kw_only=True)
class CooldownUsages:
    combustion: Optional[float] = None
    arcane_power: Optional[float] = None
    power_infusion: Optional[float] = None
    presence_of_mind: Optional[float] = None
    toep: Optional[float] = None
    mqg: Optional[float] = None
    berserking30: Optional[float] = None
    berserking20: Optional[float] = None
    berserking10: Optional[float] = None


class Character:
    def __init__(self,
                 tal: MageTalents,
                 env: Optional[Environment] = None,
                 name: str = '',
                 sp: int = 0,
                 crit: float = 0,
                 hit: float = 0,
                 haste: float = 0,
                 lag: float = 0.1,  # default lag between spells that seems to occur on turtle
                 opts: MageOptions = MageOptions(),
                 ):

        self.env = env
        self.name = name
        self.sp = sp
        self.crit = crit
        self.hit = hit
        self.haste = haste
        self.lag = lag

        self.opts = opts
        self.tal = tal

        # avoid circular import
        from turtlewow_sim.cooldowns import Cooldowns
        self.cds = Cooldowns(self)

        self._dmg_modifier = 1
        self._trinket_haste = 0
        self._sp_bonus = 0
        self._t2proc = -1

        self.num_casts = {}

        if self.env:
            self.env.add_character(self)

    def reset(self):
        # avoid circular import
        from turtlewow_sim.cooldowns import Cooldowns
        self.cds = Cooldowns(self)

        self._dmg_modifier = 1
        self._trinket_haste = 0
        self._sp_bonus = 0
        self._t2proc = -1

        self.num_casts = {}

    def _set_rotation(self, name, *args, **kwargs):
        def callback(mage):
            rotation = getattr(mage, '_' + name)
            return rotation(*args, **kwargs)

        self.rotation = callback

    def _random_delay(self, secs=2):
        if secs:
            delay = round(random.random() * secs, 2)
            yield self.env.timeout(delay)

    def _use_cds(self, cooldown_usages: CooldownUsages = CooldownUsages()):
        for field in fields(cooldown_usages):
            use_time = getattr(cooldown_usages, field.name)
            cooldown_obj = getattr(self.cds, field.name)
            if use_time and cooldown_obj.usable and self.env.now >= use_time:
                cooldown_obj.activate()

    def print(self, msg):
        if self.env.print:
            self.env.p(f"{self.env.time()} - ({self.name}) {msg}")

    def add_trinket_haste(self, haste):
        self._trinket_haste += haste

    def remove_trinket_haste(self, haste):
        self._trinket_haste -= haste

    def add_sp_bonus(self, sp):
        self._sp_bonus += sp

    def remove_sp_bonus(self, sp):
        self._sp_bonus -= sp

    def add_dmg_modifier(self, mod):
        self._dmg_modifier += mod

    def remove_dmg_modifier(self, mod):
        self._dmg_modifier -= mod
