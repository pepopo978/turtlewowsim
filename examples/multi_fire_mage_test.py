from _example_imports import *

mages = []
num_mages = 1

for i in range(10):
    fm = Mage(name=f'haste{i}', sp=1000, crit=40.43, hit=16, tal=FireMageTalents, haste=i)
    fm.smart_scorch()

    sim = Simulation(characters=[fm])
    sim.run(iterations=20000, duration=120)
    sim.detailed_report()
