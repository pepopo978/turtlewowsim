from _example_imports import *

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mqg reos', sp=1040, crit=40, hit=16,
              tal=ArcaneMageTalents,
              opts=MageOptions(),
              equipped_items=EquippedItems(
                  ornate_bloodstone_dagger=False,
                  wrath_of_cenarius=True,
              ))
    fm.spam_arcane_explosion(cds=CooldownUsages(arcane_power=5, mqg=5, reos=6))
    mages.append(fm)

env = Environment(num_mobs=2)
env.add_characters(mages)
env.run(until=127)
env.meter.report()
