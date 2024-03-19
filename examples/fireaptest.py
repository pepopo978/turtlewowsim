from classicmagedps import FireEnvironment, FireMage, Simulation
from classicmagedps.specs import ApFireMage

reg_mage1 = FireMage(name='reg_mage1', sp=945, crit=30, hit=16, fullt2=False)
ap_fire = ApFireMage(name='ap_fire', sp=945, crit=30, hit=16, fullt2=False)

reg_mage1.smart_scorch(combustion=10, mqg=10)
ap_fire.spam_fireballs(combustion=10, mqg=10, arcane_power=10, presence_of_mind=10)

sim = Simulation(env=FireEnvironment, mages=[reg_mage1, ap_fire])
sim.run(iterations=1000, duration=200)
sim.report()

# env = FireEnvironment()
# env.add_mages([reg_mage1, ap_fire])
# env.run(until=120)
# env.meter.report()
