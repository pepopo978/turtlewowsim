# turtlewowsim

Simulation for Turtle WoW that currently supports Fire/Frost Mages.

## Installation

Need python 3.10 or later and Poetry to install dependencies

## Usage
<p align="center">
        <a href="https://repl.it/@mcdallas/CrowdedBowedLinuxpc"><img src="https://repl.it/badge/github/mcdallas/classicmagedps" align="center" /></a>
</p>
For a single iteration:

``` python
from turtlewow_sim.env import Environment
from turtlewow_sim.mage import Mage
from turtlewow_sim.specs import FireMageTalents

mages = []
num_mages = 1

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents())
    fm.smart_scorch()
    mages.append(fm)

env = Environment(print_dots=True)
env.add_characters(mages)
env.run(until=180)
env.meter.report()

```

You will get an output like this
```
[2.1] - (mage0) scorch (1.6 cast) 825
[2.8] - (mage1) scorch (1.6 cast) 847
[3.7] - (mage0) scorch (1.6 cast) **1254**
[4.4] - (mage1) scorch (1.6 cast) **1333**
[5.3] - (mage0) scorch (1.6 cast) 925
[5.7] - (mage0) (2) ignite tick 654 ticks remaining 1 time left 2.74s
[6.0] - (mage1) scorch (1.6 cast) **1396**
[7.7] - (mage0) (3) ignite tick 1007 ticks remaining 1 time left 2.34s
[8.4] - (mage0) fireball (3.1 cast) **3574**
[9.1] - (mage1) fireball (3.1 cast) 2455
[9.7] - (mage0) (4) ignite tick 1911 ticks remaining 1 time left 2.7s
[11.5] - (mage0) fireball (3.1 cast) **3519**
[11.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 3.8s
[12.2] - (mage1) fireball (3.1 cast) **3577**
[13.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 2.54s
[14.6] - (mage0) fireball (3.1 cast) **3477**
[15.3] - (mage1) fireball (3.1 cast) 2403
[15.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 2.9s
[17.7] - (mage0) fireball (3.1 cast) **3649**
[17.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 4.0s
[18.4] - (mage1) fireball (3.1 cast) **3606**
[19.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 2.74s
[20.8] - (mage0) fireball (3.1 cast) **3562**
[21.5] - (mage1) fireball (3.1 cast) 2453
[21.7] - (mage0) (5) ignite tick 2802 ticks remaining 1 time left 3.1s
[23.7] - (mage0) (5) ignite tick 2802 ticks remaining 0 time left 1.1s
[23.9] - (mage0) fireball (3.1 cast) 2269
[24.6] - (mage1) fireball (3.1 cast) 2295
[24.8] - (mage0) Ignite dropped
```

For multiple iterations:

``` python
from turtlewow_sim.env import Environment
from turtlewow_sim.mage import Mage
from turtlewow_sim.simulation import Simulation
from turtlewow_sim.specs import FireMageTalents

mages = []
num_mages = 5

for i in range(num_mages):
    fm = Mage(name=f'mage{i}', sp=1009, crit=33.17, hit=16, tal=FireMageTalents())
    fm.smart_scorch()
    mages.append(fm)

sim = Simulation(env=Environment, mages=mages)
sim.run(iterations=1000, duration=180)
sim.detailed_report()
```

After the simulation finishes the result will look like this:

```
Total spell dmg                         : 765822
Total dot dmg                           : 275181
Total Ignite dmg                        : 275181
Total dmg                               : 275181
Average mage dps                        : 1169
Average >=1 stack ignite uptime         : 90.6%
Average >=3 stack ignite uptime         : 76.1%
Average   5 stack ignite uptime         : 63.1%
Average ignite tick                     : 3437
```

but you can run with the `detailed_report()` method to get a more detailed output

## Talents and Debuffs

You can customize each character by passing additional arguments. The full constructor looks like this:
```
    class Character:
    def __init__(self,
                 tal: MageTalents,
                 env: Optional[Environment] = None,
                 name: str = '',
                 sp: int = 0,
                 crit: float = 0,
                 hit: float = 0,
                 haste: float = 0,
                 lag: float = 0.1,  # default lag between spells that seems to occur on turtle
                 opts: MageOptions = MageOptions(),
                 ):
```                 

There are premade talent configurations for each spec:
```
@dataclass(kw_only=True)
class FireMageTalents(MageTalents):
    imp_scorch: bool = True,
    critial_mass: bool = False,  # this is usually included in character's crit chance already
    fire_power: bool = True,
    fire_blast_cooldown: float = 8,


@dataclass(kw_only=True)
class ApFrostMageTalents(MageTalents):
    arcane_instability: bool = True,
    piercing_ice: bool = True,


@dataclass(kw_only=True)
class WcFrostMageTalents(MageTalents):
    winters_chill: bool = True,
    piercing_ice: bool = True
```

Every simulation assumes Curse of Elements is applied, you can turn it off by adding this line after you create your env
```
env.debuffs.coe = False
```
or by passing it as an argument in Simulation
```
sim = Simulation(env=Environment, coe=False)
```
no consumables are assumed otherwise, you need to factor those in your total sp/crit

You can also enable permanent nightfall proc using 
```
sim = Simulation(env=Environment, nightfall=True)
```

## Rotations
All rotations include a random initial delay of 0-2 seconds. You can disable this by passing the delay=0 parameter

Some currently supported rotations are:


* spam_scorch()

* spam_fireballs()

* spam_frostbolts()

1 scorch + 9 fireballs (repeated)
* one_scorch_then_fireballs()  

 1 scorch + 1 pyro + 6 fireballs (repeated)
* one_scorch_one_pyro_then_fb() 

1 scorch + 1 frostbolt + 8 fireballs (repeated)
* one_scorch_one_frostbolt_then_fb()  

 cast scorch if less than 5 imp.scorch stacks 
 else cast fireball
* smart_scorch()  


You can pass as arguments to each rotation when you want each mage to attempt
to activate their cooldowns. For example `mage1.one_scorch_one_pyro_then_fb(cds=CooldownUsages(arcane_power=5, power_infusion=6, mqg=7))
` will tell the first mage to attempt to activate arcane_power at 5 seconds, power_infusion at 6 seconds and mqg at 7 seconds.

Available cooldowns are:
```
class CooldownUsages:
    combustion: Optional[float] = None
    arcane_power: Optional[float] = None
    power_infusion: Optional[float] = None
    presence_of_mind: Optional[float] = None
    toep: Optional[float] = None
    mqg: Optional[float] = None
    berserking30: Optional[float] = None
    berserking20: Optional[float] = None
    berserking10: Optional[float] = None
```
