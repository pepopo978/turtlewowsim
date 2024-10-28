import functools
import random
from dataclasses import fields, dataclass

from sim.cooldown_usages import CooldownUsages
from sim.env import Environment
from sim.equipped_items import EquippedItems
from sim.spell_school import DamageType
from sim.talent_school import TalentSchool


class Character:
    def __init__(self,
                 tal: dataclass,
                 name: str,
                 sp: int,
                 crit: float,
                 hit: float,
                 haste: float,
                 lag: float,
                 equipped_items: EquippedItems = None,
                 ):

        self.name = name
        self.sp = sp
        self.crit = crit
        self.hit = hit
        self.haste = haste
        self.lag = lag
        self.env = None

        self.tal = tal

        self._damage_type_haste = {
            DamageType.PHYSICAL: 0,
            DamageType.FIRE: 0,
            DamageType.FROST: 0,
            DamageType.ARCANE: 0,
            DamageType.NATURE: 0,
            DamageType.SHADOW: 0,
            DamageType.HOLY: 0
        }

        # avoid circular import
        from sim.cooldowns import Cooldowns
        self.cds = Cooldowns(self)

        self.equipped_items = equipped_items
        self.item_proc_handler = None

        self._dmg_modifier = 1
        self._trinket_haste = 0
        self._cooldown_haste = 0
        self._sp_bonus = 0

        self.num_casts = {}

    def attach_env(self, env: Environment):
        self.env = env
        if self.equipped_items:
            # avoid circular import
            from sim.item_proc_handler import ItemProcHandler
            self.item_proc_handler = ItemProcHandler(self, self.env, self.equipped_items)

    def reset(self):
        # avoid circular import
        from sim.cooldowns import Cooldowns
        self.cds = Cooldowns(self)

        self._dmg_modifier = 1
        self._trinket_haste = 0
        self._cooldown_haste = 0
        self._sp_bonus = 0

        self.num_casts = {}

    def get_haste_factor_for_damage_type(self, dmg_type: DamageType):
        haste_factor = 1 + self.haste / 100
        trinket_haste_factor = 1 + self._trinket_haste / 100
        cooldown_haste_factor = 1 + self._cooldown_haste / 100
        damage_type_haste_factor = 1 + self._damage_type_haste[dmg_type] / 100

        return haste_factor * trinket_haste_factor * cooldown_haste_factor * damage_type_haste_factor

    def _get_cast_time(self, base_cast_time: float, damage_type: DamageType):
        haste_scaling_factor = self.get_haste_factor_for_damage_type(damage_type)

        return base_cast_time / haste_scaling_factor + self.lag

    def _rotation_callback(self, mage, name, *args, **kwargs):
        rotation = getattr(mage, '_' + name)
        return rotation(*args, **kwargs)

    def _set_rotation(self, name, *args, **kwargs):
        self.rotation = functools.partial(self._rotation_callback, name=name, *args, **kwargs)

    def _random_delay(self, secs=2):
        if secs:
            delay = round(random.random() * secs, 2)
            self.print(f"Random initial delay of {delay} seconds")
            yield self.env.timeout(delay)

    def _use_cds(self, cooldown_usages: CooldownUsages = CooldownUsages()):
        for field in fields(cooldown_usages):
            cooldown_obj = getattr(self.cds, field.name)
            use_times = getattr(cooldown_usages, field.name, None)
            if isinstance(use_times, list):
                for index, use_time in enumerate(use_times):
                    if use_time is not None and cooldown_obj.usable and self.env.now >= use_time:
                        use_times[index] = None
                        cooldown_obj.activate()
            else:
                use_time = use_times
                if use_time is not None and cooldown_obj.usable and self.env.now >= use_time:
                    setattr(cooldown_usages, field.name, None)  # remove use_time so it doesn't get used again
                    cooldown_obj.activate()

    def _roll_hit(self, hit_chance: float):
        return random.randint(1, 100) <= hit_chance

    def _roll_crit(self, crit_chance: float):
        return random.randint(1, 100) <= crit_chance

    def roll_spell_dmg(self, min_dmg: int, max_dmg: int, spell_coeff: float):
        dmg = random.randint(min_dmg, max_dmg)
        dmg += (self.sp + self._sp_bonus) * spell_coeff

        return dmg

    def _check_for_procs(self):
        if self.item_proc_handler:
            self.item_proc_handler.check_for_procs(self.env.now)

    def roll_partial(self, is_dot: bool, is_binary: bool):
        if is_binary:
            return 1

        roll = random.random()
        if is_dot:
            # No partial: 98.53 %
            # 25 % partial: 1.1 %
            # 50 % partial: .366 %
            # 75 % partial: 0 %
            if roll <= .9853:
                return 1
            elif roll <= .9963:
                return .75
            elif roll <= 1:
                return .5
        else:
            # No partial: 82.666 %
            # 25 % partial: 13 %
            # 50 % partial: 4.166 %
            # 75 % partial: 1 %
            if roll <= .82666:
                return 1
            elif roll <= .95666:
                return .75
            elif roll <= .99832:
                return .5
            elif roll <= 1:
                return .25

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

    def add_cooldown_haste(self, haste):
        self._cooldown_haste += haste

    def remove_cooldown_haste(self, haste):
        self._cooldown_haste -= haste

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
