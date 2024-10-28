from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'haste', sp=1000, crit=40, hit=15, haste=0,
              tal=ArcaneMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=True,
                  wrath_of_cenarius=True,
              ))
    fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0, charm_of_magic=0))
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=90)
env.meter.report()
