from _example_imports import *

mages = []
num_mages = 2

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'test', sp=1085, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0))
    else:
        fm = Mage(name=f'reg{i}', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))

        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0, mqg=0))
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=60, print=False)
sim.detailed_report()
