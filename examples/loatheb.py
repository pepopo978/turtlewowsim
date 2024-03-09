from classicmagedps import FireEnvironment, FireMage, Simulation

mages = []
num_mages = 5

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1004, crit=92, hit=16, drop_scorch_ignites=True)
    fm.smart_scorch(combustion=10, power_infusion=1, toep=5)
    mages.append(fm)

# Single run
# env = FireEnvironment()
# env.add_mages(mages)
# env.run(until=222)
# env.meter.report()

# multi run
sim = Simulation(env=FireEnvironment, mages=mages, coe=True, nightfall=True)
sim.run(iterations=1000, duration=222)
