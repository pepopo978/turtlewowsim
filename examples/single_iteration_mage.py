from sim.env import Environment
from sim.mage import Mage
from sim.mage_options import MageOptions
from sim.mage_talents import FireMageTalents

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents)
    fm.tal.hot_streak = False
    if i==0:
        fm.smart_scorch_and_fireblast()
    else:
        fm.smart_scorch()
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=180)
env.meter.report()
