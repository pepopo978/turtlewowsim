from turtlewow_sim.env import Environment
from turtlewow_sim.mage import Mage
from turtlewow_sim.simulation import Simulation
from turtlewow_sim.specs import FireMageTalents

mages = []
num_mages = 5

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents())
    fm.smart_scorch()
    mages.append(fm)

sim = Simulation(env=Environment, mages=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
