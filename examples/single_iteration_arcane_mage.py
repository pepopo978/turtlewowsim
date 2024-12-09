from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mqg', sp=1000, crit=40.4, hit=16,
              tal=ArcaneMageTalents,
              opts=MageOptions(t3_8_set=False),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=False,
                  wrath_of_cenarius=True,
                  endless_gulch=False,
              ))
    fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=5, mqg=5))
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=127)
env.meter.report()
