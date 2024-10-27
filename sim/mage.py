import random
from functools import partial
from typing import Optional

from sim.character import Character, CooldownUsages
from sim.cooldowns import Cooldown
from sim.env import Environment
from sim.hot_streak import HotStreak
from sim.mage_options import MageOptions
from sim.mage_talents import MageTalents
from sim.spell import Spell, SPELL_COEFFICIENTS
from sim.spell_school import DamageType
from sim.talent_school import TalentSchool


class FireBlastCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self._cd = cooldown

    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return self._cd


class FrostNovaCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self._cd = cooldown

    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return self._cd


class Mage(Character):
    def __init__(self,
                 tal: MageTalents,
                 opts: MageOptions = MageOptions(),
                 name: str = '',
                 sp: int = 0,
                 crit: float = 0,
                 hit: float = 0,
                 haste: float = 0,
                 lag: float = 0.07,  # lag added by server tick time
                 ):
        super().__init__(name, sp, crit, hit, haste, lag)
        self.hot_streak = None
        self.tal = tal
        self.opts = opts

        self._t2proc: bool = False
        self._flash_freeze_proc: bool = False

        self._ice_barrier_expiration = 0
        if opts.start_with_ice_barrier:
            self._ice_barrier_expiration = opts.starting_ice_barrier_duration

    def reset(self):
        super().reset()

        self._t2proc = False
        self._flash_freeze_proc = False

    def attach_env(self, env: Environment):
        super().attach_env(env)

        self.fire_blast_cd = FireBlastCooldown(self, self.tal.fire_blast_cooldown)
        self.frost_nova_cd = FrostNovaCooldown(self, self.tal.frost_nova_cooldown)

        if self.tal.hot_streak:
            self.hot_streak = HotStreak(env, self)

    def _ice_barrier_active(self):
        return self._ice_barrier_expiration >= self.env.now

    def _spam_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self._fireball()

    def _spam_pyroblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self._pyroblast()

    def _spam_frostbolts(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if self.tal.ice_barrier and not self._ice_barrier_active():
                yield from self._ice_barrier()
            if self.opts.use_frostnova_for_icicles and self.frost_nova_cd.usable:
                yield from self._frost_nova()
            else:
                yield from self._frostbolt()

    def _spam_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self._scorch()

    def _spam_scorch_unless_mqg(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if self.cds.mqg.is_active():
                yield from self._fireball()
            else:
                yield from self._scorch()

    def _one_scorch_then_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """1 scorch then 9 fireballs rotation"""
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self._scorch()
            for _ in range(9):
                self._use_cds(cds)
                yield from self._fireball()

    def _smart_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """ Cast scorch if less than 5 imp scorch stacks or if 5 stack ignite
        and extend_ignite_with_scorch else cast fireball"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(cds)

            if self.env.debuffs.scorch_stacks < 5 or self.env.debuffs.scorch_timer <= 4.5:
                yield from self._scorch()
            else:
                yield from self._fireball()

    def _smart_scorch_and_fireblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """Same as above except fireblast on cd"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(cds)
            if self.env.debuffs.scorch_stacks < 5 or self.env.debuffs.scorch_timer <= 4.5:
                yield from self._scorch()
            elif self.fire_blast_cd.usable:
                yield from self._fire_blast()
            else:
                yield from self._fireball()

    def _one_scorch_one_pyro_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=1):
        yield from self._random_delay(delay)

        self._use_cds(cds)
        yield from self._scorch()
        self._use_cds(cds)
        yield from self._pyroblast()
        for _ in range(7):
            self._use_cds(cds)
            yield from self._fireball()

        yield from self._one_scorch_then_fireballs(cds, delay=0)

    def _one_scorch_one_frostbolt_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=1):
        yield from self._random_delay(delay)

        self._use_cds(cds)
        yield from self._scorch()
        self._use_cds(cds)
        yield from self._frostbolt()
        for _ in range(8):
            self._use_cds(cds)
            yield from self._fireball()

        yield from self._one_scorch_then_fireballs(cds, delay=0)

    def _get_cast_time(self, base_cast_time: float):
        # check for pom
        if self.cds.presence_of_mind.is_active():
            self.cds.presence_of_mind.deactivate()
            return self.lag

        trinket_haste = 1 + self._trinket_haste / 100
        gear_and_consume_haste = 1 + self.haste / 100
        haste_scaling_factor = trinket_haste * gear_and_consume_haste

        if base_cast_time and haste_scaling_factor:
            return base_cast_time / haste_scaling_factor + self.lag
        else:
            return base_cast_time + self.lag

    def _get_talent_school(self, spell: Spell):
        if spell in [Spell.CORRUPTION, Spell.CURSE_OF_AGONY, Spell.CURSE_OF_SHADOW]:
            return TalentSchool.Affliction
        elif spell in [Spell.SHADOWBOLT, Spell.IMMOLATE, Spell.SEARING_PAIN, Spell.CONFLAGRATE]:
            return TalentSchool.Destruction
        else:
            raise ValueError(f"Unknown spell {spell}")

    def _get_hit_chance(self, spell: Spell, is_binary=False):
        # elemental precision assumed to be included in hit already
        return min(83 + self.hit, 99)

    def _get_crit_multiplier(self, dmg_type: DamageType, talent_school: TalentSchool):
        mult = super()._get_crit_multiplier(dmg_type, talent_school)
        if dmg_type == DamageType.Frost:
            mult = 1.5 + self.tal.ice_shards * 0.1
        return mult

    def modify_dmg(self, dmg: int, dmg_type: DamageType, is_periodic: bool):
        dmg = super().modify_dmg(dmg, dmg_type, is_periodic)

        if dmg_type == DamageType.Fire and self.tal.fire_power:
            dmg *= 1.1

        if self.tal.piercing_ice and dmg_type == DamageType.Frost:
            dmg *= 1.06

        if self.tal.ice_barrier and dmg_type == DamageType.Frost and self._ice_barrier_active():
            dmg *= 1.15

        return int(dmg)

    # caller must handle any gcd cooldown
    def _spell(self,
               spell: Spell,
               damage_type: DamageType,
               talent_school: TalentSchool,
               min_dmg: int,
               max_dmg: int,
               base_cast_time: float,
               crit_modifier: float,
               cooldown: float,
               on_gcd: bool):

        casting_time = self._get_cast_time(base_cast_time)
        if self._t2proc:
            casting_time = self.lag
            self._t2proc = False
            self.print("T2 proc used")

        # account for gcd
        if on_gcd and casting_time < self.env.GCD and cooldown == 0:
            cooldown = self.env.GCD - casting_time + self.lag

        hit = self._roll_hit(self._get_hit_chance(spell))
        crit = False
        dmg = 0
        if hit:
            crit = self._roll_crit(self.crit + crit_modifier)
            dmg = self._roll_spell_dmg(min_dmg, max_dmg, SPELL_COEFFICIENTS[spell])
            dmg = self.modify_dmg(dmg, damage_type, is_periodic=False)

        is_binary_spell = (
                spell == Spell.FROSTBOLT or
                spell == Spell.ICICLE or
                spell == Spell.FROST_NOVA or
                spell == Spell.CONE_OF_COLD)

        partial_amount = self.roll_partial(is_dot=False, is_binary=is_binary_spell)
        partial_desc = ""
        if partial_amount < 1:
            dmg = int(dmg * partial_amount)
            partial_desc = f"({int(partial_amount * 100)}% partial)"

        if casting_time:
            yield self.env.timeout(casting_time)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2)} cast)"
            if cooldown:
                description += f" ({cooldown} gcd)"

        if not hit:
            self.print(f"{spell.value} {description} RESIST")
        elif not crit:
            self.print(f"{spell.value} {description} {partial_desc} {dmg}")
        else:
            mult = self._get_crit_multiplier(damage_type, talent_school)
            dmg = int(dmg * mult)
            self.print(f"{spell.value} {description} {partial_desc} **{dmg}**")

        if hit and self.opts.fullt2 and (
                spell == Spell.FIREBALL or
                spell == Spell.FROSTBOLT or
                spell == Spell.ARCANE_MISSILES):
            if random.randint(1, 100) <= 10:
                self._t2proc = True
                self.print("T2 proc")

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.name, dmg)

        self.num_casts[spell] = self.num_casts.get(spell, 0) + 1

        return hit, crit, dmg, cooldown

    def _fire_spell(self,
                    spell: Spell,
                    min_dmg: int,
                    max_dmg: int,
                    base_cast_time: float,
                    crit_modifier: float,
                    cooldown: float = 0.0,
                    on_gcd: bool = True):
        # check for ignite conditions
        has_5_stack_scorch = self.env.debuffs.scorch_stacks == 5
        has_5_stack_ignite = self.env.ignite and self.env.ignite.stacks == 5
        has_scorch_ignite = has_5_stack_ignite and self.env.ignite.is_suboptimal()

        # check for hot streak pyroblast
        if self.hot_streak and self.hot_streak.get_stacks() == 9 and self.opts.pyro_on_9_hot_streak:
            self.print("Hot Streak Pyroblast")
            self.hot_streak.use_stacks()
            yield from self._pyroblast(casting_time=1.5)
            return

        # check for scorch ignite drop
        if self.opts.drop_suboptimal_ignites and has_scorch_ignite and spell != Spell.PYROBLAST:
            yield from self._frostbolt()  # have to use frostbolt with 6s ignite window
            return

        # check for ignite extension
        if has_5_stack_scorch and has_5_stack_ignite:
            # check that spell is not already fireblast or scorch
            if spell not in (Spell.FIREBLAST, Spell.SCORCH):
                if self.env.ignite.ticks_left <= self.opts.remaining_ticks_for_ignite_extend:
                    if self.opts.extend_ignite_with_fire_blast and self.fire_blast_cd.usable:
                        yield from self._fire_blast()
                        return
                    if self.opts.extend_ignite_with_scorch:
                        yield from self._scorch()
                        return

        hit, crit, dmg, cooldown = yield from self._spell(spell=spell,
                                                          damage_type=DamageType.Fire,
                                                          talent_school=TalentSchool.Fire,
                                                          min_dmg=min_dmg,
                                                          max_dmg=max_dmg,
                                                          base_cast_time=base_cast_time,
                                                          crit_modifier=crit_modifier,
                                                          cooldown=cooldown,
                                                          on_gcd=on_gcd)

        if hit:
            self.cds.combustion.cast_fire_spell()  # only happens on hit

            if spell == Spell.FIREBALL:
                self.env.debuffs.add_fireball_dot(self)
            elif spell == Spell.PYROBLAST:
                self.env.debuffs.add_pyroblast_dot(self)
            elif spell == Spell.SCORCH and self.tal.imp_scorch:
                # roll for whether debuff hits
                fire_vuln_hit = self._roll_hit(self._get_hit_chance(spell))
                if fire_vuln_hit:
                    self.env.debuffs.scorch()

        if crit:
            if self.tal.ignite:
                self.env.ignite.refresh(self, dmg, spell)

            # check for hot streak
            if self.hot_streak and (spell == Spell.FIREBALL or spell == Spell.FIREBLAST):
                self.hot_streak.add_stack()

            self.cds.combustion.use_charge()  # only used on crit

        if spell == Spell.FIREBLAST:
            self.fire_blast_cd.activate()

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown)

    def _frost_spell(self,
                     spell: Spell,
                     min_dmg: int,
                     max_dmg: int,
                     base_cast_time: float,
                     crit_modifier: float,
                     cooldown: float = 0.0,
                     on_gcd: bool = True):

        # check for flash freeze
        if self._flash_freeze_proc:
            self._flash_freeze_proc = False
            yield from self._icicles_channel(channel_time=1.0)
            return

        crit_modifier += self.env.debuffs.wc_stacks * 2  # winters chill added crit (2% per stack)

        hit, crit, dmg, cooldown = yield from self._spell(spell=spell,
                                                          damage_type=DamageType.Frost,
                                                          talent_school=TalentSchool.Frost,
                                                          min_dmg=min_dmg,
                                                          max_dmg=max_dmg,
                                                          base_cast_time=base_cast_time,
                                                          crit_modifier=crit_modifier,
                                                          cooldown=cooldown,
                                                          on_gcd=on_gcd)

        if hit:
            if self.tal.winters_chill:
                # roll for whether debuff hits
                winters_chill_hit = self._roll_hit(self._get_hit_chance(spell))
                if winters_chill_hit:
                    self.env.debuffs.add_winters_chill_stack()

            if self.tal.flash_freeze:
                flash_freeze_hit = False
                if spell == Spell.FROSTBOLT or spell == Spell.CONE_OF_COLD:
                    flash_freeze_hit = (self._roll_hit(5 * self.tal.frostbite) and
                                        self._roll_hit(50 * self.tal.flash_freeze))
                elif spell == Spell.FROST_NOVA:
                    flash_freeze_hit = self._roll_hit(50 * self.tal.flash_freeze)

                if flash_freeze_hit:
                    self._flash_freeze_proc = 1
                    self.print("Flash Freeze proc")

        if spell == Spell.FROST_NOVA:
            self.frost_nova_cd.activate()

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown)

    def _scorch(self):
        min_dmg = 237
        max_dmg = 280
        casting_time = 1.5
        crit_modifier = 0

        crit_modifier += self.tal.incinerate_crit  # incinerate added crit (2 or 4%)

        yield from self._fire_spell(spell=Spell.SCORCH,
                                    min_dmg=min_dmg,
                                    max_dmg=max_dmg,
                                    base_cast_time=casting_time,
                                    crit_modifier=crit_modifier)

    def _fireball(self):
        min_dmg = 596
        max_dmg = 760
        casting_time = 3
        crit_modifier = 0
        if self.tal.critical_mass:
            crit_modifier += 6

        if self.opts.pyro_on_t2_proc and self._t2proc:
            yield from self._pyroblast()
        else:
            yield from self._fire_spell(spell=Spell.FIREBALL,
                                        min_dmg=min_dmg,
                                        max_dmg=max_dmg,
                                        base_cast_time=casting_time,
                                        crit_modifier=crit_modifier)

    def _fire_blast(self):
        min_dmg = 431
        max_dmg = 510
        casting_time = 0
        crit_modifier = 0
        if self.tal.critical_mass:
            crit_modifier += 6

        crit_modifier += self.tal.incinerate_crit  # incinerate added crit (2 or 4%)

        yield from self._fire_spell(spell=Spell.FIREBLAST,
                                    min_dmg=min_dmg,
                                    max_dmg=max_dmg,
                                    base_cast_time=casting_time,
                                    crit_modifier=crit_modifier,
                                    cooldown=self.tal.fire_blast_gcd)

    def _pyroblast(self, casting_time=6.0):
        min_dmg = 716
        max_dmg = 890
        crit_modifier = 0
        if self.tal.critical_mass:
            crit_modifier += 6

        yield from self._fire_spell(spell=Spell.PYROBLAST,
                                    min_dmg=min_dmg,
                                    max_dmg=max_dmg,
                                    base_cast_time=casting_time,
                                    crit_modifier=crit_modifier)

    def _frostbolt(self):
        min_dmg = 515
        max_dmg = 556
        casting_time = 2.5
        crit_modifier = 0

        yield from self._frost_spell(spell=Spell.FROSTBOLT,
                                     min_dmg=min_dmg,
                                     max_dmg=max_dmg,
                                     base_cast_time=casting_time,
                                     crit_modifier=crit_modifier)

    def _frost_nova(self):
        # use rank 2 to get full spell coefficient
        min_dmg = 33
        max_dmg = 38
        casting_time = 0
        crit_modifier = 0

        yield from self._frost_spell(spell=Spell.FROST_NOVA,
                                     min_dmg=min_dmg,
                                     max_dmg=max_dmg,
                                     base_cast_time=casting_time,
                                     crit_modifier=crit_modifier)

    def _ice_barrier(self):
        self._ice_barrier_expiration = self.env.now + 60

        if self.env.print:
            description = f"({round(self.lag, 2)} cast)"
            description += f" ({self.env.GCD} gcd)"
            self.print(f"Ice Barrier {description}")
        yield self.env.timeout(self.env.GCD + self.lag)

    def _icicle(self, casting_time: float = 1):
        min_dmg = 272
        max_dmg = 272

        yield from self._frost_spell(spell=Spell.ICICLE,
                                     min_dmg=min_dmg,
                                     max_dmg=max_dmg,
                                     base_cast_time=casting_time,
                                     crit_modifier=0,
                                     on_gcd=False)

    def _icicles_channel(self, channel_time: float = 5):
        num_icicles = 5
        time_between_icicles = channel_time / num_icicles - self.lag

        for i in range(num_icicles):
            if i == 0:
                yield from self._icicle(casting_time=time_between_icicles + self.lag)  # initial delay
            else:
                yield from self._icicle(casting_time=time_between_icicles)

    def spam_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        # set rotation to internal _spam_fireballs and use partial to pass args and kwargs to that function
        return partial(self._set_rotation, name="spam_fireballs")(cds=cds, delay=delay)

    def spam_pyroblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_pyroblast")(cds=cds, delay=delay)

    def spam_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_scorch")(cds=cds, delay=delay)

    def spam_scorch_unless_mqg(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_scorch_unless_mqg")(cds=cds, delay=delay)

    def smart_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="smart_scorch")(cds=cds, delay=delay)

    def smart_scorch_and_fireblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="smart_scorch_and_fireblast")(cds=cds, delay=delay)

    def one_scorch_then_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="one_scorch_then_fireballs")(cds=cds, delay=delay)

    def one_scorch_one_pyro_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="one_scorch_one_pyro_then_fb")(cds=cds, delay=delay)

    def one_scorch_one_frostbolt_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="one_scorch_one_frostbolt_then_fb")(cds=cds, delay=delay)

    def spam_frostbolts(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_frostbolts")(cds=cds, delay=delay)
