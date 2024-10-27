# spell name enum
from enum import Enum


class Spell(Enum):
    # Warlock
    IMMOLATE = "Immolate"
    SEARING_PAIN = "Searing Pain"
    CONFLAGRATE = "Conflagrate"
    CORRUPTION = "Corruption"
    CURSE_OF_AGONY = "Curse of Agony"
    CURSE_OF_SHADOW = "Curse of Shadow"
    SHADOWBOLT = "Shadowbolt"

    # Mage
    ARCANE_MISSILE = "Arcane Missile"
    ARCANE_MISSILES_CHANNEL = "Arcane Missiles Channel"
    ARCANE_SURGE = "Arcane Surge"
    ARCANE_RUPTURE = "Arcane Rupture"
    FIREBALL = "Fireball"
    PYROBLAST = "Pyroblast"
    SCORCH = "Scorch"
    FIREBLAST = "Fire Blast"
    FROSTBOLT = "Frostbolt"
    FROST_NOVA = "Frost Nova"
    CONE_OF_COLD = "Cone of Cold"
    ICICLES_CHANNEL = "Icicles Channel"
    ICICLE = "Icicle"


SPELL_COEFFICIENTS = {
    # Warlock
    Spell.IMMOLATE: 0.1865,
    Spell.SHADOWBOLT: 0.8571,

    # Mage
    Spell.ARCANE_MISSILE: 0.328,
    Spell.ARCANE_SURGE: 0.65,
    Spell.ARCANE_RUPTURE: 1.0,
    Spell.FIREBALL: 1.0,
    Spell.PYROBLAST: 1.0,
    Spell.SCORCH: 0.4285,
    Spell.FIREBLAST: 0.4285,
    Spell.FROSTBOLT: 0.814,
    Spell.FROST_NOVA: 0.1357,
    Spell.CONE_OF_COLD: 0.1357,
    Spell.ICICLE: 0.4,
}
