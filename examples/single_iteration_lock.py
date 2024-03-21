from sim.env import Environment
from sim.warlock import Warlock
from sim.warlock_options import WarlockOptions
from sim.warlock_talents import SMRuin

locks = []
num_locks = 3

for i in range(num_locks):
    fm = Warlock(name=f'lock{i}', sp=1009, crit=33.17, hit=16, tal=SMRuin, opts=WarlockOptions())
    fm.corruption_immolate_shadowbolt()
    locks.append(fm)

env = Environment(print_dots=True)
env.add_characters(locks)
env.run(until=180)
env.meter.report()
