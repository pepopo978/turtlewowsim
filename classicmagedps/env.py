import random

import simpy

from classicmagedps.utils import DamageMeter


class FrostEnvironment(simpy.Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mages = []
        self.PRINT = True
        self.PRINT_DOTS = False
        self.debuffs = Debuffs(self)
        self.meter = DamageMeter(self)
        self.process(self.debuffs.run())

    def time(self):
        dt = str(round(self.now, 1))
        return '[' + str(dt) + ']'

    def p(self, msg):
        if self.PRINT:
            print(msg)

    def add_mage(self, mage):
        self.mages.append(mage)
        mage.env = self

    def add_mages(self, mages):
        self.mages.extend(mages)
        for mage in mages:
            mage.env = self

    def run(self, *args, **kwargs):
        random.shuffle(self.mages)
        for mage in self.mages:
            self.process(mage.rotation(mage))
        super().run(*args, **kwargs)


class FireEnvironment(FrostEnvironment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_spell_dmg = 0
        self.total_ignite_dmg = 0
        self.ignite = Ignite(self)
        self.process(self.ignite.monitor())


class FireDot:
    def __init__(self, owner, env):
        self.owner = owner
        self.env = env

        self.time_between_ticks = 0
        self.starting_ticks = 0
        self.ticks_left = 0
        self.base_tick_dmg = 0
        self.name = ""

    def refresh(self):
        self.ticks_left = self.starting_ticks

    def active(self):
        return self.ticks_left > 0

    def _do_dmg(self):
        tick_dmg = self.base_tick_dmg

        if self.env.debuffs.coe:
            tick_dmg *= 1.1

        if self.env.debuffs.nightfall:
            tick_dmg *= 1.15

        if self.owner.power_infusion.active:
            tick_dmg *= 1.2

        if self.owner.dmf:
            tick_dmg *= 1.1

        tick_dmg *= 1 + self.env.debuffs.scorch_stacks * 0.03
        tick_dmg = int(tick_dmg)
        if self.env.PRINT_DOTS:
            self.env.p(
                f"{self.env.time()} - ({self.owner.name}) {self.name} dot tick {tick_dmg} ticks remaining {self.ticks_left}")
        self.env.meter.register(self.owner, tick_dmg)

    def run(self):
        while self.ticks_left > 0:
            yield self.env.timeout(self.time_between_ticks)
            self.ticks_left -= 1
            self._do_dmg()


class FireballDot(FireDot):
    def __init__(self, owner, env):
        super().__init__(owner, env)

        self.time_between_ticks = 2
        self.ticks_left = 4
        self.starting_ticks = 4
        self.base_tick_dmg = 19
        self.name = "Fireball"


class PyroblastDot(FireDot):
    def __init__(self, owner, env, has_firepower=True):
        super().__init__(owner, env)

        self.time_between_ticks = 3
        self.ticks_left = 4
        self.starting_ticks = 4
        self.firepower_multiplier = 1.1 if has_firepower else 1
        self.base_tick_dmg = (67 + self.owner.sp * 0.15) * self.firepower_multiplier
        self.name = "Pyroblast"


class Debuffs:
    def __init__(self, env, coe=True, nightfall=False):
        self.env = env
        self.scorch_stacks = 0
        self.scorch_timer = 0
        self.coe = coe
        self.nightfall = nightfall
        self.wc_stacks = 0
        self.wc_timer = 0

        self.fireball_dots = {}  # owner -> FireballDot
        self.pyroblast_dots = {}  # owner  -> PyroblastDot

    def scorch(self):
        self.scorch_stacks = min(self.scorch_stacks + 1, 5)
        self.scorch_timer = 30

    def winters_chill(self):
        self.wc_stacks = min(self.wc_stacks + 1, 5)
        self.wc_timer = 30

    def add_fireball_dot(self, owner):
        if owner in self.fireball_dots and self.fireball_dots[owner].active():
            # refresh
            self.fireball_dots[owner].refresh()
        else:
            # create new dot
            self.fireball_dots[owner] = FireballDot(owner, self.env)
            # start dot thread
            self.env.process(self.fireball_dots[owner].run())

    def add_pyroblast_dot(self, owner):
        if owner in self.pyroblast_dots and self.pyroblast_dots[owner].active():
            # refresh
            self.pyroblast_dots[owner].refresh()
        else:
            # create new dot
            self.pyroblast_dots[owner] = PyroblastDot(owner, self.env)
            # start dot thread
            self.env.process(self.pyroblast_dots[owner].run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.scorch_timer = max(self.scorch_timer - 1, 0)
            if not self.scorch_timer:
                self.scorch_stacks = 0
            self.wc_timer = max(self.wc_stacks - 1, 0)
            if not self.wc_timer:
                self.wc_stacks = 0


class Ignite:
    def __init__(self, env):
        self.active = False
        self.env = env
        self.cum_dmg = 0
        self.last_crit_time = 0
        self.ticks_left = 0
        self.owner = None
        self.stacks = 0
        self._uptime = 0
        self._2_stack_uptime = 0
        self._3_stack_uptime = 0
        self._4_stack_uptime = 0
        self._5_stack_uptime = 0
        self.ticks = []
        self.power_infusion = False
        self.crit_this_window = False
        self.contains_scorch = False
        self.contains_fireblast = False
        self.ignite_id = 0

    def is_suboptimal(self):
        return self.contains_scorch or self.contains_fireblast

    def refresh(self, mage, dmg, spell_name):
        self.check_for_drop()
        self.last_crit_time = self.env.now

        if self.active:
            if self.stacks <= 4:
                self.cum_dmg += dmg
                self.stacks += 1
                if spell_name.lower() == 'scorch':
                    self.contains_scorch = True
                elif spell_name.lower() == 'fireblast':
                    self.contains_fireblast = True

            if self.owner.power_infusion.active:
                self.power_infusion = True

            self.ticks_left = 2
        else:  # new ignite
            self.active = True
            self.cum_dmg = dmg
            self.stacks = 1
            self.owner = mage
            self.ticks_left = 2

            # start tick thread
            self.env.process(self.run(self.ignite_id))

    def drop(self):
        self.owner.print(f"Ignite dropped")
        self.active = False
        self.owner = None
        self.cum_dmg = 0
        self.stacks = 0
        self.power_infusion = False
        self.ticks_left = 0
        self.last_crit_time = 0
        self.contains_scorch = False
        self.contains_fireblast = False
        self.ignite_id += 1  # increment ignite id

    def check_for_drop(self):
        # only check last crit time if ignite is active and down to 0 ticks
        if self.active and self.ticks_left == 0:
            # check if 4 seconds have passed since last crit
            if self.env.now - self.last_crit_time > 4:
                self.drop()

    def monitor(self):
        while True:
            # check if ignite dropped in last 0.05 sec
            self.check_for_drop()

            if self.active:
                self._uptime += 0.05
                if self.stacks >= 2:
                    self._2_stack_uptime += 0.05
                if self.stacks >= 3:
                    self._3_stack_uptime += 0.05
                if self.stacks >= 4:
                    self._4_stack_uptime += 0.05
                if self.stacks == 5:
                    self._5_stack_uptime += 0.05

            yield self.env.timeout(0.05)

    def run(self, ignite_id):
        while self.ignite_id == ignite_id:
            yield self.env.timeout(2)
            if self.ticks_left > 0:
                self.ticks_left -= 1
                self._do_dmg()

    def _do_dmg(self):
        tick_dmg = self.cum_dmg * 0.2

        if self.env.debuffs.coe:
            tick_dmg *= 1.1  # ignite double dips on CoE

        if self.env.debuffs.nightfall:
            tick_dmg *= 1.15

        if self.power_infusion:
            tick_dmg *= 1.2

        tick_dmg *= 1 + self.env.debuffs.scorch_stacks * 0.03  # ignite double dips on imp.scorch
        if self.owner.dmf:
            tick_dmg *= 1.1  # ignite double dips on DMF

        tick_dmg = int(tick_dmg)
        if self.env.PRINT:
            time_left = self.last_crit_time + 4 - self.env.now
            self.env.p(
                f"{self.env.time()} - ({self.owner.name}) ({self.stacks}) ignite tick {tick_dmg} ticks remaining {self.ticks_left} time left {round(time_left, 2)}s")
        self.env.meter.register(self.owner, tick_dmg)
        self.env.total_ignite_dmg += tick_dmg
        self.ticks.append(tick_dmg)

    @property
    def uptime(self):
        return self._uptime / self.env.now

    @property
    def uptime_gte_2_stacks(self):
        return self._2_stack_uptime / self.env.now

    @property
    def uptime_gte_3_stacks(self):
        return self._3_stack_uptime / self.env.now

    @property
    def uptime_gte_4_stacks(self):
        return self._4_stack_uptime / self.env.now

    @property
    def uptime_5_stacks(self):
        return self._5_stack_uptime / self.env.now

    @property
    def avg_tick(self):
        if not self.ticks:
            return 0
        return sum(self.ticks) / len(self.ticks)

    @property
    def max_tick(self):
        return max(self.ticks)

    @property
    def num_ticks(self):
        return len(self.ticks)

    def report(self):
        print(f"Ignite uptime: {round(self.uptime * 100, 2)}%")
        print(f">=3 stack ignite uptime: {round(self.uptime_gte_3_stacks * 100, 2)}%")
        print(f"5 stack ignite uptime: {round(self.uptime_5_stacks * 100, 2)}%")
        print(f"Num Ticks: {len(self.ticks)}")
        print(f"Average tick: {round(self.avg_tick, 2)}")
        print(f"Max Tick: {max(self.ticks)}")
