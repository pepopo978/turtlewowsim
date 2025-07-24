from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    m = Mage(name=f'sulfuras', sp=1020, crit=40, hit=16, haste=1,
             tal=ArcaneMageTalents(),
             opts=MageOptions(),
             equipped_items=EquippedItems(
                 ornate_bloodstone_dagger=False,
                 wrath_of_cenarius=False,
                 endless_gulch=False,
                 true_band_of_sulfuras=False,
             ))
    m.arcane_surge_rupture_missiles(cds=CooldownUsages())
    mages.append(m)

env = Environment(num_mobs=1, mob_level=63)
env.add_characters(mages)
env.run(until=127)
env.meter.detailed_report()
