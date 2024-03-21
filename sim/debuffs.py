from sim.fire_dots import PyroblastDot, FireballDot, ImmolateDot
from sim.shadow_dots import CorruptionDot, CurseOfAgonyDot


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

    def scorch(self):
        self.scorch_stacks = min(self.scorch_stacks + 1, 5)
        self.scorch_timer = 30

    def winters_chill(self):
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
            if not self.scorch_timer:
                self.scorch_stacks = 0
            self.wc_timer = max(self.wc_stacks - 1, 0)
            if not self.wc_timer:
                self.wc_stacks = 0
