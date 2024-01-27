class Cooldown:
    DURATION = NotImplemented

    def __init__(self, mage):
        self.mage = mage
        self.active = False
        self.used = False

    @property
    def usable(self):
        return not self.active and not self.used

    def activate(self):
        raise NotImplementedError


class PresenceOfMind(Cooldown):
    @property
    def usable(self):
        return not self.active and not self.used

    def activate(self):
        self.mage.print(self.__class__.__name__)
        self.active = True

    def deactivate(self):
        self.active = False
        self.used = True


class ArcanePower(Cooldown):
    DURATION = 15
    DMG_MOD = 1.3

    @property
    def usable(self):
        return not self.active and not self.used and not self.mage.power_infusion.active

    def activate(self):
        self.mage.dmg_modifier = self.DMG_MOD
        self.active = True
        self.mage.print(self.__class__.__name__)

        def callback(self):
            yield self.mage.env.timeout(self.DURATION)
            self.mage.dmg_modifier = 1
            self.active = False
            self.used = True

        self.mage.env.process(callback(self))


class Combustion(Cooldown):
    def __init__(self, mage):
        self.mage = mage
        self.charges = 0
        self.crit_bonus = 0
        self.used = False

    @property
    def active(self):
        return self.charges > 0

    def activate(self):
        self.mage.print("Combustion")
        self.charges = 3
        self.crit_bonus = 10
        self.used = True


class MQG(Cooldown):
    DURATION = 20

    @property
    def usable(self):
        return not self.active and not self.used and not self.mage.toep.active

    def activate(self):
        self.mage.trinket_haste = 33
        self.active = True
        self.mage.print("MQG")
        self.used = True

        def callback(self):
            yield self.mage.env.timeout(self.DURATION)
            self.mage.trinket_haste = 0
            self.active = False

        self.mage.env.process(callback(self))


class PowerInfusion(ArcanePower):
    DURATION = 15
    DMG_MOD = 1.2

    @property
    def usable(self):
        return not self.active and not self.used and not self.mage.arcane_power.active


class TOEP(Cooldown):
    DURATION = 15
    DMG_BONUS = 175

    @property
    def usable(self):
        return not self.active and not self.used and not self.mage.mqg.active

    def activate(self):
        self.mage.sp_bonus = 175
        self.active = True
        self.mage.print(self.__class__.__name__)
        self.used = True

        def callback(self):
            yield self.mage.env.timeout(self.DURATION)
            self.mage.sp_bonus = 0
            self.active = False

        self.mage.env.process(callback(self))
