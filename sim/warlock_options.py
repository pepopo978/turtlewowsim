from dataclasses import dataclass


@dataclass(kw_only=True)
class WarlockOptions:
    permanent_curse: bool = True # assume curse is always up
    firestone: bool = False # 2 % fire crit chance
    crit_dmg_bonus_35: bool = False # 10% crit damage bonus
