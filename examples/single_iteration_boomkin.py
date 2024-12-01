from _example_imports import *
from sim.druid import Druid
from sim.druid_options import DruidOptions
from sim.druid_talents import BoomkinTalents

druids = []
num_mages = 1

for i in range(num_mages):
    d = Druid(name=f'druid', sp=1000, crit=40.4, hit=16,
              tal=BoomkinTalents,
              opts=DruidOptions(),
              equipped_items=EquippedItems())
    d.starfire_wrath_eclipse()
    druids.append(d)

env = Environment(print_dots=True)
env.add_characters(druids)
env.run(until=120)
env.meter.report()
