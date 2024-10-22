from collections import defaultdict
from typing import List

from tqdm import trange

from sim import JUSTIFY
from sim.character import Character
from sim.env import Environment
from sim.utils import mean, mean_percentage

# histogram dependencies
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


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

    def run_iteration(self, i, duration):
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

        results = {
            'dps': {},
            'casts': {},
            'total_spell_dmg': env.total_spell_dmg,
            'total_dot_dmg': env.total_dot_dmg,
            'total_ignite_dmg': env.total_ignite_dmg,
            'total_dmg': env.get_total_dmg(),
            'avg_dps': env.meter.raid_dmg(),
            'max_single_dps': max(env.meter.dps().values()),
            '>=1 stack uptime': env.ignite.uptime_gte_1_stack,
            '>=2 stack uptime': env.ignite.uptime_gte_2_stacks,
            '>=3 stack uptime': env.ignite.uptime_gte_3_stacks,
            '>=4 stack uptime': env.ignite.uptime_gte_4_stacks,
            '5 stack uptime': env.ignite.uptime_5_stacks,
            '1 stack ticks': env.ignite.num_1_stack_ticks,
            '2 stack ticks': env.ignite.num_2_stack_ticks,
            '3 stack ticks': env.ignite.num_3_stack_ticks,
            '4 stack ticks': env.ignite.num_4_stack_ticks,
            '5 stack ticks': env.ignite.num_5_stack_ticks,
            'num_ticks': env.ignite.num_ticks,
            'avg_tick': env.ignite.avg_tick,
            'max_tick': env.ignite.max_tick,
            'num_drops': env.ignite.num_drops,
            'ISB uptime': env.improved_shadow_bolt.uptime_percent,
            'Total added dot dmg': env.improved_shadow_bolt.total_added_dot_dmg,
            'Total added spell dmg': env.improved_shadow_bolt.total_added_spell_dmg,
            'had_any_ignite': env.ignite.had_any_ignites,
            'had_any_isbs': env.improved_shadow_bolt.had_any_isbs,
        }

        # Collect DPS and casts data
        for character, mdps in env.meter.dps().items():
            results['dps'][character] = mdps
        for character in self.characters:
            results['casts'][character.name] = sum(character.num_casts.values())

        return i, results

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
            'num_drops': [None] * iterations,
            # isb
            'ISB uptime': [None] * iterations,
            'Total added dot dmg': [None] * iterations,
            'Total added spell dmg': [None] * iterations,
        }

        for i in trange(iterations, ascii=True):
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
            self.results['num_drops'][i] = env.ignite.num_drops

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

    def report(self, verbosity=1):
        if verbosity > 1:
            # per character stats
            for char in self.results['dps']:
                label = f"{char} DPS Mean"
                print(
                    f"{self._justify(label)}: {mean(self.results['dps'][char])} in {mean(self.results['casts'][char])} casts")

                if verbosity > 2:
                    label = f"{char} DPS standard deviation"
                    print(f"{self._justify(label)}: {np.std(self.results['dps'][char])}")
                    label = f"{char} DPS min"
                    print(f"{self._justify(label)}: {np.min(self.results['dps'][char])}")
                    label = f"{char} DPS 25th percentile"
                    print(f"{self._justify(label)}: {np.percentile(self.results['dps'][char], 25)}")
                    label = f"{char} DPS 50th percentile"
                    print(f"{self._justify(label)}: {np.percentile(self.results['dps'][char], 50)}")
                    label = f"{char} DPS 75th percentile"
                    print(f"{self._justify(label)}: {np.percentile(self.results['dps'][char], 75)}")
                    label = f"{char} DPS max"
                    print(f"{self._justify(label)}: {np.max(self.results['dps'][char])}")

                # label = f"{char} DPS Variance"
                # print(f"{self._justify(label)}: {np.var(self.results['dps'][char])}")

        print(f"{self._justify('Total spell dmg')}: {mean(self.results['total_spell_dmg'])}")
        print(f"{self._justify('Total dot dmg')}: {mean(self.results['total_dot_dmg'])}")
        if self.results['had_any_ignite']:
            print(f"{self._justify('Total ignite dmg')}: {mean(self.results['total_ignite_dmg'])}")
        print(f"{self._justify('Total dmg')}: {mean(self.results['total_dmg'])}")

        print(f"{self._justify('Average char dps')}: {mean(self.results['avg_dps'])}")
        print(f"{self._justify('Highest single char dps')}: {max(self.results['max_single_dps'])}")

        if verbosity > 1:
            if self.results['had_any_ignite']:
                # include ignite info if there was any
                print(f"------ Ignite ------")
                if verbosity > 2:
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
                if verbosity > 2:
                    print(f"{self._justify('Average   1 stack ticks')}: {mean(self.results['1 stack ticks'])}")
                    print(f"{self._justify('Average   2 stack ticks')}: {mean(self.results['2 stack ticks'])}")
                    print(f"{self._justify('Average   3 stack ticks')}: {mean(self.results['3 stack ticks'])}")
                    print(f"{self._justify('Average   4 stack ticks')}: {mean(self.results['4 stack ticks'])}")
                print(f"{self._justify('Average   5 stack ticks')}: {mean(self.results['5 stack ticks'])}")
                print(f"{self._justify('Average ignite tick')}: {mean(self.results['avg_tick'])}")
                print(f"{self._justify('Average num tick')}: {mean(self.results['num_ticks'])}")
                print(f"{self._justify('Average max tick')}: {mean(self.results['max_tick'])}")
                print(f"{self._justify('Average num drops')}: {mean(self.results['num_drops'])}")

        if verbosity > 1:
            if self.results['had_any_isbs']:
                print(f"------ ISB ------")
                print(f"{self._justify('ISB uptime')}: {mean(self.results['ISB uptime'])}%")
                print(f"{self._justify('Total added dot dmg')}: {mean(self.results['Total added dot dmg'])}")
                print(f"{self._justify('Total added spell dmg')}: {mean(self.results['Total added spell dmg'])}")

    def extended_report(self):
        self.report(verbosity=2)

    def detailed_report(self):
        self.report(verbosity=3)

    def histogram_report_individual(self):
        for char in self.results['dps']:
            fig = px.histogram(x=self.results['dps'][char], histnorm='probability density')
            fig.update_layout(title=f"DPS of {char}")
            fig.show()

    def histogram_report_overlay(self):
        fig = go.Figure()
        for char in self.results['dps']:
            fig.add_trace(go.Histogram(x=self.results['dps'][char], name=char))

        # Overlay both histograms
        fig.update_layout(title=f"DPS Distributions", barmode='overlay')
        # Reduce opacity to see both histograms
        fig.update_traces(opacity=0.50)
        fig.show()
