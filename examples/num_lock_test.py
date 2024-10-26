from _example_imports import *

locks = []
num_locks = 3

for i in range(num_locks):
    lock = Warlock(name=f'lock{i}', sp=1005, crit=30.73, hit=10, tal=SMRuin, opts=WarlockOptions())
    lock.cos_corruption_shadowbolt()
    locks.append(lock)

    lock = Warlock(name=f'immolate_lock{i}', sp=1005, crit=30.73, hit=10, tal=SMRuin, opts=WarlockOptions())
    lock.cos_corruption_immolate_shadowbolt()
    locks.append(lock)

sim = Simulation(characters=locks)
sim.run(iterations=2000, duration=180)
sim.extended_report()
