from classicmagedps import Mage


class FireMage(Mage):
    def __init__(self,
                 name,
                 sp,
                 crit,
                 hit,
                 dmf=False,
                 fire_blast_cooldown=6.5,
                 **kwargs
                 ):
        super().__init__(
            name=name,
            sp=sp,
            crit=crit,
            hit=hit,
            dmf=dmf,
            firepower=True,
            imp_scorch=True,
            incinerate=True,
            winters_chill=False,
            arcane_instability=False,
            piercing_ice=False,
            fire_blast_cooldown=fire_blast_cooldown,
            **kwargs
        )


class ApFireMage(Mage):
    def __init__(self,
                 name,
                 sp,
                 crit,
                 hit,
                 dmf=False,
                 fire_blast_cooldown=8,
                 **kwargs
                 ):
        super().__init__(
            name=name,
            sp=sp,
            crit=crit,
            hit=hit,
            dmf=dmf,
            firepower=False,
            imp_scorch=False,
            incinerate=False,
            winters_chill=False,
            arcane_instability=False,
            piercing_ice=False,
            fire_blast_cooldown=fire_blast_cooldown,
            **kwargs
        )


class ApFrostMage(Mage):
    def __init__(self,
                 name,
                 sp,
                 crit,
                 hit,
                 dmf=False,
                 **kwargs
                 ):
        super().__init__(
            name=name,
            sp=sp,
            crit=crit,
            hit=hit,
            dmf=dmf,
            firepower=False,
            imp_scorch=False,
            incinerate=False,
            winters_chill=False,
            arcane_instability=True,
            piercing_ice=True,
            **kwargs
        )


class WcMage(Mage):
    def __init__(self,
                 name,
                 sp,
                 crit,
                 hit,
                 dmf=False,
                 **kwargs
                 ):
        super().__init__(
            name=name,
            sp=sp,
            crit=crit,
            hit=hit,
            dmf=dmf,
            firepower=False,
            imp_scorch=False,
            incinerate=False,
            winters_chill=True,
            arcane_instability=False,
            piercing_ice=True,
            **kwargs
        )
