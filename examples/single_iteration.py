from sim.env import Environment
from sim.mage import Mage
from sim.mage_options import MageOptions
from sim.talents import FireMageTalents

mages = []
num_mages = 3

for i in range(num_mages):
    tal = FireMageTalents
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=tal,
              opts=MageOptions(extend_ignite_with_scorch=True))
    fm.smart_scorch()
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=180)
env.meter.report()
