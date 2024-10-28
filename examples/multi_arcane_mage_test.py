from _example_imports import *

mages = []
num_mages = 3

for i in range(num_mages):
    if i==0:
        fm = Mage(name=f'procs', sp=1000, crit=40, hit=15,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
    else:
        fm = Mage(name=f'reg{i}', sp=1000, crit=40, hit=15,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())

    fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0))
    # fm.arcane_rupture_surge_missiles(cds=CooldownUsages(arcane_power=0))
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
