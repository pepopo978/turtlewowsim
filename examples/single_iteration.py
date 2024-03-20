from turtlewow_sim.env import Environment
from turtlewow_sim.mage import Mage
from turtlewow_sim.specs import FireMageTalents

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents())
    fm.smart_scorch()
    mages.append(fm)

env = Environment(print_dots=True)
env.add_characters(mages)
env.run(until=180)
env.meter.report()
