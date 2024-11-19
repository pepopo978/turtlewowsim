from _example_imports import *

mages = []
num_mages = 7

base_sp = 1000
base_crit = 100
base_hit = 14

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'mqg', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, mqg=5))
    elif i == 1:
        fm = Mage(name=f'reos', sp=base_sp+40, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, reos=5))
    elif i == 2:
        fm = Mage(name=f'charm_of_magic', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, charm_of_magic=5))
    elif i == 3:
        fm = Mage(name=f'mqg_gulch', sp=base_sp+30, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, mqg=5))
    elif i == 4:
        fm = Mage(name=f'eye of dim', sp=base_sp, crit=base_crit+3, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5))
    elif i == 5:
        fm = Mage(name=f'gulch', sp=base_sp+30, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5))
    elif i == 6:
        fm = Mage(name=f'tear', sp=base_sp+44, crit=base_crit, hit=base_hit+2,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5))
    else:
        fm = Mage(name=f'mark of champ', sp=1085, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5))


    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
