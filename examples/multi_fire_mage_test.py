from _example_imports import *

mages = []
num_mages = 3

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents)
    fm.smart_scorch_and_fireblast()
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=60)
sim.detailed_report()
