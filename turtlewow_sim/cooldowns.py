from turtlewow_sim.character import Character


class Cooldown:
    DURATION = NotImplemented

    def __init__(self, character: Character):
        self.character = character
        self._used = False

        self._active = False

    @property
    def env(self):
        return self.character.env

    @property
    def usable(self):
        return not self._active and not self._used

    @property
    def used(self):
        return self._used

    def is_active(self):
        return self._active

    @property
    def name(self):
        return type(self).__name__

    def activate(self):
        self._active = True
        self.character.print(f"{self.name} activated")

    def deactivate(self):
        self._active = False
        self._used = True
        self.character.print(f"{self.name} deactivated")


class PresenceOfMind(Cooldown):
    pass


class ArcanePower(Cooldown):
    DURATION = 15
    DMG_MOD = 0.3

    @property
    def usable(self):
        return not self._active and not self.used and not self.character.cds.power_infusion.is_active()

    def activate(self):
        super().activate()
        self.character.add_dmg_modifier(self.DMG_MOD)

        def callback(self):
            yield self.character.env.timeout(self.DURATION)
            self.deactivate()

        self.character.env.process(callback(self))

    def deactivate(self):
        super().deactivate()
        self.character.remove_dmg_modifier(self.DMG_MOD)


class Combustion(Cooldown):
    def __init__(self, character: Character):
        super().__init__(character)
        self._charges = 0
        self._crit_bonus = 0

    @property
    def crit_bonus(self):
        return self._crit_bonus

    def use_charge(self):
        if self._charges:
            self._charges -= 1
            if self._charges == 0:
                self.deactivate()

    def cast_fire_spell(self):
        if self._charges:
            self._crit_bonus += 10

    def activate(self):
        super().activate()
        self._charges = 3
        self._crit_bonus = 10
        self._used = True


class MQG(Cooldown):
    DURATION = 20

    @property
    def usable(self):
        return not self._active and not self.used and not self.character.cds.toep.is_active()

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(33)

        def callback(self):
            yield self.character.env.timeout(self.DURATION)
            self.deactivate()

        self.character.env.process(callback(self))

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(33)


class Berserking(Cooldown):
    DURATION = 10

    def __init__(self, character: Character, haste: float):
        super().__init__(character)
        self.haste = haste

    @property
    def usable(self):
        return not self._active and not self.used

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(self.haste)

        def callback(self):
            yield self.character.env.timeout(self.DURATION)
            self.deactivate()

        self.character.env.process(callback(self))

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.haste)


class PowerInfusion(ArcanePower):
    DURATION = 15
    DMG_MOD = 0.2

    @property
    def usable(self):
        return not self._active and not self.used and not self.character.cds.arcane_power.is_active()


class TOEP(Cooldown):
    DURATION = 15
    DMG_BONUS = 175

    @property
    def usable(self):
        return not self._active and not self.used and not self.character.cds.mqg.is_active()

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(self.DMG_BONUS)

        def callback(self):
            yield self.character.env.timeout(self.DURATION)
            self.deactivate()

        self.character.env.process(callback(self))

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


class Cooldowns:
    def __init__(self, character):
        self.combustion = Combustion(character)
        self.arcane_power = ArcanePower(character)
        self.power_infusion = PowerInfusion(character)
        self.presence_of_mind = PresenceOfMind(character)
        self.toep = TOEP(character)
        self.mqg = MQG(character)
        self.berserking30 = Berserking(character, 30)
        self.berserking20 = Berserking(character, 20)
        self.berserking10 = Berserking(character, 10)
