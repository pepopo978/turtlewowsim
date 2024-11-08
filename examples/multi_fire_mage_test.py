from _example_imports import *

mages = []
num_mages = 3

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1000, crit=40.43, hit=16, tal=FireMageTalents)
    fm.smart_scorch_and_fireblast()
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=120)
sim.detailed_report()
