import random

import simpy


class Environment(simpy.Environment):
    def __init__(self,
                 print=True,
                 print_dots=False,
                 permanent_coe=True,
                 permanent_cos=True,
                 permanent_nightfall=False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        from sim.debuffs import Debuffs
        from sim.utils import DamageMeter

        self.characters = []
        self.print = print
        self.print_dots = print_dots
        self.debuffs = Debuffs(self, permanent_coe=permanent_coe, permanent_cos=permanent_cos,
                               permanent_nightfall=permanent_nightfall)
        self.meter = DamageMeter(self)
        self.process(self.debuffs.run())

        from sim.ignite import Ignite
        self.ignite = Ignite(self)

        from sim.improved_shadow_bolt import ImprovedShadowBolt
        self.improved_shadow_bolt = ImprovedShadowBolt(self)

        self.total_spell_dmg = 0
        self.total_dot_dmg = 0
        self.total_ignite_dmg = 0
        self.GCD = 1.5

    def get_total_dmg(self):
        return self.total_spell_dmg + self.total_dot_dmg + self.total_ignite_dmg

    def time(self):
        dt = str(round(self.now, 1))
        return '[' + str(dt) + ']'

    def p(self, msg):
        if self.print:
            print(msg)

    def add_character(self, character):
        self.characters.append(character)
        character.attach_env(self)

    def add_characters(self, characters):
        for char in characters:
            self.add_character(char)

    def run(self, *args, **kwargs):
        random.shuffle(self.characters)
        for char in self.characters:
            self.process(char.rotation(char))
        super().run(*args, **kwargs)
