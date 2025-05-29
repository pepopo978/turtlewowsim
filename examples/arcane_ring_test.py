from _example_imports import *

mages = []
num_rings = 1
num_mobs = 1

base_sp = 1000
base_crit = 40
base_hit = 16

cooldowns = CooldownUsages()

for i in range(num_rings):
    m = None
    if i == 0:
        m = Mage(name=f'wrath_of_cenarius', sp=base_sp, crit=base_crit, hit=base_hit,
                 tal=ArcaneMageTalents(),
                 opts=MageOptions(),
                 equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=True,
                  ))
    elif i == 1:
        m = Mage(name=f't3 ring', sp=base_sp + 30, crit=base_crit+1, hit=base_hit,
                 tal=ArcaneMageTalents(),
                 opts=MageOptions(),
                 equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))
    elif i == 2:
        m = Mage(name=f't3 ring arcane (ignoring hit)', sp=base_sp + 36, crit=base_crit, hit=base_hit,
                 tal=ArcaneMageTalents(),
                 opts=MageOptions(),
                 equipped_items=EquippedItems(
                      ornate_bloodstone_dagger=False,
                      wrath_of_cenarius=False,
                  ))

    if m:
        m.arcane_surge_rupture_missiles(cds=cooldowns)
        mages.append(m)

sim = Simulation(characters=mages, num_mobs=num_mobs)
sim.run(iterations=1, duration=120, print_casts=True)
sim.detailed_report()
