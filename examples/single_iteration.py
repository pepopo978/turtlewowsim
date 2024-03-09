from classicmagedps import FireEnvironment, FireMage

env = FireEnvironment()

mages = []
num_mages = 3

for i in range(num_mages):
    fm = FireMage(name=f'mage{i}', sp=1004, crit=32, hit=16)
    fm.smart_scorch()
    mages.append(fm)

env.add_mages(mages)
env.run(until=300)
env.meter.report()
