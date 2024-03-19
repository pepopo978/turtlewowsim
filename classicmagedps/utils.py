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
        self.mages = {}

    def register(self, mage, dmg):
        if not mage in self.mages:
            self.mages[mage] = 0
        self.mages[mage] += dmg

    def raid_dmg(self):
        total_raid_dmg = sum(self.mages.values())
        total_time = self.env.now
        return round(total_raid_dmg / total_time / len(self.mages.keys()), 1)

    def report(self):
        total_time = self.env.now
        for name, dps in self.dps().items():
            print(f"{name.ljust(30, ' ')}: {dps} dps")

        total_raid_dmg = sum(self.mages.values())
        print(f"{'Average mage DPS'.ljust(30, ' ')}: {round(total_raid_dmg / total_time / len(self.mages.keys()), 1)}")
        if hasattr(self.env, 'ignite'):
            self.env.ignite.report()

    def dps(self):
        total_time = self.env.now
        dps = {}
        for mage, dmg in self.mages.items():
            dps[mage.name] = round(dmg / total_time, 1)
        return dps
