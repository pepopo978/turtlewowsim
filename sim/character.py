import random
from dataclasses import fields, dataclass
from typing import Optional

from sim.env import Environment
from sim.spell_school import DamageType
from sim.talent_school import TalentSchool


@dataclass(kw_only=True)
class CooldownUsages:
    # Mage
    combustion: Optional[float] = None
    arcane_power: Optional[float] = None
    presence_of_mind: Optional[float] = None

    # Buffs
    power_infusion: Optional[float] = None
    berserking30: Optional[float] = None
    berserking20: Optional[float] = None
    berserking10: Optional[float] = None

    # Trinkets
    toep: Optional[float] = None
    mqg: Optional[float] = None


class Character:
    def __init__(self,
                 env: Optional[Environment],
                 name: str,
                 sp: int,
                 crit: float,
                 hit: float,
                 haste: float,
                 lag: float,
                 ):

        self.env = env
        self.name = name
        self.sp = sp
        self.crit = crit
        self.hit = hit
        self.haste = haste
        self.lag = lag

        # avoid circular import
        from sim.cooldowns import Cooldowns
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
        from sim.cooldowns import Cooldowns
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
            self.print(f"Random initial delay of {delay} seconds")
            yield self.env.timeout(delay)

    def _use_cds(self, cooldown_usages: CooldownUsages = CooldownUsages()):
        for field in fields(cooldown_usages):
            use_time = getattr(cooldown_usages, field.name)
            cooldown_obj = getattr(self.cds, field.name)
            if use_time and cooldown_obj.usable and self.env.now >= use_time:
                cooldown_obj.activate()

    def _roll_hit(self, hit_chance: float):
        return random.randint(1, 100) <= hit_chance

    def _roll_crit(self, crit_chance: float):
        return random.randint(1, 100) <= crit_chance

    def _roll_spell_dmg(self, min_dmg: int, max_dmg: int, spell_coeff: float):
        dmg = random.randint(min_dmg, max_dmg)
        dmg += (self.sp + self._sp_bonus) * spell_coeff
        return dmg

    def _get_crit_multiplier(self, dmg_type: DamageType, talent_school: TalentSchool):
        return 1.5

    def modify_dmg(self, dmg: int, dmg_type: DamageType, is_periodic: bool):
        if self._dmg_modifier != 1:
            dmg *= self._dmg_modifier
        # apply env debuffs
        return self.env.debuffs.modify_dmg(self, dmg, dmg_type, is_periodic)

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

    @property
    def dmg_modifier(self):
        return self._dmg_modifier
        
    @property
    def eff_sp(self):
        return self.sp + self._sp_bonus

    def add_dmg_modifier(self, mod):
        self._dmg_modifier += mod

    def remove_dmg_modifier(self, mod):
        self._dmg_modifier -= mod
