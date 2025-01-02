from sim.character import Character
from sim.env import Environment
from sim.spell_school import DamageType


class Dot:
    def __init__(self, name: str, owner: Character, env: Environment, damage_type: DamageType, cast_time: float, register_casts=True):
        self.owner = owner
        self.env = env
        self.damage_type = damage_type

        self.sp = self.owner.eff_sp  # snapshot sp
        self.coefficient = 0
        self.time_between_ticks = 0
        self.starting_ticks = 0
        self.ticks_left = 0
        self.base_tick_dmg = 0
        self.name = name
        self.register_casts = register_casts

        if register_casts:
            self.env.meter.register_dot_cast(
                char_name=self.owner.name,
                spell_name=self.name,
                cast_time=cast_time)

    def _get_effective_tick_dmg(self):
        dmg = self.base_tick_dmg + self.sp * self.coefficient
        return self.owner.modify_dmg(dmg, self.damage_type, is_periodic=True)

    # This method is overridden in the child class
    def _do_dmg(self):
        tick_dmg = self._get_effective_tick_dmg()
        partial_amount = self.owner.roll_partial(is_dot=True, is_binary=False)
        partial_desc = ""
        if partial_amount < 1:
            tick_dmg = int(tick_dmg * partial_amount)
            partial_desc = f"({int(partial_amount * 100)}% partial)"

        if self.env.print_dots:
            self.env.p(
                f"{self.env.time()} - ({self.owner.name}) {self.name} dot tick {partial_desc} {tick_dmg} ticks remaining {self.ticks_left}")

        self.env.meter.register_dot_dmg(
            char_name=self.owner.name,
            spell_name=self.name,
            dmg=tick_dmg,
            aoe=False)

    def run(self):
        while self.ticks_left > 0:
            yield self.env.timeout(self.time_between_ticks)
            self.ticks_left -= 1
            self._do_dmg()

    def refresh(self, cast_time: float):
        self.ticks_left = self.starting_ticks

        if self.register_casts:
            self.env.meter.register_dot_cast(
                char_name=self.owner.name,
                spell_name=self.name,
                cast_time=cast_time)

    def is_active(self):
        return self.ticks_left > 0
