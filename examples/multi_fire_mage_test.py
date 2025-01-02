from _example_imports import *

mages = []

fm = Mage(name=f'normal', sp=1000, crit=40.43, hit=16,
          tal=MageTalents(
              ignite=5,
              imp_scorch=3,
              fire_power=5,
              critical_mass=0,  # generally counted in crit already, 2% per point
              hot_streak=3,
              incinerate_crit=4,
              fire_blast_cooldown=6.5,
              fire_blast_gcd=1
          ),
          haste=3)
fm.smart_scorch_and_fireblast(CooldownUsages(combustion=5))
mages.append(fm)
#
# fm = Mage(name=f'scorch spam', sp=1000, crit=40.43, hit=16, tal=FireMageTalents, haste=3,
#           opts=MageOptions(extend_ignite_with_scorch=True,
#                            extend_ignite_with_fire_blast=True,
#                            drop_suboptimal_ignites=True,
#                            remaining_seconds_for_ignite_extend=7),
#           equipped_items=EquippedItems(ornate_bloodstone_dagger=False))
# fm.smart_scorch(CooldownUsages(combustion=5, mqg=5))
# mages.append(fm)

# fm = Mage(name=f'fireblast extend', sp=1000, crit=40.43, hit=16, tal=FireMageTalents, haste=3,
#           opts=MageOptions(extend_ignite_with_fire_blast=True,
#                            extend_ignite_with_scorch=False,
#                            remaining_seconds_for_ignite_extend=3))
# fm.smart_scorch(CooldownUsages(combustion=5, mqg=5))
# mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=100000, duration=130, print_casts=False)
sim.detailed_report()
