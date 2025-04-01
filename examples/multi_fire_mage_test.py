from _example_imports import *

mages = []

fm = Mage(name=f'fireball->fireblast', sp=1000, crit=40.43, hit=16, haste=3,
          tal=FireMageTalents,
          opts=MageOptions())
fm.smart_scorch_and_fireblast(CooldownUsages(combustion=10, mqg=10))
mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()

mages = []
fm = Mage(name=f'fireball->fireblast->scorch', sp=1000, crit=40.43, hit=16, haste=3,
          tal=FireMageTalents,
          opts=MageOptions(extend_ignite_with_scorch=True),
          equipped_items=EquippedItems(ornate_bloodstone_dagger=False))
fm.smart_scorch_and_fireblast(CooldownUsages(combustion=10, mqg=10))
mages.append(fm)


sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()

mages = []
fm = Mage(name=f'fireball->scorch', sp=1000, crit=40.43, hit=16, haste=3,
          tal=FireMageTalents,
          opts=MageOptions(extend_ignite_with_scorch=True, remaining_seconds_for_ignite_extend=6),
          equipped_items=EquippedItems(ornate_bloodstone_dagger=False))
fm.smart_scorch(CooldownUsages(combustion=10, mqg=10))
mages.append(fm)

# fm = Mage(name=f'fireblast extend', sp=1000, crit=40.43, hit=16, tal=FireMageTalents, haste=3,
#           opts=MageOptions(extend_ignite_with_fire_blast=True,
#                            extend_ignite_with_scorch=False,
#                            remaining_seconds_for_ignite_extend=3))
# fm.smart_scorch(CooldownUsages(combustion=5, mqg=5))
# mages.append(fm)

sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
