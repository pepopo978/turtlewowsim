from sim.character import CooldownUsages
from sim.env import Environment
from sim.mage import Mage
from sim.mage_options import MageOptions
from sim.mage_talents import ApFrostMageTalents, WcFrostMageTalents

env = Environment(permanent_coe=True)

alice = Mage(name='Alice', sp=500, crit=30, hit=12, opts=MageOptions(fullt2=True), tal=ApFrostMageTalents)
bob = Mage(name='Bob', sp=456, crit=22, hit=16, tal=WcFrostMageTalents)
charlie = Mage(name='Charlie', sp=525, crit=28, hit=9, tal=ApFrostMageTalents)
duncan = Mage(name='Duncan', sp=525, crit=28, hit=9, tal=ApFrostMageTalents)
eddie = Mage(name='Eddie', sp=570, crit=33, hit=15, tal=ApFrostMageTalents)

env.add_characters([alice])

alice.spam_frostbolts(cds=CooldownUsages(arcane_power=3, presence_of_mind=3, mqg=3))
bob.spam_frostbolts()
charlie.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))
duncan.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))
eddie.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))

env.run(until=60)
env.meter.report()
