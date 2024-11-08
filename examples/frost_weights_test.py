from _example_imports import *

mages = []
num_mages = 5

for i in range(num_mages):
    fm = None
    if i == 0:
        fm = Mage(name=f'control', sp=1000, crit=40, hit=15, haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
        fm.icicle_frostbolts()
    elif i == 1:
        fm = Mage(name=f'1 hit', sp=1000, crit=40, hit=16,haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
        fm.icicle_frostbolts()
    elif i == 2:
        fm = Mage(name=f'1 crit', sp=1000, crit=41, hit=15,haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
        fm.icicle_frostbolts()
    elif i == 3:
        fm = Mage(name=f'1 haste', sp=1000, crit=40, hit=15, haste=1,
                  tal=IcicleMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
        fm.icicle_frostbolts()
    elif i == 4:
        fm = Mage(name=f'20sp', sp=1020, crit=40, hit=15,haste=0,
                  tal=IcicleMageTalents,
                  opts=MageOptions(),
                  equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
        fm.icicle_frostbolts()

    if fm:
        mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=50000, duration=120, print_casts=False)
sim.detailed_report()
