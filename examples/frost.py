from sim.character import CooldownUsages
from sim.env import Environment
from sim.mage import Mage
from sim.mage_options import MageOptions
from sim.talents import ApFrostMageTalents, WcFrostMageTalents

env = Environment()

alice = Mage(env=env, name='Alice', sp=500, crit=30, hit=12, opts=MageOptions(fullt2=True), tal=ApFrostMageTalents)
bob = Mage(env=env, name='Bob', sp=456, crit=22, hit=16, tal=WcFrostMageTalents)
charlie = Mage(env=env, name='Charlie', sp=525, crit=28, hit=9, tal=ApFrostMageTalents)
duncan = Mage(env=env, name='Duncan', sp=525, crit=28, hit=9, tal=ApFrostMageTalents)
eddie = Mage(env=env, name='Eddie', sp=570, crit=33, hit=15, tal=ApFrostMageTalents)

env.add_characters([alice, bob, charlie, duncan, eddie])

alice.spam_frostbolts(cds=CooldownUsages(arcane_power=0, presence_of_mind=0, mqg=3))
bob.spam_frostbolts()
charlie.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))
duncan.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))
eddie.spam_frostbolts(cds=CooldownUsages(arcane_power=15, presence_of_mind=15))

env.run(until=60)
env.meter.report()
