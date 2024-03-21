from sim.env import Environment
from sim.mage import Mage
from sim.simulation import Simulation
from sim.mage_talents import FireMageTalents
from sim.warlock import Warlock
from sim.warlock_options import WarlockOptions
from sim.warlock_talents import SMRuin

locks = []
num_locks = 3

for i in range(num_locks):
    fm = Warlock(name=f'lock{i}', sp=1009, crit=33.17, hit=16, tal=SMRuin, opts=WarlockOptions())
    fm.corruption_immolate_shadowbolt()
    locks.append(fm)

sim = Simulation(characters=locks)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
