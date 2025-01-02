from typing import Dict

from sim import JUSTIFY


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
    def __init__(self, env, num_mobs):
        self.env = env
        self.num_mobs = num_mobs
        self.characters: Dict[str, int] = {}

        self.total_spell_dmg = 0
        self.total_dot_dmg = 0
        self.total_ignite_dmg = 0
        self.total_proc_dmg = 0

    def register_spell_dmg(self, name: str, dmg: int, aoe=False):
        if not name in self.characters:
            self.characters[name] = 0
        if aoe:
            dmg *= self.num_mobs
        self.characters[name] += dmg
        self.total_spell_dmg += dmg

    def register_proc_dmg(self, name: str, dmg: int, aoe=False):
        if not name in self.characters:
            self.characters[name] = 0
        if aoe:
            dmg *= self.num_mobs
        self.characters[name] += dmg
        self.total_proc_dmg += dmg

    def register_dot_dmg(self, name: str, dmg: int, aoe=False):
        if not name in self.characters:
            self.characters[name] = 0
        if aoe:
            dmg *= self.num_mobs
        self.characters[name] += dmg
        self.total_dot_dmg += dmg

    def register_ignite_dmg(self, name: str, dmg: int, aoe=False):
        if not name in self.characters:
            self.characters[name] = 0
        if aoe:
            dmg *= self.num_mobs
        self.characters[name] += dmg
        self.total_ignite_dmg += dmg

    def get_total_dmg(self):
        return self.total_spell_dmg + self.total_dot_dmg + self.total_ignite_dmg

    def raid_dmg(self):
        total_raid_dmg = sum(self.characters.values())
        total_time = self.env.now
        return round(total_raid_dmg / total_time / len(self.characters.keys()), 1)

    def report(self):
        total_time = self.env.now
        casts = {}
        for character in self.env.characters:
            casts[character.name] = sum(character.num_casts.values())

        for name, dps in self.dps().items():
            print(f"{name.ljust(JUSTIFY, ' ')}: {dps} dps in {casts[name]} casts")

        total_raid_dmg = sum(self.characters.values())
        print(
            f"{'Average DPS'.ljust(JUSTIFY, ' ')}: {round(total_raid_dmg / total_time / len(self.characters.keys()), 1)}")

        self.env.ignite.report()
        self.env.improved_shadow_bolt.report()

    def dps(self):
        total_time = self.env.now
        dps = {}
        for name, dmg in self.characters.items():
            dps[name] = round(dmg / total_time, 1)
        return dps
