from dataclasses import dataclass
from typing import Optional, Union, List


@dataclass(kw_only=True)
class CooldownUsages:
    # Mage
    combustion: Optional[Union[float, List[float]]] = None
    arcane_power: Optional[Union[float, List[float]]] = None
    presence_of_mind: Optional[Union[float, List[float]]] = None

    # Buffs
    power_infusion: Optional[Union[float, List[float]]] = None
    berserking30: Optional[Union[float, List[float]]] = None
    berserking20: Optional[Union[float, List[float]]] = None
    berserking10: Optional[Union[float, List[float]]] = None

    # Trinkets
    toep: Optional[Union[float, List[float]]] = None
    mqg: Optional[Union[float, List[float]]] = None
    reos: Optional[Union[float, List[float]]] = None
