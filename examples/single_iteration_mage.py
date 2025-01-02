from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'fire', sp=1000, crit=40.43, hit=16, tal=FireMageTalents, haste=3,
              opts=MageOptions())
    fm.smart_scorch(CooldownUsages(combustion=5))
    mages.append(fm)

env = Environment()
env.add_characters(mages)
env.run(until=180)
env.meter.detailed_report()
