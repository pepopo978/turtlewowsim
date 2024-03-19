import random
from functools import partial

from classicmagedps.cooldowns import Combustion, ArcanePower, PowerInfusion, TOEP, MQG, PresenceOfMind, Bezerking30, \
    Bezerking15

SPELL_COEFFICIENTS = {
    'fireball': 1.0,
    'pyroblast': 1.0,
    'scorch': 0.4285,
    'fireblast': 0.4285,
    'frostbolt': 0.814,
}

class Mage:
    def __init__(self,
                 name,
                 sp,
                 crit,
                 hit,
                 fire_blast_cooldown=8,
                 env=None,
                 firepower=True,
                 dmf=False,
                 imp_scorch=True,
                 incinerate=False,
                 winters_chill=False,
                 arcane_instability=False,
                 piercing_ice=True,
                 pyro_on_t2_proc=True,
                 fullt2=False,
                 lag=0.1,
                 haste=0,
                 drop_scorch_ignites=False,
                 extend_ignite_with_scorch=False,
                 ):
        self.env = env
        self.name = name
        self.sp = sp
        self.crit = crit
        self.hit = hit
        self.firepower = firepower
        self.dmf = dmf
        self.imp_scorch = imp_scorch
        self.incineration = incinerate
        self.fire_blast_cooldown = fire_blast_cooldown
        self.dmg_modifier = 1
        self.trinket_haste = 0
        self.haste = haste
        self.winters_chill = winters_chill
        self.arcane_instability = arcane_instability
        self.piercing_ice = piercing_ice
        self.fullt2 = fullt2
        self._t2proc = -1
        self.sp_bonus = 0
        self.combustion = Combustion(self)
        self.arcane_power = ArcanePower(self)
        self.power_infusion = PowerInfusion(self)
        self.presence_of_mind = PresenceOfMind(self)
        self.toep = TOEP(self)
        self.mqg = MQG(self)
        self.bezerking30 = Bezerking30(self)
        self.bezerking15 = Bezerking15(self)
        self.pyro_on_t2_proc = pyro_on_t2_proc
        self.fire_blast_remaining_cd = 0
        self.lag = lag
        self.drop_scorch_ignites = drop_scorch_ignites
        self.extend_ignite_with_scorch = extend_ignite_with_scorch

        self.num_casts = {}

        if self.env:
            self.env.mages.append(self)

    def _set_rotation(self, name, *args, **kwargs):
        def callback(mage):
            rotation = getattr(mage, '_' + name)
            return rotation(*args, **kwargs)

        self.rotation = callback

    def spam_fireballs(self, *args, **kwargs):
        # set rotation to internal _spam_fireballs and use partial to pass args and kwargs to that function
        return partial(self._set_rotation, name="spam_fireballs")(*args, **kwargs)

    def spam_pyroblast(self, *args, **kwargs):
        return partial(self._set_rotation, name="spam_pyroblast")(*args, **kwargs)

    def spam_scorch(self, *args, **kwargs):
        return partial(self._set_rotation, name="spam_scorch")(*args, **kwargs)

    def spam_scorch_unless_mqg(self, *args, **kwargs):
        return partial(self._set_rotation, name="spam_scorch_unless_mqg")(*args, **kwargs)

    def smart_scorch(self, *args, **kwargs):
        return partial(self._set_rotation, name="smart_scorch")(*args, **kwargs)

    def smart_scorch_and_fireblast(self, *args, **kwargs):
        return partial(self._set_rotation, name="smart_scorch_and_fireblast")(*args, **kwargs)

    def one_scorch_then_fireballs(self, *args, **kwargs):
        return partial(self._set_rotation, name="one_scorch_then_fireballs")(*args, **kwargs)

    def one_scorch_one_pyro_then_fb(self, *args, **kwargs):
        return partial(self._set_rotation, name="one_scorch_one_pyro_then_fb")(*args, **kwargs)

    def one_scorch_one_frostbolt_then_fb(self, *args, **kwargs):
        return partial(self._set_rotation, name="one_scorch_one_frostbolt_then_fb")(*args, **kwargs)

    def spam_frostbolts(self, *args, **kwargs):
        return partial(self._set_rotation, name="spam_frostbolts")(*args, **kwargs)

    def _random_delay(self, secs=2):
        if secs:
            delay = round(random.random() * secs, 2)
            yield self.env.timeout(delay)

    def _use_cds(self, **kwargs):
        for name, time in kwargs.items():
            cd = getattr(self, name)
            if cd.usable and self.env.now >= time:
                cd.activate()

    def _spam_fireballs(self, delay=2, **cds):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            yield from self.fireball()

    def _spam_pyroblast(self, delay=2, **cds):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            yield from self.pyroblast()

    def _spam_frostbolts(self, delay=2, **cds):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            yield from self.frostbolt()

    def _spam_scorch(self, delay=2, **cds):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            yield from self.scorch()

    def _spam_scorch_unless_mqg(self, delay=2, **cds):
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            if self.mqg.active:
                yield from self.fireball()
            else:
                yield from self.scorch()

    def _one_scorch_then_fireballs(self, delay=2, **cds):
        """1 scorch then 9 fireballs rotation"""
        yield from self._random_delay(delay)

        while True:
            self._use_cds(**cds)
            yield from self.scorch()
            for _ in range(9):
                self._use_cds(**cds)
                yield from self.fireball()

    def _smart_scorch(self, delay=2, **cds):
        """Cast scorch if less than 5 imp scorch stacks or if 5 stack ignite and extend_ignite_with_scorch else cast fireball"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(**cds)
            if self.env.ignite.stacks == 5 and self.env.ignite.is_suboptimal() and self.drop_scorch_ignites:
                # let ignite drop
                yield from self.pyroblast()
            elif self.env.debuffs.scorch_stacks < 5 or (self.env.ignite.stacks == 5 and self.extend_ignite_with_scorch):
                yield from self.scorch()
            else:
                # check if scorch about to fall off
                if self.env.debuffs.scorch_timer <= 4.5:
                    yield from self.scorch()
                else:
                    yield from self.fireball()

    def _smart_scorch_and_fireblast(self, delay=2, **cds):
        """Same as above except fireblast on cd"""
        yield from self._random_delay(delay)
        while True:
            self._use_cds(**cds)
            if (self.env.debuffs.scorch_stacks == 5 and
                    self.fire_blast_remaining_cd <= 0 and
                    self.env.ignite.stacks == 5 and self.env.ignite.ticks_left <= 1):
                yield from self.fire_blast()
                self.fire_blast_remaining_cd = self.fire_blast_cooldown - 1.5
                # fire blast cd - gcd
            elif self.env.debuffs.scorch_stacks < 5 or \
                    (self.env.ignite.stacks == 5 and self.extend_ignite_with_scorch):
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

    def _one_scorch_one_pyro_then_fb(self, delay=1, **cds):
        yield from self._random_delay(delay)

        self._use_cds(**cds)
        yield from self.scorch()
        self._use_cds(**cds)
        yield from self.pyroblast()
        for _ in range(7):
            self._use_cds(**cds)
            yield from self.fireball()

        yield from self._one_scorch_then_fireballs(delay=0, **cds)

    def _one_scorch_one_frostbolt_then_fb(self, delay=1, **cds):
        yield from self._random_delay(delay)

        self._use_cds(**cds)
        yield from self.scorch()
        self._use_cds(**cds)
        yield from self.frostbolt()
        for _ in range(8):
            self._use_cds(**cds)
            yield from self.fireball()

        yield from self._one_scorch_then_fireballs(delay=0, **cds)

    def print(self, msg):
        if self.env.print:
            self.env.p(f"{self.env.time()} - ({self.name}) {msg}")

    def get_cast_time(self, base_cast_time):
        # check for pom
        if self.presence_of_mind.active:
            self.presence_of_mind.deactivate()
            return 0

        trinket_haste = 1 + self.trinket_haste / 100
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

        if self.pyro_on_t2_proc and self._t2proc >= 0:
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

        crit_chance = self.crit + crit_modifier + self.combustion.crit_bonus
        if self.arcane_instability:
            crit_chance += 3

        crit = random.randint(1, 100) <= crit_chance

        coeff = SPELL_COEFFICIENTS[name]

        dmg = random.randint(min_dmg, max_dmg)
        dmg += (self.sp + self.sp_bonus) * coeff

        if self.firepower:
            dmg *= 1.1  # Fire Power
        if self.arcane_instability:
            dmg *= 1.03
        if self.env.debuffs.coe:
            dmg *= 1.1  # CoE
        if self.env.debuffs.nightfall:
            dmg *= 1.15
        if self.dmf:
            dmg *= 1.1

        dmg *= 1 + self.env.debuffs.scorch_stacks * 0.03  # imp. scorch

        dmg = int(dmg * self.dmg_modifier)
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
            if self.combustion.active:
                self.combustion.crit_bonus += 10
        elif not crit:
            self.print(f"{name} {description} {dmg}")
            if self.combustion.active:
                self.combustion.crit_bonus += 10
        else:
            dmg = int(dmg * 1.5)
            self.print(f"{name} {description} **{dmg}**")
            self.env.ignite.refresh(self, dmg, name)

            if self.combustion.active:
                self.combustion.charges -= 1
                if self.combustion.charges == 0:
                    self.combustion.crit_bonus = 0
                    self.print("Combustion ended")

        if name == 'fireball':
            self.env.debuffs.add_fireball_dot(self)

        if name == 'pyroblast':
            self.env.debuffs.add_pyroblast_dot(self)

        if name == 'scorch' and self.imp_scorch and hit:
            # roll for whether debuff hits
            fire_vuln_hit = random.randint(1, 100) <= hit_chance
            if fire_vuln_hit:
                self.env.debuffs.scorch()

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self, dmg)
        if self.fullt2 and name == 'fireball':
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
        if self.arcane_instability:
            crit_chance += 3

        crit = random.randint(1, 100) <= crit_chance

        dmg = random.randint(min_dmg, max_dmg)
        coeff = SPELL_COEFFICIENTS[name]
        dmg += (self.sp + self.sp_bonus) * coeff

        if self.piercing_ice:
            dmg *= 1.06  # Piercing Ice
        if self.arcane_instability:
            dmg *= 1.03
        if self.env.debuffs.coe:
            dmg *= 1.1  # CoE
        if self.env.debuffs.nightfall:
            dmg *= 1.15
        if self.dmf:
            dmg *= 1.1

        dmg = int(dmg * self.dmg_modifier)
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

        if self.winters_chill:
            # roll for whether debuff hits
            winters_chill_hit = random.randint(1, 100) <= hit_chance
            if winters_chill_hit:
                self.env.debuffs.winters_chill()

        self.env.total_spell_dmg += dmg
        self.env.meter.register(self, dmg)
        if self.fullt2 and name == 'frostbolt':
            if random.randint(1, 100) <= 10:
                self._t2proc = 1
                self.print("T2 proc")

        self.num_casts[name] = self.num_casts.get(name, 0) + 1

        # handle gcd
        if cooldown:
            yield self.env.timeout(cooldown + self.lag / 2)

    def scorch(self):
        min_dmg = 237
        max_dmg = 280
        casting_time = 1.5
        crit_modifier = 4 if self.incineration else 0

        yield from self._fire_spell(name='scorch', min_dmg=min_dmg, max_dmg=max_dmg, base_cast_time=casting_time,
                                    crit_modifier=crit_modifier)

    def fire_blast(self):
        min_dmg = 431
        max_dmg = 510
        casting_time = 0
        crit_modifier = 4 if self.incineration else 0

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
