from dataclasses import dataclass


@dataclass(kw_only=True)
class EquippedItems:
    blade_of_eternal_darkness: bool = None
    ornate_bloodstone_dagger: bool = None
    wrath_of_cenarius: bool = None
    endless_gulch: bool = None
