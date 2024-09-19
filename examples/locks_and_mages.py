from sim.mage import Mage
from sim.mage_talents import FireMageTalents
from sim.simulation import Simulation
from sim.warlock import Warlock
from sim.warlock_options import WarlockOptions
from sim.warlock_talents import SMRuin

characters = []
num_mages = 3
num_locks = 3

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents)
    fm.smart_scorch()
    characters.append(fm)

for i in range(num_locks):
    lock = Warlock(name=f'lock{i}', sp=1005, crit=30.73, hit=10, tal=SMRuin, opts=WarlockOptions())
    lock.corruption_immolate_shadowbolt()
    characters.append(lock)

sim = Simulation(characters=characters)
sim.run(iterations=1000, duration=60)
sim.extended_report()
