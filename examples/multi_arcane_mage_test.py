from _example_imports import *

mages = []
num_mages = 3

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'test', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    else:
        fm = Mage(name=f'reg{i}', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))

        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=120, print=False)
sim.detailed_report()
