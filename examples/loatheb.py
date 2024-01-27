from classicmagedps import FireEnvironment, FireMage, Simulation

reg_mage1 = FireMage(name='mage1', sp=950, crit=90, hit=16, fullt2=False, drop_scorch_ignites=True)
reg_mage2 = FireMage(name='mage2', sp=950, crit=90, hit=16, fullt2=False, drop_scorch_ignites=True)
reg_mage3 = FireMage(name='mage3', sp=950, crit=90, hit=16, fullt2=False, drop_scorch_ignites=True)

reg_mage1.smart_scorch(combustion=10)
reg_mage2.smart_scorch(combustion=10)
reg_mage3.smart_scorch(combustion=10)

# env = FireEnvironment()
# env.add_mages([reg_mage1, reg_mage2, reg_mage3])
# env.run(until=2000)
# env.meter.report()

sim = Simulation(env=FireEnvironment, mages=[reg_mage1, reg_mage2, reg_mage3])
sim.run(iterations=1000, duration=300)

# sim = Simulation(env=FireEnvironment, mages=[reg_mage1, reg_mage2, reg_mage3, reg_mage4])
# sim.run(iterations=5000, duration=200)
