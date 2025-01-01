from _example_imports import *
from sim.druid import Druid
from sim.druid_options import DruidOptions
from sim.druid_talents import BoomkinTalents

boomkins = []
options = DruidOptions(ignore_arcane_eclipse=True, ignore_nature_eclipse=False, starfire_on_balance_of_all_things_proc=True)

d = Druid(name=f'spam_starfire', sp=1000, crit=30, hit=16, haste=0,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.spam_starfire(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'spam_wrath', sp=1000, crit=30, hit=16, haste=0,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.spam_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'moonfire_starfire', sp=1000, crit=30, hit=16, haste=0,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.moonfire_starfire(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'insect_swarm_starfire', sp=1000, crit=30, hit=16, haste=0,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.insect_swarm_starfire(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)
d = Druid(name=f'insect_swarm_wrath', sp=1000, crit=30, hit=16, haste=0,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.insect_swarm_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'moonfire_wrath', sp=1000, crit=30, hit=16, haste=0,
            tal=BoomkinTalents,
            opts=options,
            equipped_items=EquippedItems())
d.moonfire_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'moonfire_insect_swarm_wrath', sp=1000, crit=30, hit=16, haste=0,
           tal=BoomkinTalents,
           opts=options,
           equipped_items=EquippedItems())
d.moonfire_insect_swarm_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'moonfire_insect_swarm_starfire', sp=1000, crit=30, hit=16, haste=0,
              tal=BoomkinTalents,
              opts=options,
              equipped_items=EquippedItems())
d.moonfire_insect_swarm_starfire(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_wrath_subrotation)
boomkins.append(d)

sim = Simulation(characters=boomkins)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
