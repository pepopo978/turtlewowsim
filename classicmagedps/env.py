import random

import simpy

from classicmagedps.debuffs import Debuffs
from classicmagedps.ignite import Ignite
from classicmagedps.utils import DamageMeter


class FrostEnvironment(simpy.Environment):

    def __init__(self, print=True, print_dots=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mages = []
        self.print = print
        self.print_dots = print_dots
        self.debuffs = Debuffs(self)
        self.meter = DamageMeter(self)
        self.process(self.debuffs.run())
        self.total_spell_dmg = 0

    def get_total_dmg(self):
        return self.total_spell_dmg

    def time(self):
        dt = str(round(self.now, 1))
        return '[' + str(dt) + ']'

    def p(self, msg):
        if self.print:
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
        self.total_dot_dmg = 0
        self.total_ignite_dmg = 0
        self.ignite = Ignite(self)
        self.process(self.ignite.monitor())

    def get_total_dmg(self):
        return self.total_spell_dmg + self.total_dot_dmg + self.total_ignite_dmg
