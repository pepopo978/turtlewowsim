from _example_imports import *

mages = []
#
m = Mage(name=f'boed', sp=905, crit=39, hit=16, haste=9,
         tal=ArcaneMageTalents,
         opts=MageOptions(interrupt_arcane_missiles=False),
         equipped_items=EquippedItems(
             blade_of_eternal_darkness=True,
             wrath_of_cenarius=True,
             endless_gulch=False,
         ))
m.spam_arcane_explosion(cds=CooldownUsages(arcane_power=5, mqg=5))
mages.append(m)

m = Mage(name=f'ornate', sp=905, crit=39, hit=16, haste=9,
         tal=ArcaneMageTalents,
         opts=MageOptions(interrupt_arcane_missiles=False),
         equipped_items=EquippedItems(
             ornate_bloodstone_dagger=True,
             wrath_of_cenarius=True,
             endless_gulch=False,
         ))
m.spam_arcane_explosion(cds=CooldownUsages(arcane_power=5, mqg=5))
mages.append(m)
#
m = Mage(name=f'normal', sp=1000, crit=40, hit=16, haste=5,
         tal=ArcaneMageTalents,
         opts=MageOptions(interrupt_arcane_missiles=False),
         equipped_items=EquippedItems(
             ornate_bloodstone_dagger=False,
             wrath_of_cenarius=True,
             endless_gulch=False,
         ))
m.spam_arcane_explosion(cds=CooldownUsages(arcane_power=5, mqg=5))
mages.append(m)
#
# m = Mage(name=f'reos', sp=1000, crit=40, hit=16, haste=0,
#          tal=ArcaneMageTalents,
#          opts=MageOptions(interrupt_arcane_missiles=False),
#          equipped_items=EquippedItems(
#              ornate_bloodstone_dagger=False,
#              wrath_of_cenarius=True,
#              endless_gulch=False,
#          ))
# m.arcane_missiles(cds=CooldownUsages())
# mages.append(m)
#
# m = Mage(name=f'double reos', sp=1040, crit=40, hit=16, haste=8,
#          tal=ArcaneMageTalents,
#          opts=MageOptions(interrupt_arcane_missiles=True),
#          equipped_items=EquippedItems(
#              ornate_bloodstone_dagger=False,
#              wrath_of_cenarius=True,
#              endless_gulch=False,
#          ))
# m.arcane_rupture_surge_missiles(cds=CooldownUsages(arcane_power=5, reos=[5, 150]))
# mages.append(m)

sim = Simulation(characters=mages, num_mobs=5, mob_level=63)
sim.run(iterations=10000, duration=30, print_casts=False)
sim.detailed_report()
