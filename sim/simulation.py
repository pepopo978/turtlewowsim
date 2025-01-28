from collections import defaultdict
from typing import List

import numpy as np
# histogram dependencies
import plotly.express as px
import plotly.graph_objects as go
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
                 permanent_nightfall: bool = False,
                 num_mobs: int = 1,
                 mob_level: int = 63):
        self.characters = characters or []
        self.permanent_coe = permanent_coe
        self.permanent_cos = permanent_cos
        self.permanent_nightfall = permanent_nightfall
        self.num_mobs = num_mobs
        self.mob_level = mob_level

        self.duration = 0

    def run(self, iterations, duration, print_casts=False, print_dots=False):
        self.duration = duration

        self.results = {
            'dps': defaultdict(list),
            'casts': defaultdict(list),
            'per_spell_data': defaultdict(list),
            'buff_uptime': defaultdict(list),
            'partial_resists': defaultdict(list),
            'resists': defaultdict(list),

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
            env = Environment(print_casts=print_casts,
                              print_dots=print_dots,
                              permanent_coe=self.permanent_coe,
                              permanent_cos=self.permanent_cos,
                              permanent_nightfall=self.permanent_nightfall,
                              num_mobs=self.num_mobs,
                              mob_level=self.mob_level)

            # reset each char to clear last run
            for character in self.characters:
                character.reset()

            env.add_characters(self.characters)

            env.run(until=duration)
            dps_results = env.meter.dps()
            for character, mdps in dps_results.items():
                self.results['dps'][character].append(mdps)
                self.results['casts'][character].append(env.meter.total_casts(character))

            for character in self.characters:
                char_name = character.name
                self.results['partial_resists'][char_name].append(character.num_partials)
                self.results['resists'][char_name].append(character.num_resists)

                if char_name not in self.results['per_spell_data']:
                    self.results['per_spell_data'][char_name] = env.meter.per_spell_data(char_name)
                else:
                    for spell_name, data in env.meter.per_spell_data(char_name).items():
                        if spell_name in self.results['per_spell_data'][char_name]:
                            for key, value in data.items():
                                self.results['per_spell_data'][char_name][spell_name][key] += value
                        else:
                            self.results['per_spell_data'][char_name][spell_name] = data

                if char_name not in self.results['buff_uptime']:
                    self.results['buff_uptime'][char_name] =  character.buff_uptimes
                else:
                    for buff_name, buff_uptime in character.buff_uptimes.items():
                        if buff_name in self.results['buff_uptime'][char_name]:
                            self.results['buff_uptime'][char_name][buff_name] += buff_uptime
                        else:
                            self.results['buff_uptime'][char_name][buff_name] = buff_uptime


            self.results['total_spell_dmg'][i] = env.meter.total_spell_dmg
            self.results['total_dot_dmg'][i] = env.meter.total_dot_dmg
            self.results['total_ignite_dmg'][i] = env.meter.total_ignite_dmg

            self.results['total_dmg'][i] = env.meter.get_total_dmg()
            self.results['avg_dps'][i] = env.meter.raid_dmg()
            self.results['max_single_dps'][i] = max(dps_results.values())

            ignite = env.ignite
            self.results['>=1 stack uptime'][i] = ignite.uptime_gte_1_stack
            self.results['>=2 stack uptime'][i] = ignite.uptime_gte_2_stacks
            self.results['>=3 stack uptime'][i] = ignite.uptime_gte_3_stacks
            self.results['>=4 stack uptime'][i] = ignite.uptime_gte_4_stacks
            self.results['5 stack uptime'][i] = ignite.uptime_5_stacks
            self.results['1 stack ticks'][i] = ignite.num_1_stack_ticks
            self.results['2 stack ticks'][i] = ignite.num_2_stack_ticks
            self.results['3 stack ticks'][i] = ignite.num_3_stack_ticks
            self.results['4 stack ticks'][i] = ignite.num_4_stack_ticks
            self.results['5 stack ticks'][i] = ignite.num_5_stack_ticks
            self.results['num_ticks'][i] = ignite.num_ticks
            self.results['avg_tick'][i] = ignite.avg_tick
            self.results['max_tick'][i] = ignite.max_tick
            self.results['num_drops'][i] = ignite.num_drops

            isb = env.improved_shadow_bolt
            self.results['ISB uptime'][i] = isb.uptime_percent
            self.results['Total added dot dmg'][i] = isb.total_added_dot_dmg
            self.results['Total added spell dmg'][i] = isb.total_added_spell_dmg

            if ignite.had_any_ignites:
                self.results['had_any_ignite'] = True
            if isb.had_any_isbs:
                self.results['had_any_isbs'] = True

    def _justify(self, string):
        return string.ljust(JUSTIFY, ' ')

    def report(self, verbosity=1):
        chars_to_dps = {}

        if verbosity > 1:
            messages_to_dps = {}
            # per character stats
            for char in self.results['dps']:
                mean_dps = mean(self.results['dps'][char])
                mean_casts = mean(self.results['casts'][char])
                label = f"{char} DPS Mean"
                msg = f"{self._justify(label)}: {mean_dps} in {mean_casts} casts"
                messages_to_dps[msg] = mean_dps
                chars_to_dps[char] = mean_dps

            sorted_by_dps = dict(sorted(messages_to_dps.items(), key=lambda item: item[1], reverse=True))

            chars_sorted_by_dps = dict(sorted(chars_to_dps.items(), key=lambda item: item[1], reverse=True))

            # sort dps_to_dps_messages by dps
            for msg, dps in sorted_by_dps.items():
                print(msg)

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

        if verbosity > 2:
            print(f"------ Per Spell Data ------")
            for char in chars_sorted_by_dps.keys():
                iterations = len(self.results['dps'][char])
                print(f"{char}:")
                for spell_name, data in self.results['per_spell_data'][char].items():
                    num_casts = round(data['num_casts'] / iterations, 1)
                    total_dmg = round(data['total_dmg'] / iterations)
                    percent_dmg = round(data['percent_dmg'] / iterations, 1)
                    avg_dmg = round(data['avg_dmg'] / iterations)
                    avg_cast_time = round(data['avg_cast_time'] / iterations, 2)
                    avg_dps = round(data['avg_dps'] / iterations)

                    stats = f"{num_casts} casts"
                    if total_dmg:
                        stats += f", {total_dmg} dmg ({percent_dmg}%), {avg_dmg} avg dmg"
                    if avg_cast_time:
                        stats += f", {avg_cast_time} avg cast time"
                    if avg_dps:
                        stats += f", {avg_dps} dps"

                    print(f"    {spell_name.ljust(JUSTIFY, ' ')}: {stats}")

            print(f"------ Resists ------")
            for char in self.results['partial_resists']:
                label = f"{char} Partial Resists"
                print(f"{self._justify(label)}: {mean(self.results['partial_resists'][char])}")

            for char in self.results['resists']:
                label = f"{char} Resists"
                print(f"{self._justify(label)}: {mean(self.results['resists'][char])}")

        if verbosity > 2:
            print(f"------ Buff Uptime ------")
            for char in chars_sorted_by_dps.keys():
                iterations = len(self.results['dps'][char])
                print(f"{char}:")
                for buff_name, total_uptime in self.results['buff_uptime'][char].items():
                    avg_uptime = round(total_uptime / iterations, 1)
                    avg_uptime_percent = round(100 * avg_uptime / self.duration, 1)
                    print(f"    {buff_name.ljust(JUSTIFY, ' ')}: {avg_uptime} sec ({avg_uptime_percent}%)")


        if verbosity > 3:
            print(f"------ Advanced Stats ------")
            for char in self.results['dps']:
                label = f"{char} DPS standard deviation"
                print(f"{self._justify(label)}: {round(np.std(self.results['dps'][char]), 2)}")
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

    def extended_report(self):
        self.report(verbosity=2)

    def detailed_report(self):
        self.report(verbosity=3)

    def extremely_detailed_report(self):
        self.report(verbosity=4)

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
