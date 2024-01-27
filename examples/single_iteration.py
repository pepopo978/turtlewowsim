from classicmagedps import FireEnvironment, FireMage

env = FireEnvironment()

reg_mage1 = FireMage(name='mage1', sp=945, crit=30, hit=16, fullt2=True)

reg_mage1.smart_scorch(combustion=10, arcane_power=30, presence_of_mind=30)

env.add_mages([reg_mage1])

env.run(until=120)
env.meter.report()
