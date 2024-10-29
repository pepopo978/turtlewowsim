from _example_imports import *

mages = []
num_mages = 6

for i in range(num_mages):
    if i == 0:
        fm = Mage(name=f'mqg', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330, mqg=0))
    elif i == 1:
        fm = Mage(name=f'reos', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330, reos=0))
    elif i == 2:
        fm = Mage(name=f'charm_of_magic', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330, charm_of_magic=0))
    elif i == 3:
        fm = Mage(name=f'toep', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330, toep=0))
    elif i == 4:
        fm = Mage(name=f'eye of dim', sp=1000, crit=43, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330))
    else:
        fm = Mage(name=f'mark of champ', sp=1085, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=True,
                      wrath_of_cenarius=True,
                  ))
        fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=330))


    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=60, print_casts=False)
sim.detailed_report()
