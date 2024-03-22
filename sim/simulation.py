from collections import defaultdict
from typing import List

from tqdm import trange

from sim import JUSTIFY
from sim.character import Character
from sim.env import Environment
from sim.utils import mean, mean_percentage


class Simulation:
    def __init__(self,
                 characters: List[Character] = None,
                 permanent_coe: bool = True,
                 permanent_cos: bool = True,
                 permanent_nightfall: bool = False):
        self.characters = characters or []
        self.permanent_coe = permanent_coe
        self.permanent_cos = permanent_cos
        self.permanent_nightfall = permanent_nightfall

    def run(self, iterations, duration):
        self.results = {
            'dps': defaultdict(list),
            'casts': defaultdict(list),

            'total_spell_dmg': [None] * iterations,
            'total_dot_dmg': [None] * iterations,
            'total_ignite_dmg': [None] * iterations,
            'total_dmg': [None] * iterations,
            'avg_dps': [None] * iterations,
            'max_single_dps': [None] * iterations,
            'had_any_ignite': False,
            'had_any_isbs': False,
            # ignite
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
            # isb
            'ISB uptime': [None] * iterations,
            'Total added dot dmg': [None] * iterations,
            'Total added spell dmg': [None] * iterations,
        }

        for i in trange(iterations):
            env = Environment(print=False,
                              print_dots=False,
                              permanent_coe=self.permanent_coe,
                              permanent_cos=self.permanent_cos,
                              permanent_nightfall=self.permanent_nightfall)

            # reset each char to clear last run
            for character in self.characters:
                character.reset()

            env.add_characters(self.characters)

            env.run(until=duration)
            for character, mdps in env.meter.dps().items():
                self.results['dps'][character].append(mdps)

            for character in self.characters:
                # add up all values in the num_casts dict
                self.results['casts'][character.name].append(sum(character.num_casts.values()))

            self.results['total_spell_dmg'][i] = env.total_spell_dmg
            self.results['total_dot_dmg'][i] = env.total_dot_dmg
            self.results['total_ignite_dmg'][i] = env.total_ignite_dmg

            self.results['total_dmg'][i] = env.get_total_dmg()
            self.results['avg_dps'][i] = env.meter.raid_dmg()
            self.results['max_single_dps'][i] = max(env.meter.dps().values())

            # include ignite info if there was any
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

            # include isb info if there was any
            self.results['ISB uptime'][i] = env.improved_shadow_bolt.uptime_percent
            self.results['Total added dot dmg'][i] = env.improved_shadow_bolt.total_added_dot_dmg
            self.results['Total added spell dmg'][i] = env.improved_shadow_bolt.total_added_spell_dmg

            if env.ignite.had_any_ignites:
                self.results['had_any_ignite'] = True
            if env.improved_shadow_bolt.had_any_isbs:
                self.results['had_any_isbs'] = True

    def _justify(self, string):
        return string.ljust(JUSTIFY, ' ')

    def report(self):
        print(f"{self._justify('Total spell dmg')}: {mean(self.results['total_spell_dmg'])}")
        print(f"{self._justify('Total dot dmg')}: {mean(self.results['total_dot_dmg'])}")
        print(f"{self._justify('Total ignite dmg')}: {mean(self.results['total_ignite_dmg'])}")
        print(f"{self._justify('Total dmg')}: {mean(self.results['total_dmg'])}")
        print(f"{self._justify('Average character dps')}: {mean(self.results['avg_dps'])}")

        # include ignite info if there was any
        if self.results['had_any_ignite']:
            print(f"------ Ignite ------")
            print(
                f"{self._justify('Average >=1 stack ignite uptime')}: {mean_percentage(self.results['>=1 stack uptime'])}%")
            print(
                f"{self._justify('Average >=3 stack ignite uptime')}: {mean_percentage(self.results['>=3 stack uptime'])}%")
            print(
                f"{self._justify('Average   5 stack ignite uptime')}: {mean_percentage(self.results['5 stack uptime'])}%")
            print(f"{self._justify('Average ignite tick')}: {mean(self.results['avg_tick'])}")

    def detailed_report(self):
        for char in self.results['dps']:
            label = f"{char} average DPS"
            print(
                f"{self._justify(label)}: {mean(self.results['dps'][char])} in {mean(self.results['casts'][char])} casts")

        print(f"{self._justify('Total spell dmg')}: {mean(self.results['total_spell_dmg'])}")
        print(f"{self._justify('Total dot dmg')}: {mean(self.results['total_dot_dmg'])}")
        if self.results['had_any_ignite']:
            print(f"{self._justify('Total ignite dmg')}: {mean(self.results['total_ignite_dmg'])}")
        print(f"{self._justify('Total dmg')}: {mean(self.results['total_dmg'])}")

        print(f"{self._justify('Average char dps')}: {mean(self.results['avg_dps'])}")
        print(f"{self._justify('Highest single char dps')}: {max(self.results['max_single_dps'])}")

        # include ignite info if there was any
        if self.results['had_any_ignite']:
            print(f"------ Ignite ------")
            print(
                f"{self._justify('Average >=1 stack ignite uptime')}: {mean_percentage(self.results['>=1 stack uptime'])}%")
            print(
                f"{self._justify('Average >=2 stack ignite uptime')}: {mean_percentage(self.results['>=2 stack uptime'])}%")
            print(
                f"{self._justify('Average >=3 stack ignite uptime')}: {mean_percentage(self.results['>=3 stack uptime'])}%")
            print(
                f"{self._justify('Average >=4 stack ignite uptime')}: {mean_percentage(self.results['>=4 stack uptime'])}%")
            print(
                f"{self._justify('Average   5 stack ignite uptime')}: {mean_percentage(self.results['5 stack uptime'])}%")
            print(f"{self._justify('Average   1 stack ticks')}: {mean(self.results['1 stack ticks'])}")
            print(f"{self._justify('Average   2 stack ticks')}: {mean(self.results['2 stack ticks'])}")
            print(f"{self._justify('Average   3 stack ticks')}: {mean(self.results['3 stack ticks'])}")
            print(f"{self._justify('Average   4 stack ticks')}: {mean(self.results['4 stack ticks'])}")
            print(f"{self._justify('Average   5 stack ticks')}: {mean(self.results['5 stack ticks'])}")
            print(f"{self._justify('Average ignite tick')}: {mean(self.results['avg_tick'])}")
            print(f"{self._justify('Average num tick')}: {mean(self.results['num_ticks'])}")
            print(f"{self._justify('Average max tick')}: {mean(self.results['max_tick'])}")

        if self.results['had_any_isbs']:
            print(f"------ ISB ------")
            print(f"{self._justify('ISB uptime')}: {mean(self.results['ISB uptime'])}%")
            print(f"{self._justify('Total added dot dmg')}: {mean(self.results['Total added dot dmg'])}")
            print(f"{self._justify('Total added spell dmg')}: {mean(self.results['Total added spell dmg'])}")
