from classicmagedps.dots import FireballDot, PyroblastDot


class Debuffs:
    def __init__(self, env, coe=True, nightfall=False):
        self.env = env
        self.scorch_stacks = 0
        self.scorch_timer = 0
        self.coe = coe
        self.nightfall = nightfall
        self.wc_stacks = 0
        self.wc_timer = 0

        self.fireball_dots = {}  # owner -> FireballDot
        self.pyroblast_dots = {}  # owner  -> PyroblastDot

    def scorch(self):
        self.scorch_stacks = min(self.scorch_stacks + 1, 5)
        self.scorch_timer = 30

    def winters_chill(self):
        self.wc_stacks = min(self.wc_stacks + 1, 5)
        self.wc_timer = 30

    def add_fireball_dot(self, owner):
        if owner in self.fireball_dots and self.fireball_dots[owner].active():
            # refresh
            self.fireball_dots[owner].refresh()
        else:
            # create new dot
            self.fireball_dots[owner] = FireballDot(owner, self.env)
            # start dot thread
            self.env.process(self.fireball_dots[owner].run())

    def add_pyroblast_dot(self, owner):
        if owner in self.pyroblast_dots and self.pyroblast_dots[owner].active():
            # refresh
            self.pyroblast_dots[owner].refresh()
        else:
            # create new dot
            self.pyroblast_dots[owner] = PyroblastDot(owner, self.env)
            # start dot thread
            self.env.process(self.pyroblast_dots[owner].run())

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.scorch_timer = max(self.scorch_timer - 1, 0)
            if not self.scorch_timer:
                 self.scorch_stacks = 0
            self.wc_timer = max(self.wc_stacks - 1, 0)
            if not self.wc_timer:
                self.wc_stacks = 0
