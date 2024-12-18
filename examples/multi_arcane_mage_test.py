from _example_imports import *

mages = []
num_mages = 1
for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'arcane_surge_rupture_missiles', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    elif i == 1:
        fm = Mage(name=f'dagger', sp=905, crit=39, hit=15, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    elif i == 2:
        fm = Mage(name=f'arcane_surge_fireblast_rupture_missiles', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.damage_type_hit[DamageType.FIRE] = -6
        fm.arcane_surge_fireblast_rupture_missiles(cds=CooldownUsages())
    else:
        fm = Mage(name=f'arcane_missiles', sp=1000, crit=40, hit=16, haste=0,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(t3_8_set=False, extra_second_arcane_missile=False),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=False,
                  ))
        fm.arcane_missiles(cds=CooldownUsages())
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=50000, duration=120, print_casts=False)
sim.detailed_report()
