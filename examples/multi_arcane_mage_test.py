from _example_imports import *

mages = []
num_mages = 2
for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'test', sp=990, crit=37, hit=16, haste=2,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=True),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                      endless_gulch=False,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    else:
        fm = Mage(name=f'reg', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                      endless_gulch=False,
                  ))

        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
