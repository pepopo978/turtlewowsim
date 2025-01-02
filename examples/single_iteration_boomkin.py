from _example_imports import *
from sim.druid import Druid
from sim.druid_options import DruidOptions
from sim.druid_talents import BoomkinTalents

boomkins = []
num_boomkins = 1

for i in range(num_boomkins):
    d = Druid(name=f'test', sp=1000, crit=40, hit=16, haste=0,
              tal=BoomkinTalents,
              opts=DruidOptions(ignore_arcane_eclipse=True, ignore_nature_eclipse=True, starfire_on_balance_of_all_things_proc=True),
              equipped_items=EquippedItems())
    d.moonfire_insect_swarm_wrath(cds=CooldownUsages())
    d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
    d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
    boomkins.append(d)

env = Environment(print_dots=True)
env.add_characters(boomkins)
env.run(until=120)
env.meter.detailed_report()
