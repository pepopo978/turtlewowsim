from _example_imports import *

locks = []
#
# lock = Warlock(name=f'affli', sp=1005, crit=40, hit=10, tal=AfflictionLock, opts=WarlockOptions())
# lock.cos_corruption_siphon_harvest_drain()
# locks.append(lock)
#
lock = Warlock(name=f'SMRuin', sp=1005, crit=40, hit=10, tal=SMRuin, opts=WarlockOptions())
lock.cos_corruption_shadowbolt()
locks.append(lock)
#
# lock = Warlock(name=f'FireLock', sp=1005, crit=40, hit=10, tal=FireLock, opts=WarlockOptions())
# lock.cos_immo_conflag_soulfire_searing()
# locks.append(lock)

sim = Simulation(characters=locks)
sim.run(iterations=2000, duration=180, use_multiprocessing=True)
sim.detailed_report()
