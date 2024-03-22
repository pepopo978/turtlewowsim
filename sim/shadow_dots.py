import random

from sim.dot import Dot
from sim.warlock import Spell, Warlock


class ShadowDot(Dot):
    def _do_dmg(self):
        tick_dmg = self._get_effective_tick_dmg()
        tick_dmg *= self.dmg_multiplier

        if self.env.debuffs.has_cos:
            tick_dmg *= 1.1

        if self.env.debuffs.has_nightfall:
            tick_dmg *= 1.15

        tick_dmg *= self.owner.dmg_modifier

        isb_msg = "(ISB)" if self.env.improved_shadow_bolt.is_active else ""
        tick_dmg = int(self.env.improved_shadow_bolt.apply_to_dot(self.owner, tick_dmg))

        if self.env.print_dots:
            self.env.p(
                f"{self.env.time()} - ({self.owner.name}) {isb_msg} {self.name} dot tick {tick_dmg} ticks remaining {self.ticks_left}")
        self.env.total_dot_dmg += tick_dmg
        self.env.meter.register(self.owner.name, tick_dmg)


class CorruptionDot(ShadowDot):
    def __init__(self, owner, env):
        super().__init__(owner, env)

        self.coefficient = 0.1666
        self.time_between_ticks = 3
        self.ticks_left = 6
        self.starting_ticks = 6
        self.base_tick_dmg = 137
        self.name = Spell.CORRUPTION.value

        if isinstance(owner, Warlock):
            if owner.tal.demonic_sacrifice:
                self.dmg_multiplier += 0.15

            if owner.tal.shadow_mastery:
                self.dmg_multiplier += 0.1

    def _do_dmg(self):
        super()._do_dmg()

        if isinstance(self.owner, Warlock):
            if self.owner.tal.nightfall > 0:
                if random.randint(1, 100) <= self.owner.tal.nightfall * 2:
                    self.owner.nightfall_proc()


class CurseOfAgonyDot(ShadowDot):
    def __init__(self, owner, env, has_shadow_mastery=True, has_demonic_sacrifice=False):
        super().__init__(owner, env)

        self.coefficient = 0.0833
        self.time_between_ticks = 2
        self.ticks_left = 12
        self.starting_ticks = 12
        self.base_tick_dmg = 87
        self.name = Spell.CURSE_OF_AGONY.value

        if has_demonic_sacrifice:
            self.dmg_multiplier += 0.15

        if has_shadow_mastery:
            self.dmg_multiplier += 0.1

    def _get_effective_tick_dmg(self):
        standard_tick_dmg = super()._get_effective_tick_dmg()

        # first four ticks each deal 1/24 of the damage each (about 4.2%),
        # the next four deal 1/12 of the damage (about 8.3%),
        # and then the last four each deal 1/8 of the damage (12.5%).
        # In other words, the first four ticks combine to 1/6 (16.6%) of the damage,
        # the next four to 1/3 (33.3%),
        # and the last four together to about one half of the total damage."
        # https://wowwiki-archive.fandom.com/wiki/Curse_of_Agony
        if self.ticks_left >= 8:
            # instead of 1/12 of the damage use 1/24 for tick 11,10,9,8
            return standard_tick_dmg * 0.5
        elif self.ticks_left >= 4:
            # 1/12 of the damage for tick 7,6,5,4
            return standard_tick_dmg
        elif self.ticks_left >= 0:
            # 1/8 of the damage for tick 3,2,1,0
            return standard_tick_dmg * 1.5
        else:
            return 0


class CurseOfShadow(ShadowDot):
    def __init__(self, owner, env):
        super().__init__(owner, env)

        self.coefficient = 0
        self.time_between_ticks = 1
        self.ticks_left = 300  # ideally use event for this instead at some point
        self.starting_ticks = 300
        self.base_tick_dmg = 0
        self.name = Spell.CURSE_OF_SHADOW.value
