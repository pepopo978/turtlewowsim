from _example_imports import *

mages = []
num_mages = 3

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'test', sp=1095, crit=40.43, hit=16,
                  tal=IcicleMageTalents,
                  opts=MageOptions(use_frostnova_for_icicles=True,
                                   start_with_ice_barrier=True),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
    else:
        fm = Mage(name=f'mage{i}', sp=1095, crit=40.43, hit=16,
                  tal=IcicleMageTalents,
                  opts=MageOptions(use_frostnova_for_icicles=True,
                                   start_with_ice_barrier=True))
    fm.icicle_frostbolts()
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=5000, duration=180)
sim.detailed_report()