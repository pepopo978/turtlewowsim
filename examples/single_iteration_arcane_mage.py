from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'test', sp=1000, crit=40, hit=16,
              tal=ArcaneMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=False,
                  wrath_of_cenarius=True,
              ))
    fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, zhc=5))
    mages.append(fm)

env = Environment(num_mobs=1, mob_level=63)
env.add_characters(mages)
env.run(until=127)
env.meter.detailed_report()
