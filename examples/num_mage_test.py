from sim.env import Environment
from sim.mage import Mage
from sim.simulation import Simulation
from sim.talents import FireMageTalents

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1031, crit=33.17, hit=16, tal=FireMageTalents)
    fm.smart_scorch()
    mages.append(fm)

sim = Simulation(env=Environment, mages=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
