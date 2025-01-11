from _example_imports import *

mages = []
num_mages = 2

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'kt neck', sp=1000+15, crit=40+2, hit=16, haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(use_frostnova_for_icicles=True,
                                   start_with_ice_barrier=True))
        fm.icicle_frostbolts(cds=CooldownUsages())
        mages.append(fm)
    if i == 1:
        fm = Mage(name=f'twins neck', sp=1000+27, crit=40+1, hit=16, haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(use_frostnova_for_icicles=True,
                                   start_with_ice_barrier=True))
        fm.icicle_frostbolts(cds=CooldownUsages())
        mages.append(fm)

sim = Simulation(characters=mages, num_mobs=1)
sim.run(iterations=10000, duration=120)
sim.detailed_report()
