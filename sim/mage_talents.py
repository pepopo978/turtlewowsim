from dataclasses import dataclass


@dataclass(kw_only=True)
class MageTalents:
    # Fire
    imp_scorch: bool = False
    incinerate: bool = False
    fire_power: bool = False
    critial_mass: bool = False
    fire_blast_cooldown: float = 8

    # Frost
    winters_chill: bool = False
    piercing_ice: bool = False
    ice_shards: int = 0

    # Arcane
    arcane_instability: bool = False


FireMageTalents = MageTalents(
    imp_scorch=True,
    fire_power=True,
    critial_mass=False,  # generally counted in crit already
    fire_blast_cooldown=8
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
