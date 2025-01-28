from dataclasses import dataclass


@dataclass(kw_only=True)
class WarlockOptions:
    firestone: bool = False # 2 % fire crit chance
