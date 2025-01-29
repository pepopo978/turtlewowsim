from _example_imports import *

mages = []

m = Mage(name=f'no interrupt', sp=1000, crit=40, hit=16, haste=9,
         tal=ArcaneMageTalents,
         opts=MageOptions(interrupt_arcane_missiles=False),
         equipped_items=EquippedItems(
             ornate_bloodstone_dagger=False,
             wrath_of_cenarius=True,
             endless_gulch=False,
         ))
m.arcane_surge_rupture_missiles(cds=CooldownUsages())
mages.append(m)

m = Mage(name=f'interrupt', sp=1000, crit=40, hit=16, haste=9,
         tal=ArcaneMageTalents,
         opts=MageOptions(interrupt_arcane_missiles=True),
         equipped_items=EquippedItems(
             ornate_bloodstone_dagger=False,
             wrath_of_cenarius=True,
             endless_gulch=False,
         ))
m.arcane_surge_rupture_missiles(cds=CooldownUsages())
mages.append(m)

sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
