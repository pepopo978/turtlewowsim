from dataclasses import dataclass

from turtlewow_sim.mage_options import MageTalents


@dataclass(kw_only=True)
class FireMageTalents(MageTalents):
    imp_scorch: bool = True,
    critial_mass: bool = False,  # this is usually included in character's crit chance already
    fire_power: bool = True,
    fire_blast_cooldown: float = 8,


@dataclass(kw_only=True)
class ApFrostMageTalents(MageTalents):
    arcane_instability: bool = True,
    piercing_ice: bool = True,


@dataclass(kw_only=True)
class WcFrostMageTalents(MageTalents):
    winters_chill: bool = True,
    piercing_ice: bool = True
