from copy import deepcopy
from tqdm import trange
from collections import defaultdict
from classicmagedps.env import FireEnvironment
from classicmagedps.utils import mean


class Simulation:

    def __init__(self, env=FireEnvironment, mages=None, coe=True, nightfall=False):
        self.env_class = env
        self.mages = mages or []
        self.coe = coe
        self.nightfall = nightfall

    def run(self, iterations, duration):
        self.results = {
            'dps': defaultdict(list),

            'total_spell_dmg': [None] * iterations,
            'total_ignite_dmg': [None] * iterations,
            'avg_mage_dps': [None] * iterations,
            'max_single_dps': [None] * iterations,
            'uptime':[None] * iterations,
            '>=3 stack uptime': [None] * iterations,
            '5 stack uptime': [None] * iterations,
            'avg_tick': [None] * iterations,
            'num_ticks': [None] * iterations,
            'max_tick': [None] * iterations,
        }

        for i in trange(iterations):
            env = self.env_class()
            env.debuffs.coe = self.coe
            env.debuffs.nightfall = self.nightfall
            env.PRINT = False
            mages = [deepcopy(mage) for mage in self.mages]
            env.add_mages(mages)

            env.run(until=duration)
            for mage, mdps in env.meter.dps().items():
                self.results['dps'][mage].append(mdps)

            self.results['total_spell_dmg'][i] = env.total_spell_dmg
            self.results['total_ignite_dmg'][i] = env.total_ignite_dmg
            self.results['avg_mage_dps'][i] = env.meter.raid_dmg()
            self.results['max_single_dps'][i] = max(env.meter.dps().values())
            self.results['uptime'][i] = env.ignite.uptime
            self.results['>=3 stack uptime'][i] = env.ignite.uptime_gte_3_stacks
            self.results['5 stack uptime'][i] = env.ignite.uptime_5_stacks
            self.results['num_ticks'][i] = env.ignite.num_ticks
            self.results['avg_tick'][i] = env.ignite.avg_tick
            self.results['max_tick'][i] = env.ignite.max_tick

        self.report()

    def report(self):
        for mage in self.results['dps']:
            print(f"{mage} average DPS : {mean(self.results['dps'][mage])}")

        print(f"Total spell dmg: {mean(self.results['total_spell_dmg'])}")
        print(f"Total Ignite dmg: {mean(self.results['total_ignite_dmg'])}")

        print(f"Average mage dps: {mean(self.results['avg_mage_dps'])}")
        print(f"Highest single mage dps: {max(self.results['max_single_dps'])}")
        print(f"Average >=1 stack uptime : {100 * mean(self.results['uptime'])}%")
        print(f"Average >=3 stack ignite uptime : {100 * mean(self.results['>=3 stack uptime'])}%")
        print(f"Average 5 stack ignite uptime : {100 * mean(self.results['5 stack uptime'])}%")
        print(f"Average ignite tick : {mean(self.results['avg_tick'])}")
        print(f"Average num tick : {mean(self.results['num_ticks'])}")
        print(f"Average max tick : {mean(self.results['max_tick'])}")



