from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'haste', sp=1000, crit=40, hit=15, haste=0,
              tal=ArcaneMageTalents,
              opts=MageOptions())
    fm.arcane_surge_rupture_missiles()
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=300)
env.meter.report()
