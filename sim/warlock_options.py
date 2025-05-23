from dataclasses import dataclass


@dataclass(kw_only=True)
class WarlockOptions:
    permanent_curse: bool = True # assume curse is always up
    firestone: bool = False # 2 % fire crit chance
    crit_dmg_bonus_35: bool = False # 10% crit damage bonus
    siphon_life_bonus_35: bool = False # 50% more siphon
    use_nightfall_as_affliction: bool = False # use nightfall on shadow bolt as affliction
    use_nightfall_as_fire: bool = False
