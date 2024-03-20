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

    # Arcane
    arcane_instability: bool = False


@dataclass(kw_only=True)
class MageOptions:
    fullt2: bool = False

    drop_scorch_ignites: bool = False
    extend_ignite_with_scorch: bool = False
    pyro_on_t2_proc: bool = True
