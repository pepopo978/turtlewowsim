from collections import defaultdict

from tqdm import trange

from turtlewow_sim.env import Environment
from turtlewow_sim.utils import mean, mean_percentage


class Simulation:

    def __init__(self, env=Environment, mages=None, coe=True, nightfall=False):
        self.env_class = env
        self.mages = mages or []
        self.coe = coe
        self.nightfall = nightfall

    def run(self, iterations, duration):
        self.results = {
            'dps': defaultdict(list),
            'casts': defaultdict(list),

            'total_spell_dmg': [None] * iterations,
            'total_dot_dmg': [None] * iterations,
            'total_ignite_dmg': [None] * iterations,
            'total_dmg': [None] * iterations,
            'avg_mage_dps': [None] * iterations,
            'max_single_dps': [None] * iterations,
            '>=1 stack uptime': [None] * iterations,
            '>=2 stack uptime': [None] * iterations,
            '>=3 stack uptime': [None] * iterations,
            '>=4 stack uptime': [None] * iterations,
            '5 stack uptime': [None] * iterations,
            '1 stack ticks': [None] * iterations,
            '2 stack ticks': [None] * iterations,
            '3 stack ticks': [None] * iterations,
            '4 stack ticks': [None] * iterations,
            '5 stack ticks': [None] * iterations,
            'avg_tick': [None] * iterations,
            'num_ticks': [None] * iterations,
            'max_tick': [None] * iterations,
        }

        for i in trange(iterations):
            env = self.env_class()
            env.debuffs.coe = self.coe
            env.debuffs.nightfall = self.nightfall
            env.print = False
            env.print_dots = False
            # reset each mage to clear last run
            for mage in self.mages:
                mage.reset()

            env.add_characters(self.mages)

            env.run(until=duration)
            for mage, mdps in env.meter.dps().items():
                self.results['dps'][mage].append(mdps)

            for mage in self.mages:
                # add up all values in the num_casts dict
                self.results['casts'][mage.name].append(sum(mage.num_casts.values()))

            self.results['total_spell_dmg'][i] = env.total_spell_dmg
            if isinstance(env, Environment):
                self.results['total_dot_dmg'][i] = env.total_dot_dmg
                self.results['total_ignite_dmg'][i] = env.total_ignite_dmg
            self.results['total_dmg'][i] = env.get_total_dmg()
            self.results['avg_mage_dps'][i] = env.meter.raid_dmg()
            self.results['max_single_dps'][i] = max(env.meter.dps().values())
            self.results['>=1 stack uptime'][i] = env.ignite.uptime_gte_1_stack
            self.results['>=2 stack uptime'][i] = env.ignite.uptime_gte_2_stacks
            self.results['>=3 stack uptime'][i] = env.ignite.uptime_gte_3_stacks
            self.results['>=4 stack uptime'][i] = env.ignite.uptime_gte_4_stacks
            self.results['5 stack uptime'][i] = env.ignite.uptime_5_stacks
            self.results['1 stack ticks'][i] = env.ignite.num_1_stack_ticks
            self.results['2 stack ticks'][i] = env.ignite.num_2_stack_ticks
            self.results['3 stack ticks'][i] = env.ignite.num_3_stack_ticks
            self.results['4 stack ticks'][i] = env.ignite.num_4_stack_ticks
            self.results['5 stack ticks'][i] = env.ignite.num_5_stack_ticks
            self.results['num_ticks'][i] = env.ignite.num_ticks
            self.results['avg_tick'][i] = env.ignite.avg_tick
            self.results['max_tick'][i] = env.ignite.max_tick

    def _justify(self, string):
        return string.ljust(40, ' ')

    def report(self):
        print(f"{self._justify('Total spell dmg')}: {mean(self.results['total_spell_dmg'])}")
        print(f"{self._justify('Total dot dmg')}: {mean(self.results['total_dot_dmg'])}")
        print(f"{self._justify('Total Ignite dmg')}: {mean(self.results['total_ignite_dmg'])}")
        print(f"{self._justify('Total dmg')}: {mean(self.results['total_dmg'])}")
        print(f"{self._justify('Average mage dps')}: {mean(self.results['avg_mage_dps'])}")
        print(f"{self._justify('Average >=1 stack ignite uptime')}: {mean_percentage(self.results['>=1 stack uptime'])}%")
        print(f"{self._justify('Average >=3 stack ignite uptime')}: {mean_percentage(self.results['>=3 stack uptime'])}%")
        print(f"{self._justify('Average   5 stack ignite uptime')}: {mean_percentage(self.results['5 stack uptime'])}%")
        print(f"{self._justify('Average ignite tick')}: {mean(self.results['avg_tick'])}")

    def detailed_report(self):
        for mage in self.results['dps']:
            label = f"{mage} average DPS"
            print(f"{self._justify(label)}: {mean(self.results['dps'][mage])} in {mean(self.results['casts'][mage])} casts")

        print(f"{self._justify('Total spell dmg')}: {mean(self.results['total_spell_dmg'])}")
        print(f"{self._justify('Total dot dmg')}: {mean(self.results['total_dot_dmg'])}")
        print(f"{self._justify('Total Ignite dmg')}: {mean(self.results['total_ignite_dmg'])}")
        print(f"{self._justify('Total dmg')}: {mean(self.results['total_dmg'])}")

        print(f"{self._justify('Average mage dps')}: {mean(self.results['avg_mage_dps'])}")
        print(f"{self._justify('Highest single mage dps')}: {max(self.results['max_single_dps'])}")
        print(f"{self._justify('Average >=1 stack ignite uptime')}: {mean_percentage(self.results['>=1 stack uptime'])}%")
        print(f"{self._justify('Average >=2 stack ignite uptime')}: {mean_percentage(self.results['>=2 stack uptime'])}%")
        print(f"{self._justify('Average >=3 stack ignite uptime')}: {mean_percentage(self.results['>=3 stack uptime'])}%")
        print(f"{self._justify('Average >=4 stack ignite uptime')}: {mean_percentage(self.results['>=4 stack uptime'])}%")
        print(f"{self._justify('Average   5 stack ignite uptime')}: {mean_percentage(self.results['5 stack uptime'])}%")
        print(f"{self._justify('Average   1 stack ticks')}: {mean(self.results['1 stack ticks'])}")
        print(f"{self._justify('Average   2 stack ticks')}: {mean(self.results['2 stack ticks'])}")
        print(f"{self._justify('Average   3 stack ticks')}: {mean(self.results['3 stack ticks'])}")
        print(f"{self._justify('Average   4 stack ticks')}: {mean(self.results['4 stack ticks'])}")
        print(f"{self._justify('Average   5 stack ticks')}: {mean(self.results['5 stack ticks'])}")
        print(f"{self._justify('Average ignite tick')}: {mean(self.results['avg_tick'])}")
        print(f"{self._justify('Average num tick')}: {mean(self.results['num_ticks'])}")
        print(f"{self._justify('Average max tick')}: {mean(self.results['max_tick'])}")
