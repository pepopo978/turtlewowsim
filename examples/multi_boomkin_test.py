from _example_imports import *
from sim.druid import Druid
from sim.druid_options import DruidOptions
from sim.druid_talents import BoomkinTalents

boomkins = []
num_boomkins = 2
for i in range(num_boomkins):
    if i == 0:
        d = Druid(name=f'moonfire', sp=1000, crit=40, hit=16, haste=0,
                  tal=BoomkinTalents,
                  opts=DruidOptions(),
                  equipped_items=EquippedItems())
        d.moonfire_starfire_moonfire_insect_swarm_wrath(cds=CooldownUsages())
        boomkins.append(d)
    else:
        d = Druid(name=f'default', sp=1000, crit=40, hit=16, haste=0,
                   tal=BoomkinTalents,
                   opts=DruidOptions(),
                   equipped_items=EquippedItems())
        d.starfire_insect_swarm_wrath(cds=CooldownUsages())
        boomkins.append(d)

sim = Simulation(characters=boomkins)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
