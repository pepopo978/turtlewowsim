from _example_imports import *

mages = []
num_trinkets = 10

base_sp = 1000
base_crit = 40
base_hit = 16

for i in range(num_trinkets):
    fm = None
    cds = CooldownUsages(arcane_power=5)
    if i == 0:
        fm = Mage(name=f'nothing', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
    elif i == 1:
        fm = Mage(name=f'reos', sp=base_sp+40, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        cds = CooldownUsages(arcane_power=5, reos=5)
    elif i == 2:
        fm = Mage(name=f'charm_of_magic', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        cds = CooldownUsages(arcane_power=5, charm_of_magic=5)
    elif i == 3:
        fm = Mage(name=f'eye of dim', sp=base_sp, crit=base_crit+3, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
    elif i == 4:
        fm = Mage(name=f'gulch', sp=base_sp+30, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                      endless_gulch=True,
                  ))
    elif i == 5:
        fm = Mage(name=f'tear', sp=base_sp+44, crit=base_crit, hit=base_hit+2,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
    elif i == 6:
        fm = Mage(name=f'toep', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        cds = CooldownUsages(arcane_power=5, toep=5)
    elif i == 7:
        fm = Mage(name=f'mqg', sp=base_sp, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
        cds = CooldownUsages(arcane_power=5, mqg=5)
    elif i==8:
        fm = Mage(name=f'mark of champ', sp=base_sp+85, crit=base_crit, hit=base_hit,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
    elif i==9:
        fm = Mage(name=f'shard of nightmare', sp=base_sp+36, crit=base_crit, hit=base_hit+1,
                  tal=ArcaneMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))

    if fm:
        fm.spam_arcane_explosion(cds=cds)
        mages.append(fm)

sim = Simulation(characters=mages, num_mobs=3, mob_level=60)
sim.run(iterations=10000, duration=30, print_casts=False)
sim.detailed_report()
