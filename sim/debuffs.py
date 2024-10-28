from sim.character import Character
from sim.fire_dots import PyroblastDot, FireballDot, ImmolateDot
from sim.shadow_dots import CorruptionDot, CurseOfAgonyDot
from sim.spell_school import DamageType


class Debuffs:
    def __init__(self, env, permanent_coe=True, permanent_cos=True, permanent_nightfall=False):
        self.env = env
        self.scorch_stacks = 0
        self.scorch_timer = 0
        self.permanent_coe = permanent_coe
        self.permanent_cos = permanent_cos
        self.permanent_nightfall = permanent_nightfall
        self.wc_stacks = 0
        self.wc_timer = 0
        self.coe_timer = 0
        self.cos_timer = 0

        self.fireball_dots = {}  # owner -> FireballDot
        self.pyroblast_dots = {}  # owner  -> PyroblastDot
        self.corruption_dots = {}  # owner  -> CorruptionDot
        self.curse_of_agony_dots = {}  # owner  -> CurseOfAgonyDot
        self.immolate_dots = {}  # owner  -> ImmolateDot

    @property
    def has_coe(self):
        return self.permanent_coe or self.coe_timer > 0

    @property
    def has_cos(self):
        return self.permanent_cos or self.cos_timer > 0

    @property
    def has_nightfall(self):
        return self.permanent_nightfall

    def modify_dmg(self, character: Character, dmg: int, damage_type: DamageType, is_periodic: bool):
        if self.env.debuffs.has_cos and damage_type in [DamageType.SHADOW, DamageType.ARCANE]:
            dmg *= 1.1
        elif self.env.debuffs.has_coe and damage_type in [DamageType.FIRE, DamageType.FROST]:
            dmg *= 1.1

        if damage_type == DamageType.FIRE and self.scorch_stacks:
            dmg *= 1 + self.scorch_stacks * 0.03

        if self.env.debuffs.has_nightfall:
            dmg *= 1.15

        if damage_type == DamageType.SHADOW:
            if is_periodic:
                dmg = self.env.improved_shadow_bolt.apply_to_dot(warlock=character, dmg=dmg)
            else:
                dmg = self.env.improved_shadow_bolt.apply_to_spell(warlock=character, dmg=dmg)

        return dmg

    def scorch(self):
        self.scorch_stacks = min(self.scorch_stacks + 1, 5)
        self.scorch_timer = 30

    def add_winters_chill_stack(self):
        if self.wc_stacks < 5:
            self.env.p(f"{self.env.time()} - Winters Chill stack {self.wc_stacks + 1} added")

        self.wc_stacks = min(self.wc_stacks + 1, 5)
        self.wc_timer = 30

    def _add_dot(self, dot_dict, dot, owner):
        if owner in dot_dict and dot_dict[owner].is_active():
            # refresh
            dot_dict[owner].refresh()
        else:
            # create new dot
            dot_dict[owner] = dot(owner, self.env)
            # start dot thread
            self.env.process(dot_dict[owner].run())

    def add_fireball_dot(self, owner):
        self._add_dot(self.fireball_dots, FireballDot, owner)

    def add_pyroblast_dot(self, owner):
        self._add_dot(self.pyroblast_dots, PyroblastDot, owner)

    def is_immolate_active(self, owner):
        return owner in self.immolate_dots and self.immolate_dots[owner].is_active()

    def add_immolate_dot(self, owner):
        self._add_dot(self.immolate_dots, ImmolateDot, owner)

    def is_corruption_active(self, owner):
        return owner in self.corruption_dots and self.corruption_dots[owner].is_active()

    def add_corruption_dot(self, owner):
        self._add_dot(self.corruption_dots, CorruptionDot, owner)

    def is_curse_of_agony_active(self, owner):
        return owner in self.curse_of_agony_dots and self.curse_of_agony_dots[owner].is_active()

    def add_curse_of_agony_dot(self, owner):
        self._add_dot(self.curse_of_agony_dots, CurseOfAgonyDot, owner)

    def is_curse_of_shadows_active(self):
        return self.cos_timer > 0

    def add_curse_of_shadows_dot(self):
        self.cos_timer = 300

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.scorch_timer = max(self.scorch_timer - 1, 0)
            if self.scorch_timer <= 0:
                self.scorch_stacks = 0
            self.wc_timer = max(self.wc_timer - 1, 0)
            if self.wc_timer <= 0:
                self.wc_stacks = 0
