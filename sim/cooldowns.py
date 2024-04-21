from sim.character import Character


class Cooldown:
    STARTS_CD_ON_ACTIVATION = True

    def __init__(self, character: Character):
        self.character = character
        self._on_cooldown = False
        self._active = False

    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return 0

    @property
    def env(self):
        return self.character.env

    @property
    def usable(self):
        return not self._active and not self._on_cooldown

    @property
    def on_cooldown(self):
        return self._on_cooldown

    def is_active(self):
        return self._active

    @property
    def name(self):
        return type(self).__name__

    def activate(self):
        if self.usable:
            self._active = True
            self.character.print(f"{self.name} activated")

            if self.duration:
                def callback(self):
                    yield self.character.env.timeout(self.duration)
                    self.deactivate()

                self.character.env.process(callback(self))
            else:
                self.deactivate()

    def deactivate(self):
        self._active = False
        self.character.print(f"{self.name} deactivated")

        if self.cooldown:
            self._on_cooldown = True

            def callback(self):
                if self.STARTS_CD_ON_ACTIVATION:
                    yield self.env.timeout(self.cooldown - self.duration)
                else:
                    yield self.env.timeout(self.cooldown)

                self._on_cooldown = False

            self.character.env.process(callback(self))


class PresenceOfMind(Cooldown):
    STARTS_CD_ON_ACTIVATION = False

    @property
    def duration(self):
        return 9999

    @property
    def cooldown(self):
        return 180


class ArcanePower(Cooldown):
    DMG_MOD = 0.3

    @property
    def duration(self):
        return 15

    @property
    def cooldown(self):
        return 180

    @property
    def usable(self):
        return not self._active and not self.on_cooldown and not self.character.cds.power_infusion.is_active()

    def activate(self):
        super().activate()
        self.character.add_dmg_modifier(self.DMG_MOD)

    def deactivate(self):
        super().deactivate()
        self.character.remove_dmg_modifier(self.DMG_MOD)


class PowerInfusion(ArcanePower):
    DURATION = 15
    DMG_MOD = 0.2

    @property
    def duration(self):
        return 15

    @property
    def cooldown(self):
        return 180

    @property
    def usable(self):
        return not self._active and not self.on_cooldown and not self.character.cds.arcane_power.is_active()


class Combustion(Cooldown):
    STARTS_CD_ON_ACTIVATION = False

    def __init__(self, character: Character):
        super().__init__(character)
        self._charges = 0
        self._crit_bonus = 0

    @property
    def cooldown(self):
        return 180

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


class MQG(Cooldown):
    @property
    def duration(self):
        return 20

    @property
    def cooldown(self):
        return 300

    @property
    def usable(self):
        return super().usable and not self.character.cds.toep.is_active()

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(33)

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(33)


class Berserking(Cooldown):
    @property
    def duration(self):
        return 10

    @property
    def cooldown(self):
        return 180

    def __init__(self, character: Character, haste: float):
        super().__init__(character)
        self.haste = haste

    @property
    def usable(self):
        return not self._active and not self.on_cooldown

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(self.haste)

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.haste)


class TOEP(Cooldown):
    DMG_BONUS = 175

    @property
    def duration(self):
        return 15

    @property
    def cooldown(self):
        return 90

    @property
    def usable(self):
        return super().usable and not self.character.cds.mqg.is_active()

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(self.DMG_BONUS)

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
