from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'gulch', sp=1000, crit=35, hit=16,
              tal=FireMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(endless_gulch=True, true_band_of_sulfuras=True))
    fm.smart_scorch_and_fireblast(cds=CooldownUsages())
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=180)
env.meter.detailed_report()
