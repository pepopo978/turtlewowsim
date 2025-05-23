from _example_imports import *
from sim.warlock_talents import *

locks = []

control_sp = 1000
control_crit = 35
control_hit = 13
control_haste = 0

options = WarlockOptions(crit_dmg_bonus_35=False)
talents = FireLock

d = Warlock(name=f'control', sp=control_sp, crit=control_crit, hit=control_hit, haste=control_haste,
          tal=talents,
          opts=options,
          equipped_items=EquippedItems())
locks.append(d)

d = Warlock(name=f'1 hit', sp=control_sp, crit=control_crit, hit=control_hit + 1, haste=control_haste,
         tal=talents,
         opts=options,
         equipped_items=EquippedItems())
locks.append(d)

d = Warlock(name=f'1 crit', sp=control_sp, crit=control_crit + 1, hit=control_hit, haste=control_haste,
         tal=talents,
         opts=options,
         equipped_items=EquippedItems())
locks.append(d)

d = Warlock(name=f'1 haste', sp=control_sp, crit=control_crit, hit=control_hit, haste=control_haste + 1,
         tal=talents,
         opts=options,
         equipped_items=EquippedItems())
locks.append(d)

d = Warlock(name=f'20sp', sp=control_sp + 20, crit=control_crit, hit=control_hit, haste=control_haste,
         tal=talents,
         opts=options,
         equipped_items=EquippedItems())
locks.append(d)

for lock in locks:
    # lock.coa_corruption_siphon_harvest_drain()
    # lock.coa_corruption_siphon_shadowbolt()
    lock.immo_conflag_soulfire_searing()

sim = Simulation(characters=locks)
sim.run(iterations=10000, duration=300, print_casts=False, use_multiprocessing=True)
sim.detailed_report()
