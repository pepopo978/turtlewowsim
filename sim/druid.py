import random
from functools import partial

from sim.character import CooldownUsages
from sim.druid_options import DruidOptions
from sim.druid_rotation_cooldowns import ArcaneEclipseCooldown, NatureEclipseCooldown
from sim.druid_talents import DruidTalents
from sim.env import Environment
from sim.equipped_items import EquippedItems
from sim.mage_rotation_cooldowns import *
from sim.spell import Spell, SPELL_COEFFICIENTS, SPELL_TRIGGERS_ON_HIT, SPELL_HITS_MULTIPLE_TARGETS
from sim.spell_school import DamageType
from sim.talent_school import TalentSchool


class Druid(Character):
    def __init__(self,
                 tal: DruidTalents,
                 opts: DruidOptions = DruidOptions(),
                 name: str = '',
                 sp: int = 0,
                 crit: float = 0,
                 hit: float = 0,
                 haste: float = 0,
                 lag: float = 0.07,  # lag added by server tick time
                 equipped_items: EquippedItems = None,
                 ):
        super().__init__(tal, name, sp, crit, hit, haste, lag, equipped_items)
        self.tal = tal
        self.opts = opts
        self.nature_eclipse_rotation = None
        self.arcane_eclipse_rotation = None

    def reset(self):
        super().reset()

    def _setup_cds(self):
        self.arcane_eclipse = ArcaneEclipseCooldown(self)
        self.nature_eclipse = NatureEclipseCooldown(self)

        self.natures_grace_active = False
        self.balance_of_all_things_active = False

    def attach_env(self, env: Environment):
        super().attach_env(env)

        self._setup_cds()

    def _get_cast_time(self, base_cast_time: float, damage_type: DamageType):
        # check for nature's grace
        if base_cast_time > 0 and self.natures_grace_active:
            base_cast_time -= 0.5
            self.natures_grace_active = False

        return super()._get_cast_time(base_cast_time, damage_type)

    def _get_talent_school(self, spell: Spell):
        if spell in [Spell.CORRUPTION, Spell.CURSE_OF_AGONY, Spell.CURSE_OF_SHADOW]:
            return TalentSchool.Affliction
        elif spell in [Spell.SHADOWBOLT, Spell.IMMOLATE, Spell.SEARING_PAIN, Spell.CONFLAGRATE]:
            return TalentSchool.Destruction
        else:
            raise ValueError(f"Unknown spell {spell}")

    def _get_hit_chance(self, spell: Spell, is_binary=False):
        return min(83 + self.hit, 99)

    def _get_crit_multiplier(self, talent_school: TalentSchool, damage_type: DamageType):
        mult = super()._get_crit_multiplier(talent_school, damage_type)
        if self.tal.vengeance:
            mult += 0.1 * self.tal.vengeance
        return mult

    def modify_dmg(self, dmg: int, damage_type: DamageType, is_periodic: bool):
        dmg = super().modify_dmg(dmg, damage_type, is_periodic)

        if self.nature_eclipse.is_active() and damage_type == DamageType.NATURE:
            dmg *= 1.25
        elif self.arcane_eclipse.is_active() and damage_type == DamageType.ARCANE:
            dmg *= 1.25

        if self.tal.moonfury == 1:
            dmg *= 1.03
        elif self.tal.moonfury == 2:
            dmg *= 1.06
        elif self.tal.moonfury == 3:
            dmg *= 1.1

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
               on_gcd: bool,
               calculate_cast_time: bool = True):
        had_natures_grace = self.natures_grace_active

        casting_time = self._get_cast_time(base_cast_time, damage_type) if calculate_cast_time else base_cast_time

        # account for gcd
        gcd = self.env.GCD
        if spell == Spell.WRATH:
            gcd -= 0.1 * self.tal.imp_wrath
        if on_gcd and casting_time < gcd and cooldown == 0:
            cooldown = gcd - casting_time if casting_time > self.lag else gcd
            if casting_time == 0:
                cooldown += self.lag

        hit = self._roll_hit(self._get_hit_chance(spell), damage_type)
        crit = False
        dmg = 0
        if hit:
            crit = self._roll_crit(self.crit + crit_modifier, damage_type)
            dmg = self.roll_spell_dmg(min_dmg, max_dmg, SPELL_COEFFICIENTS.get(spell, 0), damage_type)
            dmg = self.modify_dmg(dmg, damage_type, is_periodic=False)
        else:
            self.num_resists += 1

        is_binary_spell = spell in {}

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
                description += f" ({round(cooldown, 2)} gcd)"

            if had_natures_grace:
                description += " (NG)"
        if not hit:
            self.print(f"{spell.value} {description} RESIST")
        elif not crit:
            self.print(f"{spell.value} {description} {partial_desc} {dmg}")
        else:
            mult = self._get_crit_multiplier(talent_school, damage_type)
            dmg = int(dmg * mult)

            if spell == Spell.STARFIRE and not self.arcane_eclipse.is_active():
                # try to activate eclipse
                self.nature_eclipse.activate()
            elif spell == Spell.WRATH and not self.nature_eclipse.is_active():
                self.arcane_eclipse.activate()

            if self.tal.natures_grace:
                self.natures_grace_active = True

            self.print(f"{spell.value} {description} {partial_desc} **{dmg}**")

        if hit and spell == Spell.MOONFIRE:
            self.env.debuffs.add_moonfire_dot(self)

        if hit and SPELL_TRIGGERS_ON_HIT.get(spell, False):
            self._check_for_procs()

        self.env.meter.register_spell_dmg(
            char_name=self.name,
            spell_name=spell.value,
            dmg=dmg,
            cast_time=round(casting_time + cooldown, 2),
            aoe=spell in SPELL_HITS_MULTIPLE_TARGETS)

        return hit, crit, dmg, cooldown, partial_amount

    def _arcane_spell(self,
                      spell: Spell,
                      min_dmg: int,
                      max_dmg: int,
                      base_cast_time: float,
                      crit_modifier: float,
                      cooldown: float = 0.0,
                      on_gcd: bool = True,
                      calculate_cast_time: bool = True):

        hit, crit, dmg, cooldown, partial_amount = yield from self._spell(spell=spell,
                                                                          damage_type=DamageType.ARCANE,
                                                                          talent_school=TalentSchool.Balance,
                                                                          min_dmg=min_dmg,
                                                                          max_dmg=max_dmg,
                                                                          base_cast_time=base_cast_time,
                                                                          crit_modifier=crit_modifier,
                                                                          cooldown=cooldown,
                                                                          on_gcd=on_gcd,
                                                                          calculate_cast_time=calculate_cast_time)

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown)

    def _starfire(self):
        # use rank 2 to get full spell coefficient
        min_dmg = 496
        max_dmg = 585
        casting_time = 3.5
        crit_modifier = 0

        if self.tal.imp_starfire == 1:
            casting_time -= 0.17
        elif self.tal.imp_starfire == 2:
            casting_time -= 0.34
        elif self.tal.imp_starfire == 3:
            casting_time -= 0.5

        if self.balance_of_all_things_active:
            casting_time -= 0.75
            self.balance_of_all_things_active = False

        yield from self._nature_spell(spell=Spell.STARFIRE,
                                      min_dmg=min_dmg,
                                      max_dmg=max_dmg,
                                      base_cast_time=casting_time,
                                      crit_modifier=crit_modifier)

    def _nature_spell(self,
                      spell: Spell,
                      min_dmg: int,
                      max_dmg: int,
                      base_cast_time: float,
                      crit_modifier: float,
                      cooldown: float = 0.0,
                      on_gcd: bool = True,
                      calculate_cast_time: bool = True):

        hit, crit, dmg, cooldown, partial_amount = yield from self._spell(spell=spell,
                                                                          damage_type=DamageType.NATURE,
                                                                          talent_school=TalentSchool.Balance,
                                                                          min_dmg=min_dmg,
                                                                          max_dmg=max_dmg,
                                                                          base_cast_time=base_cast_time,
                                                                          crit_modifier=crit_modifier,
                                                                          cooldown=cooldown,
                                                                          on_gcd=on_gcd,
                                                                          calculate_cast_time=calculate_cast_time)

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown)

    def _wrath(self):
        # use rank 2 to get full spell coefficient
        min_dmg = 278
        max_dmg = 313
        casting_time = 2.0 - 0.1 * self.tal.imp_wrath
        crit_modifier = 0

        yield from self._nature_spell(spell=Spell.WRATH,
                                      min_dmg=min_dmg,
                                      max_dmg=max_dmg,
                                      base_cast_time=casting_time,
                                      crit_modifier=crit_modifier)

    def _moonfire(self):
        # use rank 2 to get full spell coefficient
        min_dmg = 189
        max_dmg = 222
        casting_time = 0
        crit_modifier = 0

        if self.tal.imp_moonfire > 0:
            min_dmg *= 1 + 0.05 * self.tal.imp_moonfire
            min_dmg = int(min_dmg)
            max_dmg *= 1 + 0.05 * self.tal.imp_moonfire
            max_dmg = int(max_dmg)
            crit_modifier = 5 * self.tal.imp_moonfire

        yield from self._nature_spell(spell=Spell.MOONFIRE,
                                      min_dmg=min_dmg,
                                      max_dmg=max_dmg,
                                      base_cast_time=casting_time,
                                      crit_modifier=crit_modifier)

    def _nature_dot(self,
                    spell: Spell,
                    base_cast_time: float,
                    cooldown: float = 0.0):

        casting_time = self._get_cast_time(base_cast_time, DamageType.NATURE)

        # account for gcd
        if casting_time < self.env.GCD and cooldown == 0:
            cooldown = self.env.GCD - casting_time + self.lag

        hit_chance = self._get_hit_chance(spell)
        hit = random.randint(1, 100) <= hit_chance

        if casting_time:
            yield self.env.timeout(casting_time)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2)} cast)"
            if cooldown:
                description += f" ({round(cooldown, 2)} gcd)"

        if not hit:
            self.print(f"{spell.value} {description} RESIST")
        else:
            self.print(f"{spell.value} {description}")
            if spell == Spell.INSECT_SWARM:
                self.env.debuffs.add_insect_swarm_dot(self, round(casting_time + cooldown, 2))

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown)

    def _insect_swarm(self):
        # use rank 2 to get full spell coefficient
        min_dmg = 278
        max_dmg = 313
        casting_time = 0
        crit_modifier = 0

        yield from self._nature_dot(spell=Spell.INSECT_SWARM,
                                    base_cast_time=casting_time)

    # subrotations for different eclipse states
    def insect_swarm_wrath_subrotation(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        if not self.env.debuffs.is_insect_swarm_active(self):
            yield from self._insect_swarm()
        else:
            yield from self._wrath()

    def insect_swarm_moonfire_wrath_subrotation(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        if not self.env.debuffs.is_insect_swarm_active(self):
            yield from self._insect_swarm()
        elif not self.env.debuffs.is_moonfire_active(self):
            yield from self._moonfire()
        else:
            yield from self._wrath()


    def moonfire_starfire_subrotation(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        if not self.env.debuffs.is_moonfire_active(self):
            yield from self._moonfire()
        else:
            yield from self._starfire()

    def moonfire_insect_swarm_starfire_subrotation(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        if not self.env.debuffs.is_moonfire_active(self):
            yield from self._moonfire()
        elif not self.env.debuffs.is_insect_swarm_active(self):
            yield from self._insect_swarm()
        else:
            yield from self._starfire()


    def set_nature_eclipse_subrotation(self, rotation):
        self.nature_eclipse_rotation = rotation

    def set_arcane_eclipse_subrotation(self, rotation):
        self.arcane_eclipse_rotation = rotation

    def _base_rotation(self, cds: CooldownUsages = CooldownUsages(), delay=2, rotation_callback=None):
        self._use_cds(cds)
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if self.opts.starfire_on_balance_of_all_things_proc and self.balance_of_all_things_active:
                yield from self._starfire()
            elif self.nature_eclipse.is_active() and self.nature_eclipse_rotation and not self.opts.ignore_nature_eclipse:
                yield from self.nature_eclipse_rotation(self)
            elif self.arcane_eclipse.is_active() and self.arcane_eclipse_rotation and not self.opts.ignore_arcane_eclipse:
                yield from self.arcane_eclipse_rotation(self)
            elif rotation_callback:
                yield from rotation_callback()

    # Regular rotations when not in eclipse
    def _spam_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            yield from self._starfire()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _spam_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            yield from self._wrath()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _moonfire_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_moonfire_active(self):
                yield from self._moonfire()
            else:
                yield from self._starfire()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _insect_swarm_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_insect_swarm_active(self):
                yield from self._insect_swarm()
            else:
                yield from self._starfire()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _insect_swarm_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_insect_swarm_active(self):
                yield from self._insect_swarm()
            else:
                yield from self._wrath()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _moonfire_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_moonfire_active(self):
                yield from self._moonfire()
            else:
                yield from self._wrath()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _moonfire_insect_swarm_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_moonfire_active(self):
                yield from self._moonfire()
            elif not self.env.debuffs.is_insect_swarm_active(self):
                yield from self._insect_swarm()
            else:
                yield from self._wrath()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def _moonfire_insect_swarm_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        def _rotation_callback():
            if not self.env.debuffs.is_moonfire_active(self):
                yield from self._moonfire()
            elif not self.env.debuffs.is_insect_swarm_active(self):
                yield from self._insect_swarm()
            else:
                yield from self._starfire()

        return self._base_rotation(cds=cds, delay=delay, rotation_callback=_rotation_callback)

    def spam_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_starfire")(cds=cds, delay=delay)

    def spam_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="spam_wrath")(cds=cds, delay=delay)

    def moonfire_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="moonfire_starfire")(cds=cds, delay=delay)

    def insect_swarm_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="insect_swarm_starfire")(cds=cds, delay=delay)

    def insect_swarm_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="insect_swarm_wrath")(cds=cds, delay=delay)

    def moonfire_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="moonfire_wrath")(cds=cds, delay=delay)

    def moonfire_insect_swarm_wrath(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="moonfire_insect_swarm_wrath")(cds=cds, delay=delay)

    def moonfire_insect_swarm_starfire(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        return partial(self._set_rotation, name="moonfire_insect_swarm_starfire")(cds=cds, delay=delay)
