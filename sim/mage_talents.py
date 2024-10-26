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
    winters_chill: bool = False
    piercing_ice: bool = False
    ice_shards: int = 0

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

ApFrostMageTalents = MageTalents(
    arcane_instability=True,
    piercing_ice=True,
    ice_shards=5
)

WcFrostMageTalents = MageTalents(
    winters_chill=True,
    piercing_ice=True,
    ice_shards=5
)
