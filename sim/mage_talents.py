from builtins import int
from dataclasses import dataclass


@dataclass(kw_only=True)
class MageTalents:
    # Fire
    ignite: int = 0
    imp_scorch: int = 0
    fire_power: int = 0
    critical_mass: int = 0
    hot_streak: int = 0
    incinerate_crit: int = 0
    fire_blast_cooldown: float = 8
    fire_blast_gcd: float = 1.5

    # Frost
    elemental_precision: int = 0 # todo implement
    piercing_ice: int = 0
    frostbite: int = 0
    ice_shards: int = 0
    shatter: int = 0
    winters_chill: int = 0
    flash_freeze: int = 0
    ice_barrier: bool = False
    frost_nova_cooldown: float = 25

    # Arcane
    arcane_focus: int = 0  # todo implement
    arcane_impact: int = 0
    arcane_rupture: bool = False
    temporal_convergence: int = 0
    arcane_instability: int = 0
    presence_of_mind: bool = False
    accelerated_arcana: bool = False
    arcane_potency: int = 0
    resonance_cascade: int = 0
    arcane_power: bool = False


FireMageTalents = MageTalents(
    ignite=5,
    imp_scorch=3,
    fire_power=5,
    critical_mass=0,  # generally counted in crit already, 2% per point
    hot_streak=3,
    incinerate_crit=4,
    fire_blast_cooldown=6.5,
    fire_blast_gcd=1
)

IcicleMageTalents = MageTalents(
    piercing_ice=3,
    frostbite=3,
    ice_shards=5,
    shatter=0,
    winters_chill=5,
    flash_freeze=2,
    ice_barrier=True,
    frost_nova_cooldown=21 # 2 points in improved frost nova
)

ArcaneMageTalents = MageTalents(
    arcane_focus=3, # not looked at currently
    arcane_impact=3,
    arcane_rupture=True,
    temporal_convergence=3,
    arcane_instability=3,
    presence_of_mind=True,
    accelerated_arcana=True,
    arcane_potency=2,
    resonance_cascade=3,
    arcane_power=True
)
