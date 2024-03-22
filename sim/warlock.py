import random
from enum import Enum
from functools import partial
from typing import Optional

from sim.character import Character, CooldownUsages
from sim.cooldowns import Cooldown
from sim.env import Environment
from sim.warlock_options import WarlockOptions
from sim.warlock_talents import WarlockTalents


# spell name enum
class Spell(Enum):
    IMMOLATE = "Immolate"
    SEARING_PAIN = "Searing Pain"
    CONFLAGRATE = "Conflagrate"
    CORRUPTION = "Corruption"
    CURSE_OF_AGONY = "Curse of Agony"
    CURSE_OF_SHADOW = "Curse of Shadow"
    SHADOWBOLT = "Shadowbolt"


SPELL_COEFFICIENTS = {
    Spell.IMMOLATE: 0.1865,
    Spell.SHADOWBOLT: 0.8571,
}


class AmplifyCurseCooldown(Cooldown):
    DURATION = 30
    COOLDOWN = 180

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self.cooldown = cooldown

    def use_on_curse(self):
        super().deactivate()


class ConflagrateCooldown(Cooldown):
    DURATION = 30
    COOLDOWN = 180

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self.cooldown = cooldown

    def use_on_curse(self):
        super().deactivate()


class Warlock(Character):
    def __init__(self,
                 tal: WarlockTalents,
                 opts: WarlockOptions = WarlockOptions(),
                 env: Optional[Environment] = None,
                 name: str = '',
                 sp: int = 0,
                 crit: float = 0,
                 hit: float = 0,
                 haste: float = 0,
                 lag: float = 0.1,  # default lag between spells that seems to occur on turtle
                 ):
        super().__init__(env, name, sp, crit, hit, haste, lag)
        self.tal = tal
        self.opts = opts

        # Warlock
        self.nightfall = False

    def _get_cast_time(self, base_cast_time):
        trinket_haste = 1 + self._trinket_haste / 100
        gear_and_consume_haste = 1 + self.haste / 100
        haste_scaling_factor = trinket_haste * gear_and_consume_haste

        if base_cast_time and haste_scaling_factor:
            return max(base_cast_time / haste_scaling_factor, self.env.GCD)
        else:
            return base_cast_time

    def _spam_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self._shadowbolt()

    def _corruption_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if not self.env.debuffs.is_corruption_active(self):
                yield from self._corruption()
            yield from self._shadowbolt()

    def _corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if not self.env.debuffs.is_corruption_active(self):
                yield from self._corruption()
            if not self.env.debuffs.is_immolate_active(self):
                yield from self._immolate()
            yield from self._shadowbolt()

    def _agony_corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if not self.env.debuffs.is_agony_active(self):
                yield from self._curse_of_agony()
            if not self.env.debuffs.is_corruption_active(self):
                yield from self._corruption()
            if not self.env.debuffs.is_immolate_active(self):
                yield from self._immolate()
            yield from self._shadowbolt()

    def _cos_corruption_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if not self.env.debuffs.has_cos:
                yield from self._curse_of_shadow()
            if not self.env.debuffs.is_corruption_active(self):
                yield from self._corruption()
            yield from self._shadowbolt()

    def _cos_corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if not self.env.debuffs.has_cos:
                yield from self._curse_of_shadow()
            if not self.env.debuffs.is_corruption_active(self):
                yield from self._corruption()
            if not self.env.debuffs.is_immolate_active(self):
                yield from self._immolate()
            yield from self._shadowbolt()

    def _get_hit_chance(self, spell: Spell):
        hit = self.hit
        # if affliction add suppression
        if spell in [Spell.CORRUPTION, Spell.CURSE_OF_AGONY, Spell.CURSE_OF_SHADOW]:
            hit += self.tal.suppression * 2

        return min(83 + self.hit, 99)

    def _shadow_spell(self,
                      spell: Spell,
                      min_dmg: int,
                      max_dmg: int,
                      base_cast_time: float,
                      crit_modifier: float = 0,
                      cooldown: float = 0.0):
        casting_time = self._get_cast_time(base_cast_time)

        # account for gcd
        if casting_time < self.env.GCD:
            cooldown = self.env.GCD - casting_time

        hit = random.randint(1, 100) <= self._get_hit_chance(spell)

        crit_chance = self.crit + crit_modifier
        crit = random.randint(1, 100) <= crit_chance

        dmg = random.randint(min_dmg, max_dmg)
        coeff = SPELL_COEFFICIENTS[spell]
        dmg += (self.sp + self._sp_bonus) * coeff

        if self.env.debuffs.has_cos:
            dmg *= 1.1  # CoE
        if self.env.debuffs.has_nightfall:
            dmg *= 1.15
        if self.tal.demonic_sacrifice:
            dmg *= 1.15
        if self.tal.shadow_mastery:
            dmg *= 1.1

        if self._dmg_modifier != 1:
            dmg *= self._dmg_modifier

        isb_msg = "(ISB)" if self.env.improved_shadow_bolt.is_active else ""
        if hit:
            dmg = int(self.env.improved_shadow_bolt.apply_to_spell(self, dmg))

        yield self.env.timeout(casting_time)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2) + self.lag} cast)"
            if cooldown:
                description += f" ({cooldown} gcd)"

        if not hit:
            dmg = 0
            self.print(f"{spell.value} {description} RESIST")
        elif not crit:
            self.print(f"{isb_msg} {spell.value} {description} {dmg}")
        else:
            mult = 2 if self.tal.ruin else 1.5
            dmg = int(dmg * mult)
            self.print(f"{isb_msg} {spell.value} {description} **{dmg}**")
            # refresh isb
            self.env.improved_shadow_bolt.refresh(self)

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.name, dmg)

        self.num_casts[spell] = self.num_casts.get(spell, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def _fire_spell(self,
                    spell: Spell,
                    min_dmg: int,
                    max_dmg: int,
                    base_cast_time: float,
                    crit_modifier: float = 0,
                    cooldown: float = 0.0):

        casting_time = self._get_cast_time(base_cast_time)
        # account for gcd
        if casting_time < self.env.GCD:
            cooldown = self.env.GCD - casting_time

        hit_chance = self._get_hit_chance(spell)
        hit = random.randint(1, 100) <= hit_chance

        crit_chance = self.crit + crit_modifier
        crit = random.randint(1, 100) <= crit_chance

        coeff = SPELL_COEFFICIENTS[spell]

        dmg = random.randint(min_dmg, max_dmg)
        dmg += (self.sp + self._sp_bonus) * coeff

        if self.env.debuffs.has_coe:
            dmg *= 1.1  # CoE
        if self.env.debuffs.has_nightfall:
            dmg *= 1.15
        if self.tal.emberstorm:
            dmg *= 1 + self.tal.emberstorm * 0.02
        if spell == Spell.IMMOLATE and self.tal.improved_immolate:
            dmg *= 1 + self.tal.improved_immolate * 0.05

        dmg *= 1 + self.env.debuffs.scorch_stacks * 0.03  # imp. scorch
        dmg = int(dmg * self._dmg_modifier)
        if casting_time:
            yield self.env.timeout(casting_time + self.lag)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2) + self.lag} cast)"
            if cooldown:
                description += f" ({cooldown} gcd)"

        if not hit:
            dmg = 0
            self.print(f"{spell.value} {description} RESIST")
        elif not crit:
            self.print(f"{spell.value} {description} {dmg}")
            self.cds.combustion.cast_fire_spell()  # only happens on hit
        else:
            mult = 2 if self.tal.ruin else 1.5
            dmg = int(dmg * mult)
            self.print(f"{spell.value} {description} **{dmg}**")

            self.cds.combustion.use_charge()  # only used on crit
            self.cds.combustion.cast_fire_spell()

        if spell == Spell.IMMOLATE and hit:
            self.env.debuffs.add_immolate_dot(self)

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.name, dmg)

        self.num_casts[spell] = self.num_casts.get(spell, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def _shadow_dot(self,
                    spell: Spell,
                    base_cast_time: float,
                    cooldown: float = 0.0):

        casting_time = self._get_cast_time(base_cast_time)
        # account for gcd
        if casting_time < self.env.GCD:
            cooldown = self.env.GCD - casting_time

        hit_chance = self._get_hit_chance(spell)
        hit = random.randint(1, 100) <= hit_chance

        if casting_time:
            yield self.env.timeout(casting_time + self.lag)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2) + self.lag} cast)"
            if cooldown:
                description += f" ({cooldown} gcd)"

        if not hit:
            self.print(f"{spell.value} {description} RESIST")
        else:
            self.print(f"{spell.value} {description}")
            if spell == Spell.CORRUPTION:
                self.env.debuffs.add_corruption_dot(self)
            elif spell == Spell.CURSE_OF_AGONY:
                self.env.debuffs.add_agony_dot(self)
            elif spell == Spell.CURSE_OF_SHADOW:
                self.env.debuffs.add_curse_of_shadows_dot()

        self.num_casts[spell] = self.num_casts.get(spell, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def _shadowbolt(self):
        min_dmg = 482
        max_dmg = 539
        if self.nightfall:
            casting_time = 0
            self.nightfall = False
        else:
            casting_time = 3 - self.tal.bane * 0.1

        crit_modifier = self.tal.devastation

        yield from self._shadow_spell(spell=Spell.SHADOWBOLT,
                                      min_dmg=min_dmg,
                                      max_dmg=max_dmg,
                                      crit_modifier=crit_modifier,
                                      base_cast_time=casting_time)

    def _immolate(self):
        mult = 1 + .05 * self.tal.improved_immolate
        dmg = int(279 * mult)
        casting_time = 2 - self.tal.bane * 0.4
        crit_modifier = self.tal.devastation

        yield from self._fire_spell(spell=Spell.IMMOLATE,
                                    min_dmg=dmg,
                                    max_dmg=dmg,
                                    crit_modifier=crit_modifier,
                                    base_cast_time=casting_time)

    def _searing_pain(self):
        min_dmg = 204
        max_dmg = 241
        casting_time = 1.5
        crit_modifier = self.tal.improved_searing_pain * 2 + self.tal.devastation

        yield from self._fire_spell(spell=Spell.SEARING_PAIN,
                                    min_dmg=min_dmg,
                                    max_dmg=max_dmg,
                                    crit_modifier=crit_modifier,
                                    base_cast_time=casting_time)

    def _corruption(self):
        cast_time = 2 - self.tal.improved_corruption * 0.4
        yield from self._shadow_dot(spell=Spell.CORRUPTION, base_cast_time=cast_time)

    def _curse_of_shadow(self):
        yield from self._shadow_dot(spell=Spell.CURSE_OF_SHADOW, base_cast_time=0)

    def _curse_of_agony(self):
        yield from self._shadow_dot(spell=Spell.CURSE_OF_AGONY, base_cast_time=0)

    def nightfall_proc(self):
        self.nightfall = True
        self.print("Nightfall proc!")

    def spam_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        # set rotation to internal _spam_fireballs and use partial to pass args and kwargs to that function
        return partial(self._set_rotation, name="spam_shadowbolt")(cds=cds, delay=delay)

    def corruption_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="corruption_shadowbolt")(cds=cds, delay=delay)

    def corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="corruption_immolate_shadowbolt")(cds=cds, delay=delay)

    def agony_corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="agony_corruption_immolate_shadowbolt")(cds=cds, delay=delay)

    def cos_corruption_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="cos_corruption_shadowbolt")(cds=cds, delay=delay)

    def cos_corruption_immolate_shadowbolt(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="cos_corruption_immolate_shadowbolt")(cds=cds, delay=delay)
