import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Inputs
battery = ctrl.Antecedent(np.arange(0, 101, 1), 'battery')
usage = ctrl.Antecedent(np.arange(0, 3, 1), 'usage')  # 0=Idle,1=Study,2=Gaming
time = ctrl.Antecedent(np.arange(0, 24, 1), 'time')

# Output
mode = ctrl.Consequent(np.arange(0, 101, 1), 'mode')

# Membership functions
battery['low'] = fuzz.trimf(battery.universe, [0, 0, 40])
battery['medium'] = fuzz.trimf(battery.universe, [30, 50, 70])
battery['high'] = fuzz.trimf(battery.universe, [60, 100, 100])

usage['idle'] = fuzz.trimf(usage.universe, [0, 0, 1])
usage['study'] = fuzz.trimf(usage.universe, [0, 1, 2])
usage['gaming'] = fuzz.trimf(usage.universe, [1, 2, 2])

time['day'] = fuzz.trimf(time.universe, [6, 12, 18])
time['night'] = fuzz.trimf(time.universe, [18, 23, 24])

mode['normal'] = fuzz.trimf(mode.universe, [0, 0, 40])
mode['power'] = fuzz.trimf(mode.universe, [30, 50, 70])
mode['ultra'] = fuzz.trimf(mode.universe, [60, 100, 100])

# Rules (important part)
rule1 = ctrl.Rule(battery['low'] & usage['gaming'], mode['ultra'])
rule2 = ctrl.Rule(battery['low'] & usage['study'], mode['power'])
rule3 = ctrl.Rule(battery['medium'] & usage['gaming'], mode['power'])
rule4 = ctrl.Rule(battery['high'], mode['normal'])
rule5 = ctrl.Rule(battery['low'] & time['night'], mode['ultra'])
rule6 = ctrl.Rule(battery['medium'] & usage['idle'], mode['normal'])
rule7 = ctrl.Rule(battery['medium'] & time['day'], mode['normal'])

# System
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,rule6,rule7])
sim = ctrl.ControlSystemSimulation(system)

# Take input from user
b = int(input("Enter Battery Level (0-100): "))
u = int(input("Enter Usage (0=Idle,1=Study,2=Gaming): "))
t = int(input("Enter Time (0-23): "))

sim.input['battery'] = b
sim.input['usage'] = u
sim.input['time'] = t

sim.compute()

print("\nBattery Mode Output:", sim.output['mode'])

# Interpretation
if sim.output['mode'] < 40:
    print("Mode: Normal")
elif sim.output['mode'] < 70:
    print("Mode: Power Saver")
else:
    print("Mode: Ultra Saver")

battery.view()
usage.view()
time.view()
mode.view()

import matplotlib.pyplot as plt
plt.show()