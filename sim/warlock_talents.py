from dataclasses import dataclass


@dataclass(kw_only=True)
class WarlockTalents:
    # affliction
    suppression: int = 0  # 2% hit per point
    improved_corruption: int = 0  # -.3s cast time per point
    improved_curse_of_agony: int = 0  # 3/6/10% damage per point
    improved_drains: int = 0  # 5/10% increase on drain soul
    nightfall: int = 0  # 1/3/5% chance per point
    rapid_deterioration: int = 0  # 6% affliction haste, 50/100% of haste reduces dot tick time
    soul_siphon: int = 0  # 2/4/6% drain soul/dark harvest dmg increase per effect on target
    shadow_mastery: int = 0  # 2/4/6/8/10% shadow damage

    # demonology
    improved_imp: int = 0  # 10% imp damage per point
    soul_entrapment: int = 0  # 1/2/3% increased dmg if no demon
    imp_sacrifice: int = 0  # 6% fire dmg
    succubus_sacrifice: int = 0  # 6% shadow dmg
    unholy_power: int = 0 # 5/10/15% demon dmg
    demonic_precision: int = 0  # 33/66/100% shared spell hit/crit with demon

    imp_master_demonologist: int = 0  # 1% haste per point
    succubus_master_demonologist: int = 0 # 2% damage per point
    infernal_master_demonologist: int = 0 # 3% haste per point
    felguard_master_demonologist: int = 0 # 4% damage per point

    soul_link: int = 0 # 5% damage for you and demon

    # destruction
    improved_shadow_bolt: int = 0  # 4% shadow damage per point.  20% chance per point to apply on crit.  2% chance per point to apply on regular hit
    demonic_swiftness: int = 0  # reduce imp cast time by .3/.5 sec
    bane: int = 0  # -.1 sec shadowbolt/immolate and -.4 sec soul fire per point
    aftermath: int = 0  # 2/4/6 % immolate damage
    devastation: int = 0  # 1% destruction crit per point
    improved_searing_pain: int = 0  # 2% crit per point
    improved_soul_shard: int = 0  # 8% fire damage for 30 sec after soul fire
    improved_immolate: int = 0 # 4% immolate damage per point
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

    # destruction
    improved_shadow_bolt=5,
    bane=5,
    devastation=5,
    ruin=1,
)
