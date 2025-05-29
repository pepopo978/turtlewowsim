from dataclasses import dataclass
from sim.decorators import simoption

@dataclass(kw_only=True)
class MageOptions:
    fullt2: bool = simoption("Full T2 8-set bonus (10% instant cast chance on main spells)", default=False, spec=None)
    apply_undead_bonus: bool = simoption("Apply Undead Bonus (+2% damage vs undead)", default=False, spec=None)

    # Fire
    drop_suboptimal_ignites: bool = simoption("Drop suboptimal ignites (cast frostbolt to drop bad ignite)", default=False, spec="Fire")
    remaining_seconds_for_ignite_extend: int = simoption("Seconds remaining for ignite extension", default=3, spec="Fire")
    extend_ignite_with_fire_blast: bool = simoption("Extend ignite with Fire Blast", default=False, spec="Fire")
    extend_ignite_with_scorch: bool = simoption("Extend ignite with Scorch", default=False, spec="Fire")
    pyro_on_t2_proc: bool = simoption("Cast Pyroblast on T2 proc", default=True, spec="Fire")
    pyro_on_max_hot_streak: bool = simoption("Cast Pyroblast on max Hot Streak stacks", default=True, spec="Fire")

    # Frost
    frostbolt_rank: int = simoption("Frostbolt rank (11, 4, or 3)", default=11, spec="Frost")
    use_icicles_without_flash_freeze: bool = simoption("Use Icicles without Flash Freeze proc", default=False, spec="Frost")
    use_frostnova_for_icicles: bool = simoption("Use Frost Nova to proc Flash Freeze", default=False, spec="Frost")
    keep_ice_barrier_up: bool = simoption("Keep Ice Barrier up", default=False, spec="Frost")
    start_with_ice_barrier: bool = simoption("Start with Ice Barrier active", default=False, spec="Frost")
    starting_ice_barrier_duration: int = simoption("Starting Ice Barrier duration (seconds)", default=55, spec="Frost")
    use_cold_snap_for_nova: bool = simoption("Use Cold Snap to reset Frost Nova", default=False, spec="Frost")

    # Arcane
    use_presence_of_mind_on_cd: bool = simoption("Use Presence of Mind on cooldown", default=True, spec="Arcane")
    extra_second_arcane_missile: bool = simoption("Extra second on Arcane Missiles (effect on some belts)", default=False, spec="Arcane")
    interrupt_arcane_missiles: bool = simoption("Interrupt Arcane Missiles early for Rupture/Surge", default=True, spec="Arcane")
    t3_8_set: bool = simoption("T3 8-set bonus (Arcane)", default=False, spec="Arcane")
