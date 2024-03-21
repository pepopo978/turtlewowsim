from sim.character import CooldownUsages
from sim.env import Environment
from sim.mage import Mage
from sim.simulation import Simulation
from sim.talents import FireMageTalents

reg_mage1 = Mage(name='mage1', sp=1008, crit=30.87, hit=16, haste=2, tal=FireMageTalents)
reg_mage2 = Mage(name='mage2', sp=1008, crit=30.87, hit=16, haste=2, tal=FireMageTalents)
reg_mage3 = Mage(name='mage3', sp=1008, crit=30.87, hit=16, haste=2, tal=FireMageTalents)

# reg_mage1.smart_scorch_and_fireblast()
# reg_mage2.smart_scorch_and_fireblast()
# reg_mage3.smart_scorch_and_fireblast()
# reg_mage4.smart_scorch_and_fireblast()

reg_mage1.smart_scorch(cds=CooldownUsages(berserking30=10))
reg_mage2.smart_scorch()
reg_mage3.smart_scorch()

sim = Simulation(env=Environment, mages=[reg_mage1, reg_mage2, reg_mage3])
sim.run(iterations=1000, duration=60)
sim.detailed_report()
