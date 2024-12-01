from dataclasses import dataclass


@dataclass(kw_only=True)
class DruidOptions:
    ignore_arcane_eclipse: bool = False
    ignore_nature_eclipse: bool = False


