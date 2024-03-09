from classicmagedps import FireMage, FireEnvironment, Simulation

mages = []
num_mages = 1

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1004, crit=32, hit=16)
    fm.smart_scorch()
    mages.append(fm)


sim = Simulation(env=FireEnvironment, mages=mages)
sim.run(iterations=1000, duration=300)
