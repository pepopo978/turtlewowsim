from _example_imports import *
from sim.druid import Druid
from sim.druid_options import DruidOptions
from sim.druid_talents import BoomkinTalents

boomkins = []
options = DruidOptions(ignore_arcane_eclipse=True, ignore_nature_eclipse=True,
                       starfire_on_balance_of_all_things_proc=True)

base_sp = 820
base_crit = 28
base_hit = 12
base_haste = 0
#
# d = Druid(name=f'spam_starfire', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.spam_starfire(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)
#
# d = Druid(name=f'spam_wrath', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.spam_wrath(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)
#
# d = Druid(name=f'moonfire_starfire', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.moonfire_starfire(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)
#
# d = Druid(name=f'insect_swarm_starfire', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.insect_swarm_starfire(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)
# d = Druid(name=f'insect_swarm_wrath', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.insect_swarm_wrath(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)
#
# d = Druid(name=f'moonfire_wrath', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.moonfire_wrath(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)

d = Druid(name=f'normal', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
          tal=BoomkinTalents,
          opts=options,
          equipped_items=EquippedItems())
d.moonfire_insect_swarm_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
boomkins.append(d)

d = Druid(name=f'extra ticks', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
          tal=BoomkinTalents,
          opts=DruidOptions(ignore_arcane_eclipse=True, ignore_nature_eclipse=True,
                       starfire_on_balance_of_all_things_proc=True, extra_dot_ticks=1),
          equipped_items=EquippedItems())
d.moonfire_insect_swarm_wrath(cds=CooldownUsages())
d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
boomkins.append(d)

# d = Druid(name=f'moonfire_insect_swarm_starfire', sp=base_sp, crit=base_crit, hit=base_hit, haste=base_haste,
#           tal=BoomkinTalents,
#           opts=options,
#           equipped_items=EquippedItems())
# d.moonfire_insect_swarm_starfire(cds=CooldownUsages())
# d.set_arcane_eclipse_subrotation(d.moonfire_insect_swarm_starfire_subrotation)
# d.set_nature_eclipse_subrotation(d.insect_swarm_moonfire_wrath_subrotation)
# boomkins.append(d)

sim = Simulation(characters=boomkins)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
