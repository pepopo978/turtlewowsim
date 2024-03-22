from dataclasses import dataclass


@dataclass(kw_only=True)
class WarlockTalents:
    # affliction
    suppression: int = 0  # 2% hit per point
    improved_corruption: int = 0  # -.4s cast time per point
    improved_curse_of_agony: int = 0  # 2% damage per point
    nightfall: int = 0  # 2% chance per point
    shadow_mastery: int = 0  # 2% shadow damage per point

    # demonology
    improved_imp: int = 0  # 10% imp damage per point
    demonic_sacrifice: int = 0  # 15% shadow damage per point

    # destruction
    improved_shadow_bolt: int = 0  # 4% shadow damage per point on crits
    bane: int = 0  # -.1 sec shadowbolt and -.4 sec immolate per point
    improved_firebolt: int = 0  # 0.5 sec cast time per point
    devastation: int = 0  # 1% destruction crit per point
    improved_searing_pain: int = 0  # 2% crit per point
    improved_immolate: int = 0  # 5% initial damage per point
    ruin: int = 0  # .5x crit mult
    emberstorm: int = 0  # 2% fire damage per point


SMRuin = WarlockTalents(
    # affliction
    suppression=3,
    improved_corruption=5,
    improved_curse_of_agony=3,
    nightfall=2,
    shadow_mastery=5,

    # destruction
    improved_shadow_bolt=5,
    bane=5,
    devastation=5,
    ruin=1,
)

DSRuin = WarlockTalents(
    # affliction
    suppression=2,
    improved_corruption=5,

    # demonology
    demonic_sacrifice=1,

    # destruction
    improved_shadow_bolt=5,
    bane=5,
    devastation=5,
    ruin=1,
)
