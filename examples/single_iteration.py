from classicmagedps import FireEnvironment, FireMage

env = FireEnvironment()

mages = []
num_mages = 1

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1004, crit=32.3, hit=16, haste=2)
    fm.spam_fireballs()
    mages.append(fm)

env.add_mages(mages)
env.run(until=180)
env.meter.report()
