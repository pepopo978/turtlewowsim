from sim.character import Character
from sim.spell_school import DamageType


class Cooldown:
    STARTS_CD_ON_ACTIVATION = True
    PRINTS_ACTIVATION = True

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
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            cooldown = self.cooldown
            if self.STARTS_CD_ON_ACTIVATION and cooldown:
                self._on_cooldown = True

                def callback(self, cooldown):
                    yield self.env.timeout(cooldown)
                    if self.PRINTS_ACTIVATION:
                        self.character.print(f"{self.name} cooldown ended after {cooldown} seconds")

                    self._on_cooldown = False

                self.character.env.process(callback(self, cooldown))

            if self.duration:
                def callback(self):
                    yield self.character.env.timeout(self.duration)
                    self.deactivate()

                self.character.env.process(callback(self))
            else:
                self.deactivate()

    def deactivate(self):
        self._active = False
        if self.PRINTS_ACTIVATION:
            self.character.print(f"{self.name} deactivated")

        cooldown = self.cooldown
        if not self.STARTS_CD_ON_ACTIVATION and cooldown:
            self._on_cooldown = True

            def callback(self, cooldown):
                yield self.env.timeout(cooldown)
                if self.PRINTS_ACTIVATION:
                    self.character.print(f"{self.name} cooldown ended after {cooldown} seconds")

                self._on_cooldown = False

            self.character.env.process(callback(self, cooldown))


class PowerInfusion(Cooldown):
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

    def activate(self):
        super().activate()
        self.character.add_dmg_modifier(self.DMG_MOD)

    def deactivate(self):
        super().deactivate()
        self.character.remove_dmg_modifier(self.DMG_MOD)


class MQG(Cooldown):
    # Mind Quickening Gem
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
    # Talisman of Ephemeral Power
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


class REOS(Cooldown):
    # Restrained Essence of Sapphiron
    DMG_BONUS = 130

    @property
    def duration(self):
        return 20

    @property
    def cooldown(self):
        return 120

    @property
    def usable(self):
        return super().usable and not self.character.cds.mqg.is_active() and not self.character.cds.toep.is_active()

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(self.DMG_BONUS)

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


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


class PresenceOfMind(Cooldown):
    STARTS_CD_ON_ACTIVATION = False

    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 180
        self._apply_cd_haste = apply_cd_haste

    @property
    def cooldown(self):
        return self._base_cd / self.character.get_haste_factor_for_damage_type(
            DamageType.ARCANE) if self._apply_cd_haste else self._base_cd

    @property
    def duration(self):
        return 9999


class ArcanePower(Cooldown):
    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 180
        self._apply_cd_haste = apply_cd_haste

    @property
    def cooldown(self):
        return self._base_cd / self.character.get_haste_factor_for_damage_type(
            DamageType.ARCANE) if self._apply_cd_haste else self._base_cd

    @property
    def duration(self):
        return 20

    @property
    def usable(self):
        return not self._active and not self.on_cooldown and not self.character.cds.power_infusion.is_active()

    def activate(self):
        super().activate()
        self.character.add_cooldown_haste(35)

    def deactivate(self):
        super().deactivate()
        self.character.remove_cooldown_haste(35)


class WrathOfCenariusBuff(Cooldown):
    DMG_BONUS = 132
    PRINTS_ACTIVATION = True

    def __init__(self, character: Character):
        super().__init__(character)
        self._buff_end_time = -1

    @property
    def usable(self):
        return not self._active

    @property
    def duration(self):
        return 10

    # need special handling for when cooldown ends due to possibility of cooldown reset
    def activate(self):
        if self.usable:
            self.character.add_sp_bonus(self.DMG_BONUS)

            self._buff_end_time = self.character.env.now + self.duration

            self._active = True
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            def callback(self):
                while True:
                    remaining_time = self._buff_end_time - self.character.env.now
                    yield self.character.env.timeout(remaining_time)

                    if self.character.env.now >= self._buff_end_time:
                        self.deactivate()
                        break

            self.character.env.process(callback(self))
        else:
            # refresh buff end time
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} refreshed")
            self._buff_end_time = self.character.env.now + self.duration

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


class Cooldowns:
    def __init__(self, character):
        self.power_infusion = PowerInfusion(character)

        # mage cds
        has_accelerated_arcana = False
        if hasattr(character.tal, "accelerated_arcana"):
            has_accelerated_arcana = character.tal.accelerated_arcana

        self.combustion = Combustion(character)
        self.arcane_power = ArcanePower(character, has_accelerated_arcana)
        self.presence_of_mind = PresenceOfMind(character, has_accelerated_arcana)

        self.toep = TOEP(character)
        self.reos = REOS(character)
        self.mqg = MQG(character)
        self.berserking30 = Berserking(character, 30)
        self.berserking20 = Berserking(character, 20)
        self.berserking10 = Berserking(character, 10)
