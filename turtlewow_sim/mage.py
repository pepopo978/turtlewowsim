import random
from functools import partial

from turtlewow_sim.character import Character, CooldownUsages

SPELL_COEFFICIENTS = {
    'fireball': 1.0,
    'pyroblast': 1.0,
    'scorch': 0.4285,
    'fireblast': 0.4285,
    'frostbolt': 0.814,
}


class Mage(Character):
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

    def _spam_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self.fireball()

    def _spam_pyroblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self.pyroblast()

    def _spam_frostbolts(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self.frostbolt()

    def _spam_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self.scorch()

    def _spam_scorch_unless_mqg(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            if self.cds.mqg.is_active():
                yield from self.fireball()
            else:
                yield from self.scorch()

    def _one_scorch_then_fireballs(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """1 scorch then 9 fireballs rotation"""
        yield from self._random_delay(delay)

        while True:
            self._use_cds(cds)
            yield from self.scorch()
            for _ in range(9):
                self._use_cds(cds)
                yield from self.fireball()

    def _smart_scorch(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """ Cast scorch if less than 5 imp scorch stacks or if 5 stack ignite
        and extend_ignite_with_scorch else cast fireball"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(cds)
            has_5_stack_ignite = self.env.ignite and self.env.ignite.stacks == 5
            has_scorch_ignite = has_5_stack_ignite and self.env.ignite.is_suboptimal()
            if has_scorch_ignite and self.opts.drop_scorch_ignites:
                # let ignite drop
                yield from self.pyroblast()
            elif self.env.debuffs.scorch_stacks < 5 or (has_scorch_ignite and self.opts.extend_ignite_with_scorch):
                yield from self.scorch()
            else:
                # check if scorch about to fall off
                if self.env.debuffs.scorch_timer <= 4.5:
                    yield from self.scorch()
                else:
                    yield from self.fireball()

    def _smart_scorch_and_fireblast(self, cds: CooldownUsages = CooldownUsages(), delay=2):
        """Same as above except fireblast on cd"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(cds)
            if (self.env.debuffs.scorch_stacks == 5 and
                    self.fire_blast_remaining_cd <= 0 and
                    self.env.ignite.stacks == 5 and self.env.ignite.ticks_left <= 1):
                yield from self.fire_blast()
                self.fire_blast_remaining_cd = self.tal.fire_blast_cooldown - 1.5
                # fire blast cd - gcd
            elif self.env.debuffs.scorch_stacks < 5 or \
                    (self.env.ignite.stacks == 5 and self.opts.extend_ignite_with_scorch):
                yield from self.scorch()
                self.fire_blast_remaining_cd -= 1.5
            else:
                # check if scorch about to fall off
                if self.env.debuffs.scorch_timer <= 5:
                    yield from self.scorch()
                    self.fire_blast_remaining_cd -= 1.5
                else:
                    yield from self.fireball()
                    self.fire_blast_remaining_cd -= 3

    def _one_scorch_one_pyro_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=1):
        yield from self._random_delay(delay)

        self._use_cds(cds)
        yield from self.scorch()
        self._use_cds(cds)
        yield from self.pyroblast()
        for _ in range(7):
            self._use_cds(cds)
            yield from self.fireball()

        yield from self._one_scorch_then_fireballs(cds, delay=0)

    def _one_scorch_one_frostbolt_then_fb(self, cds: CooldownUsages = CooldownUsages(), delay=1):
        yield from self._random_delay(delay)

        self._use_cds(cds)
        yield from self.scorch()
        self._use_cds(cds)
        yield from self.frostbolt()
        for _ in range(8):
            self._use_cds(cds)
            yield from self.fireball()

        yield from self._one_scorch_then_fireballs(cds, delay=0)

    def get_cast_time(self, base_cast_time):
        # check for pom
        if self.cds.presence_of_mind.is_active():
            self.cds.presence_of_mind.deactivate()
            return 0

        trinket_haste = 1 + self._trinket_haste / 100
        gear_and_consume_haste = 1 + self.haste / 100
        haste_scaling_factor = trinket_haste * gear_and_consume_haste

        if base_cast_time and haste_scaling_factor:
            return max(base_cast_time / haste_scaling_factor, 1.5)
        else:
            return base_cast_time

    def fireball(self):
        min_dmg = 596
        max_dmg = 760
        casting_time = 3

        if self.opts.pyro_on_t2_proc and self._t2proc >= 0:
            yield self.env.timeout(0.05)  # small delay between spells
            yield from self.pyroblast()
        else:
            yield from self._fire_spell(name='fireball', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time)

    def _fire_spell(self, name, min_dmg, max_dmg, base_cast_time, crit_modifier=0, cooldown=0.0):
        casting_time = self.get_cast_time(base_cast_time)
        if self._t2proc >= 0:
            casting_time = 0
            self._t2proc = -1
            self.print("T2 proc used")
        elif self._t2proc == 1:
            self._t2proc = 0  # delay using t2 until next spell

        # account for gcd
        if casting_time < 1.5:
            cooldown = 1.5 - casting_time

        hit_chance = min(83 + self.hit, 99)
        hit = random.randint(1, 100) <= hit_chance

        crit_chance = self.crit + crit_modifier + self.cds.combustion.crit_bonus
        if self.tal.arcane_instability:
            crit_chance += 3

        crit = random.randint(1, 100) <= crit_chance

        coeff = SPELL_COEFFICIENTS[name]

        dmg = random.randint(min_dmg, max_dmg)
        dmg += (self.sp + self._sp_bonus) * coeff

        if self.tal.fire_power:
            dmg *= 1.1  # Fire Power
        if self.tal.arcane_instability:
            dmg *= 1.03
        if self.env.debuffs.coe:
            dmg *= 1.1  # CoE
        if self.env.debuffs.nightfall:
            dmg *= 1.15

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
            self.print(f"{name} {description} RESIST")
        elif not crit:
            self.print(f"{name} {description} {dmg}")
            self.cds.combustion.cast_fire_spell() # only happens on hit
        else:
            dmg = int(dmg * 1.5)
            self.print(f"{name} {description} **{dmg}**")
            self.env.ignite.refresh(self, dmg, name)

            self.cds.combustion.use_charge()  # only used on crit
            self.cds.combustion.cast_fire_spell()

        if name == 'fireball':
            self.env.debuffs.add_fireball_dot(self)

        if name == 'pyroblast':
            self.env.debuffs.add_pyroblast_dot(self)

        if name == 'scorch' and self.tal.imp_scorch and hit:
            # roll for whether debuff hits
            fire_vuln_hit = random.randint(1, 100) <= hit_chance
            if fire_vuln_hit:
                self.env.debuffs.scorch()

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.name, dmg)
        if self.opts.fullt2 and name == 'fireball':
            if random.randint(1, 100) <= 10:
                self._t2proc = 1
                self.print("T2 proc")

        self.num_casts[name] = self.num_casts.get(name, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def _frost_spell(self, name, min_dmg, max_dmg, base_cast_time, cooldown=0):
        casting_time = self.get_cast_time(base_cast_time)
        if self._t2proc == 0:
            casting_time = 0
            self._t2proc = -1
            self.print("T2 proc used")
        elif self._t2proc == 1:
            self._t2proc = 0  # delay using t2 until next spell

        # account for gcd
        if casting_time < 1.5:
            cooldown = 1.5 - casting_time

        hit_chance = min(83 + self.hit, 99)
        hit = random.randint(1, 100) <= hit_chance

        crit_chance = self.crit + self.env.debuffs.wc_stacks * 2
        if self.tal.arcane_instability:
            crit_chance += 3
        if self.tal.critial_mass:
            crit_chance += 6

        crit = random.randint(1, 100) <= crit_chance

        dmg = random.randint(min_dmg, max_dmg)
        coeff = SPELL_COEFFICIENTS[name]
        dmg += (self.sp + self._sp_bonus) * coeff

        if self.tal.piercing_ice:
            dmg *= 1.06  # Piercing Ice
        if self.tal.arcane_instability:
            dmg *= 1.03
        if self.env.debuffs.coe:
            dmg *= 1.1  # CoE
        if self.env.debuffs.nightfall:
            dmg *= 1.15

        dmg = int(dmg * self._dmg_modifier)
        yield self.env.timeout(casting_time)

        description = ""
        if self.env.print:
            description = f"({round(casting_time, 2) + self.lag} cast)"
            if cooldown:
                description += f" ({cooldown} gcd)"

        if not hit:
            dmg = 0
            self.print(f"{name} {description} RESIST")
        elif not crit:
            self.print(f"{name} {description} {dmg}")

        else:
            dmg = int(dmg * 2)
            self.print(f"{name} {description} **{dmg}**")

        if self.tal.winters_chill:
            # roll for whether debuff hits
            winters_chill_hit = random.randint(1, 100) <= hit_chance
            if winters_chill_hit:
                self.env.debuffs.winters_chill()

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self.name, dmg)
        if self.opts.fullt2 and name == 'frostbolt':
            if random.randint(1, 100) <= 10:
                self.opts._t2proc = 1
                self.print("T2 proc")

        self.num_casts[name] = self.num_casts.get(name, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def scorch(self):
        min_dmg = 237
        max_dmg = 280
        casting_time = 1.5
        crit_modifier = 4 if self.tal.incinerate else 0

        yield from self._fire_spell(name='scorch', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time,
                                    crit_modifier=crit_modifier)

    def fire_blast(self):
        min_dmg = 431
        max_dmg = 510
        casting_time = 0
        crit_modifier = 4 if self.tal.incinerate else 0

        yield from self._fire_spell(name='fireblast', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time,
                                    crit_modifier=crit_modifier, cooldown=1.5)

    def pyroblast(self, casting_time=6):
        min_dmg = 716
        max_dmg = 890

        yield from self._fire_spell(name='pyroblast', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time)

    def frostbolt(self):
        min_dmg = 440
        max_dmg = 475
        casting_time = 2.5

        yield from self._frost_spell(name='frostbolt', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time)
