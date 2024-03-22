from sim.env import Environment
from sim.warlock import Warlock
from sim.warlock_options import WarlockOptions
from sim.warlock_talents import SMRuin, DSRuin

locks = []
num_locks = 1

for i in range(num_locks):
    lock = Warlock(name=f'lock{i}', sp=1005, crit=30.73, hit=10, tal=SMRuin, opts=WarlockOptions())
    lock.cos_corruption_shadowbolt()
    locks.append(lock)

    lock = Warlock(name=f'immolate_lock{i}', sp=1005, crit=30.73, hit=10, tal=SMRuin, opts=WarlockOptions())
    lock.cos_corruption_immolate_shadowbolt()
    locks.append(lock)

env = Environment(print_dots=True, permanent_cos=True)
env.add_characters(locks)
env.run(until=180)
env.meter.report()
