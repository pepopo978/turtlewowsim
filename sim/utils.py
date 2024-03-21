from typing import Dict

from sim.env import Environment


def _round(num):
    if num > 100:
        return round(num)
    elif num > 10:
        return round(num, 1)
    else:
        return round(num, 2)


def mean(sequence):
    if not sequence:
        return 0
    return _round(sum(sequence) / len(sequence))


def mean_percentage(sequence):
    if not sequence:
        return 0
    return _round(100 * sum(sequence) / len(sequence))


class DamageMeter:
    def __init__(self, env):
        self.env = env
        self.characters: Dict[str, int] = {}

    def register(self, name: str, dmg: int):
        if not name in self.characters:
            self.characters[name] = 0
        self.characters[name] += dmg

    def raid_dmg(self):
        total_raid_dmg = sum(self.characters.values())
        total_time = self.env.now
        return round(total_raid_dmg / total_time / len(self.characters.keys()), 1)

    def report(self):
        total_time = self.env.now
        for name, dps in self.dps().items():
            print(f"{name.ljust(30, ' ')}: {dps} dps")

        total_raid_dmg = sum(self.characters.values())
        print(
            f"{'Average DPS'.ljust(30, ' ')}: {round(total_raid_dmg / total_time / len(self.characters.keys()), 1)}")

        self.env.ignite.report()
        self.env.improved_shadow_bolt.report()

    def dps(self):
        total_time = self.env.now
        dps = {}
        for name, dmg in self.characters.items():
            dps[name] = round(dmg / total_time, 1)
        return dps
