import random

import simpy

from classicmagedps.utils import DamageMeter


class FrostEnvironment(simpy.Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mages = []
        self.PRINT = True
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


class FireballDot:
    def __init__(self, owner):
        self.owner = owner
        self.timer = 8

    def tick_dmg(self):
        dmg = 19
        dmg *= 1 + self.owner.env.debuffs.scorch_stacks * 0.03
        return round(dmg)


class PyroblastDot:
    def __init__(self, owner, sp):
        self.owner = owner
        self.sp = sp
        self.timer = 12

    def tick_dmg(self):
        dmg = 15 + self.sp * 0.15  # what it seems to be on turtle
        dmg *= 1 + self.owner.env.debuffs.scorch_stacks * 0.03
        return round(dmg)


class Debuffs:
    def __init__(self, env, coe=True):
        self.env = env
        self.scorch_stacks = 0
        self.scorch_timer = 0
        self.coe = coe
        self.wc_stacks = 0
        self.wc_timer = 0

        self.fireball_dots = []
        self.pyroblast_dots = []

    def scorch(self):
        self.scorch_stacks = min(self.scorch_stacks + 1, 5)
        self.scorch_timer = 30

    def winters_chill(self):
        self.wc_stacks = min(self.wc_stacks + 1, 5)
        self.wc_timer = 30

    def fireball_dot(self, owner):
        # check if dot already exists
        for dot in self.fireball_dots:
            if dot.owner == owner:
                dot.timer = 8
                return

        self.fireball_dots.append(FireballDot(owner))

    def pyroblast_dot(self, owner, sp):
        # check if dot already exists
        for dot in self.pyroblast_dots:
            if dot.owner == owner:
                dot.timer = 12
                dot.sp = sp
                return

        self.pyroblast_dots.append(PyroblastDot(owner, sp))

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.scorch_timer = max(self.scorch_timer - 1, 0)
            if not self.scorch_timer:
                self.scorch_stacks = 0
            self.wc_timer = max(self.wc_stacks - 1, 0)
            if not self.wc_timer:
                self.wc_stacks = 0

            # check for fireball dots
            for dot in self.fireball_dots:
                dot.timer -= 1
                if dot.timer % 2 == 0:
                    # self.env.p(
                    #     f"{self.env.time()} - ({dot.owner.name}) fireball tick {dot.tick_dmg()} time remaining {dot.timer}")
                    self.env.meter.register(dot.owner, dot.tick_dmg())
                if dot.timer <= 0:
                    self.fireball_dots.remove(dot)

            # check for pyroblast dots
            for dot in self.pyroblast_dots:
                dot.timer -= 1
                if dot.timer % 3 == 0:
                    self.env.p(
                        f"{self.env.time()} - ({dot.owner.name}) pyroblast tick {dot.tick_dmg()} time remaining {dot.timer}")
                    self.env.meter.register(dot.owner, dot.tick_dmg())
                if dot.timer <= 0:
                    self.pyroblast_dots.remove(dot)


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
        self._3_stack_uptime = 0
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
            self.env.process(self._tick(self.ignite_id))

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
        self.ignite_id += 1 # increment ignite id

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
                if self.stacks >= 3:
                    self._3_stack_uptime += 0.05
                if self.stacks == 5:
                    self._5_stack_uptime += 0.05

            yield self.env.timeout(0.05)

    def _tick(self, ignite_id):
        while self.ignite_id == ignite_id:
            yield self.env.timeout(2)
            if self.ticks_left > 0:
                self._do_dmg()
                self.ticks_left -= 1

    def _do_dmg(self):
        tick_dmg = self.cum_dmg * 0.2

        if self.env.debuffs.coe:
            tick_dmg *= 1.1  # ignite double dips on CoE

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
        self.env.p(f"{self.env.time()} num_ticks {len(self.ticks)} total ignite dmg {self.env.total_ignite_dmg}")

    @property
    def uptime(self):
        return self._uptime / self.env.now

    @property
    def uptime_gte_3_stacks(self):
        return self._3_stack_uptime / self.env.now

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
