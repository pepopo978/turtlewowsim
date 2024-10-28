from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mqg', sp=1000, crit=40, hit=16,
              tal=ArcaneMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=True,
                  wrath_of_cenarius=True,
              ))
    fm.arcane_surge_rupture_missiles(cds=CooldownUsages())
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=300)
env.meter.report()
