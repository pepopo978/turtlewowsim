from _example_imports import *

mages = []

arcane = Mage(name=f'arcane', sp=1027, crit=45.43, hit=16,
              tal=ArcaneMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=False,
                  wrath_of_cenarius=True,
              ))
arcane.arcane_surge_rupture_missiles(cds=CooldownUsages(arcane_power=0))
mages.append(arcane)

fire = Mage(name=f'fire', sp=1057, crit=46.43, hit=16, tal=FireMageTalents, opts=MageOptions())
fire.smart_scorch_and_fireblast(cds=CooldownUsages(combustion=10))
mages.append(fire)

frost = Mage(name=f'frost', sp=1095, crit=40.43, hit=16,
             tal=IcicleMageTalents,
             opts=MageOptions(use_frostnova_for_icicles=True,
                              start_with_ice_barrier=True),
             )
frost.icicle_frostbolts()
mages.append(frost)

sim = Simulation(characters=mages)
sim.run(iterations=2000, duration=90, print=False)
sim.detailed_report()
