from classicmagedps import FireMage, FireEnvironment, Simulation

mages = []
num_mages = 1

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1009, crit=33.17, hit=16)
    fm.spam_fireballs(delay=0)
    mages.append(fm)

sim = Simulation(env=FireEnvironment, mages=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
