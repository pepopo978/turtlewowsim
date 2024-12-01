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
    FROSTBOLTRK3 = "Frostbolt Rank 3"
    FROSTBOLTRK4 = "Frostbolt Rank 4"
    FROST_NOVA = "Frost Nova"
    CONE_OF_COLD = "Cone of Cold"
    ICICLES_CHANNEL = "Icicles Channel"
    ICICLE = "Icicle"

    # Druid
    MOONFIRE = "Moonfire"
    WRATH = "Wrath"
    STARFIRE = "Starfire"
    INSECT_SWARM = "Insect Swarm"

    # Proc Spells
    ENGULFING_SHADOWS = "ENGULFING_SHADOWS"  # Blade of Eternal Darkness
    BURNING_HATRED = "Burning Hatred"  # Ornate Bloodstone Dagger


SPELL_COEFFICIENTS = {
    # Warlock
    Spell.IMMOLATE: 0.1865,
    Spell.SEARING_PAIN: 0.4285,
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
    Spell.FROSTBOLTRK3: 0.4627,  # 2.2 / 3.5 * 0.95 * 0.775 spell lvl 14 has additional reduction
    Spell.FROSTBOLTRK4: 0.7057,  # 2.6 / 3.5 * 0.95 spell lvl 20
    Spell.FROST_NOVA: 0.1357,
    Spell.CONE_OF_COLD: 0.1357,
    Spell.ICICLE: 0.4,

    # Druid
    Spell.MOONFIRE: 0.1495,
    Spell.WRATH: 0.6214, # turtle added 5% guessing they meant a flat amount
    Spell.STARFIRE: 1.0,
    Spell.INSECT_SWARM: 0.158,

    # Proc Spells
    Spell.ENGULFING_SHADOWS: 0,  # Blade of Eternal Darkness
    Spell.BURNING_HATRED: 0.4285  # Ornate Bloodstone Dagger
}

SPELL_TRIGGERS_ON_HIT = {
    # Warlock
    Spell.IMMOLATE: True,
    Spell.SEARING_PAIN: True,
    Spell.SHADOWBOLT: True,
    Spell.CONFLAGRATE: False,
    Spell.CORRUPTION: False,
    Spell.CURSE_OF_AGONY: False,
    Spell.CURSE_OF_SHADOW: False,

    # Mage
    Spell.ARCANE_MISSILE: True,
    Spell.ARCANE_SURGE: True,
    Spell.ARCANE_RUPTURE: True,
    Spell.FIREBALL: True,
    Spell.PYROBLAST: True,
    Spell.SCORCH: True,
    Spell.FIREBLAST: True,
    Spell.FROSTBOLT: True,
    Spell.FROST_NOVA: True,
    Spell.CONE_OF_COLD: True,
    Spell.ICICLE: True,

    # Druid
    Spell.MOONFIRE: True,
    Spell.WRATH: True,
    Spell.STARFIRE: True,
    Spell.INSECT_SWARM: False,

    # Proc Spells
    Spell.ENGULFING_SHADOWS: False,  # Blade of Eternal Darkness
    Spell.BURNING_HATRED: False  # Ornate Bloodstone Dagger
}
