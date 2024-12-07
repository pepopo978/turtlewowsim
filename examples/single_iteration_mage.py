from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, haste=4, tal=FireMageTalents)
    if i==0:
        fm.smart_scorch_and_fireblast()
    else:
        fm.smart_scorch()
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=180)
env.meter.report()
