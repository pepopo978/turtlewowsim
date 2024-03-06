from classicmagedps import FireEnvironment, FireMage

env = FireEnvironment()

mages = []
num_mages = 2

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1004, crit=32, hit=16, fullt2=False)
    fm.smart_scorch(delay=0)
    mages.append(fm)

env.add_mages(mages)
env.run(until=120)
env.meter.report()
