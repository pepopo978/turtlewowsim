from builtins import int
from dataclasses import dataclass


@dataclass(kw_only=True)
class MageTalents:
    # Fire
    ignite: bool = False
    imp_scorch: bool = False
    fire_power: bool = False
    critical_mass: bool = False
    hot_streak: bool = False
    incinerate_crit: int = 0
    fire_blast_cooldown: float = 8
    fire_blast_gcd: float = 1.5

    # Frost
    piercing_ice: int = 0
    frostbite: int = 0
    ice_shards: int = 0
    shatter: int = 0
    winters_chill: int = 0
    flash_freeze: int = 0
    ice_barrier: bool = False
    frost_nova_cooldown: float = 25

    # Arcane
    arcane_instability: bool = False


FireMageTalents = MageTalents(
    ignite=True,
    imp_scorch=True,
    fire_power=True,
    critical_mass=False,  # generally counted in crit already
    hot_streak=True,
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
