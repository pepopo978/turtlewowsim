from _example_imports import *

mages = []
num_mages = 5

for i in range(num_mages):
    if i==0:
        fm = Mage(name=f'control', sp=1000, crit=40, hit=15,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())
    elif i==1:
        fm = Mage(name=f'crit', sp=1000, crit=41, hit=15,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())
    elif i==2:
        fm = Mage(name=f'hit', sp=1000, crit=40, hit=16,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())
    elif i==3:
        fm = Mage(name=f'haste', sp=1000, crit=40, hit=15, haste=1,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())
    else:
        fm = Mage(name=f'20sp', sp=1020, crit=40, hit=15,
                  tal=ArcaneMageTalents,
                  opts=MageOptions())

    fm.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0))
    # fm.arcane_rupture_surge_missiles(cds=CooldownUsages(arcane_power=0))
    mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
