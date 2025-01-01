from _example_imports import *

mages = []
num_mages = 2
for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'combined mqg power', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(mqg=5, arcane_power=5))
    elif i == 1:
        fm = Mage(name=f'separate mqg power', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(mqg=5, arcane_power=35))
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=50000, duration=120, print_casts=False)
sim.detailed_report()
