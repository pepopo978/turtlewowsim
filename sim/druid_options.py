from dataclasses import dataclass


@dataclass(kw_only=True)
class DruidOptions:
    ignore_arcane_eclipse: bool = False
    ignore_nature_eclipse: bool = False

    starfire_on_balance_of_all_things_proc: bool = False
    set_bonus_3_dot_dmg: bool = False # extra 15% dot dmg
    set_bonus_3_5_boat: bool = False # extra .25 sec off of starfire cast time from balance of all things

    extra_dot_ticks: int = 0
    ebb_and_flow_idol: bool = False


