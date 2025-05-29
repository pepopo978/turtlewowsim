from dataclasses import dataclass
from sim.decorators import simoption

@dataclass(kw_only=True)
class WarlockOptions:
    permanent_curse: bool = simoption("Assume curse is always up", default=True)
    firestone: bool = simoption("2% fire crit chance", default=False)
    crit_dmg_bonus_35: bool = simoption("10% crit damage bonus", default=False)
    siphon_life_bonus_35: bool = simoption("50% more siphon", default=False)
    use_nightfall_as_affliction: bool = simoption("Use nightfall on shadow bolt as affliction", default=False)
    use_nightfall_as_fire: bool = simoption("Use nightfall on fire", default=False)
