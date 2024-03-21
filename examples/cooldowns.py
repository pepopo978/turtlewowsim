from sim.env import Environment
from sim.mage import Mage
from sim.character import CooldownUsages
from sim.talents import FireMageTalents

env = Environment()

mage1 = Mage(env=env, name='Alice', sp=500, crit=30, hit=12, tal=FireMageTalents)
mage2 = Mage(env=env, name='Bob', sp=456, crit=22, hit=16, tal=FireMageTalents)
mage3 = Mage(env=env, name='Charlie', sp=525, crit=28, hit=9, tal=FireMageTalents)
mage4 = Mage(env=env, name='Duncan', sp=525, crit=28, hit=9, tal=FireMageTalents)


env.add_characters([mage1, mage2, mage3, mage4])

mage1.one_scorch_one_pyro_then_fb(cds=CooldownUsages(arcane_power=5, power_infusion=6, mqg=7))
mage2.one_scorch_one_pyro_then_fb(cds=CooldownUsages(combustion=10, mqg=10))
mage3.one_scorch_one_pyro_then_fb()
mage4.one_scorch_one_pyro_then_fb()

env.run(until=60)
env.meter.report()
