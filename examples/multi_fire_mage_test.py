from _example_imports import *

# mages = []
#
# fm = Mage(name=f'regular', sp=1000, crit=40.43, hit=16, haste=3,
#           tal=FireMageTalents,
#           opts=MageOptions(extend_ignite_with_scorch=True))
# fm.smart_scorch_and_fireblast(CooldownUsages(combustion=10, mqg=10))
# mages.append(fm)
#
# sim = Simulation(characters=mages)
# sim.run(iterations=10000, duration=120, print_casts=False)
# sim.detailed_report()

mages = []
fm = Mage(name=f'unceasing frost extend ignite', sp=960, crit=40.43, hit=16, haste=3,
          tal=FireMageTalents,
          opts=MageOptions(extend_ignite_with_scorch=True),
          equipped_items=EquippedItems(unceasing_frost=False))
fm.smart_scorch_and_fireblast(CooldownUsages(combustion=10, mqg=10))
mages.append(fm)


sim = Simulation(characters=mages)
sim.run(iterations=10000, duration=120, print_casts=False)
sim.detailed_report()
