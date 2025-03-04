from dataclasses import dataclass


@dataclass(kw_only=True)
class DruidOptions:
    ignore_arcane_eclipse: bool = False
    ignore_nature_eclipse: bool = False

    starfire_on_balance_of_all_things_proc: bool = False

    extra_dot_ticks: int = 0


