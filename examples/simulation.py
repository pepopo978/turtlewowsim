from classicmagedps import FireEnvironment, FireMage, Simulation

reg_mage1 = FireMage(name='mage1', sp=1008, crit=30.87, hit=16, fullt2=False, haste=2)
reg_mage2 = FireMage(name='mage2', sp=1008, crit=30.87, hit=16, fullt2=False, haste=2)
reg_mage3 = FireMage(name='mage3', sp=1008, crit=30.87, hit=16, fullt2=False, haste=2)

# reg_mage1.smart_scorch_and_fireblast()
# reg_mage2.smart_scorch_and_fireblast()
# reg_mage3.smart_scorch_and_fireblast()
# reg_mage4.smart_scorch_and_fireblast()

reg_mage1.smart_scorch(bezerking30=10)
reg_mage2.smart_scorch()
reg_mage3.smart_scorch()

sim = Simulation(env=FireEnvironment, mages=[reg_mage1, reg_mage2, reg_mage3])
sim.run(iterations=1000, duration=300)

# sim = Simulation(env=FireEnvironment, mages=[reg_mage1, reg_mage2, reg_mage3, reg_mage4])
# sim.run(iterations=5000, duration=200)
