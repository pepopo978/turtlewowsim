from dataclasses import dataclass

@dataclass(kw_only=True)
class MageOptions:
    fullt2: bool = False

    # Fire
    drop_suboptimal_ignites: bool = False  # cast pyroblast if scorch/fireblast in ignite to drop ignite
    remaining_ticks_for_ignite_extend: int = 1  # min remaining ticks to extend ignite
    extend_ignite_with_fire_blast: bool = False  # extend ignite with fire blast (prio over scorch)
    extend_ignite_with_scorch: bool = False  # extend ignite with scorch
    pyro_on_t2_proc: bool = True
    pyro_on_9_hot_streak: bool = True # cast pyroblast on 9 stacks of hot streak

    # Frost
    use_frostnova_for_icicles: bool = False  # use frost nova to proc flash freeze
    keep_ice_barrier_up: bool = False  # keep ice barrier up
    start_with_ice_barrier: bool = False  # start with ice barrier without having to cast it
    starting_ice_barrier_duration: int = 55  # duration of ice barrier at start, assumes you cast 5s before pull
