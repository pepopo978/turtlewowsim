from turtlewow_sim.character import CooldownUsages
from turtlewow_sim.env import Environment
from turtlewow_sim.mage import Mage
from turtlewow_sim.mage_options import MageOptions
from turtlewow_sim.simulation import Simulation
from turtlewow_sim.specs import FireMageTalents

mages = []
num_mages = 5

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1004, crit=92, hit=16, opts=MageOptions(drop_scorch_ignites=True),
              tal=FireMageTalents())
    fm.smart_scorch(cds=CooldownUsages(combustion=10, power_infusion=1, toep=5))
    mages.append(fm)

# Single run
# env = Environment()
# env.add_characters(mages)
# env.run(until=222)
# env.meter.report()

# multi run
sim = Simulation(env=Environment, mages=mages, coe=True, nightfall=True)
sim.run(iterations=1000, duration=222)
sim.report()
