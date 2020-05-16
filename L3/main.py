import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


def applyOR(rules):
    val = rules[0]

    for i in range(len(rules)-1):
        val = np.fmax(val, rules[i+1])

    return val


def applyAND(rules):
    val = rules[0]

    for i in range(len(rules)-1):
        val = np.fmin(val, rules[i+1])

    return val


# Iejimo kintamieji
# reliatyvus greitis  (0-150) km/h
# atstumas iki masinos (0-200) m
# automobilio padangu su kelio danga trinties koeficientas (0.1-1)
x_speed = np.arange(0, 150, 1)
x_distance = np.arange(0, 200, 1)
x_friction = np.arange(0.1, 1.00, 0.01)
# Isejimo kintamieji:
# stabdziu jega (0%-100%)
x_brakes = np.arange(0, 100, 1)

speed_lo = fuzz.trimf(x_speed, [0, 20, 40])
speed_md = fuzz.trimf(x_speed, [30, 60, 90])
speed_hi = fuzz.trimf(x_speed, [80, 115, 150])
distance_lo = fuzz.trimf(x_distance, [0, 30, 60])
distance_md = fuzz.trimf(x_distance, [40, 75, 110])
distance_hi = fuzz.trimf(x_distance, [90, 145, 200])
friction_lo = fuzz.trimf(x_friction, [0.1, 0.1, 0.4])
friction_md = fuzz.trimf(x_friction, [0.3, 0.5, 0.7])
friction_hi = fuzz.trapmf(x_friction, [0.55, 0.85, 1, 1])

brakes_lo = fuzz.trimf(x_brakes, [0, 0, 35])
brakes_md = fuzz.trimf(x_brakes, [25, 50, 75])
brakes_hi = fuzz.trimf(x_brakes, [65, 100, 100])

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_speed, speed_lo, 'b', linewidth=1.5, label='Mazas')
ax0.plot(x_speed, speed_md, 'g', linewidth=1.5, label='Vidutinis')
ax0.plot(x_speed, speed_hi, 'r', linewidth=1.5, label='Didelis')
ax0.set_title('Reliatyvus greitis')
ax0.legend()

ax1.plot(x_distance, distance_lo, 'b', linewidth=1.5, label='Mazas')
ax1.plot(x_distance, distance_md, 'g', linewidth=1.5, label='Vidutinis')
ax1.plot(x_distance, distance_hi, 'r', linewidth=1.5, label='Didelis')
ax1.set_title('Atstumas iki objekto')
ax1.legend()

ax2.plot(x_friction, friction_lo, 'b', linewidth=1.5, label='Mazas')
ax2.plot(x_friction, friction_md, 'g', linewidth=1.5, label='Vidutinis')
ax2.plot(x_friction, friction_hi, 'r', linewidth=1.5, label='Didelis')
ax2.set_title('Trinties koeficientas')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

speed = 10
distance = 50
friction = 0.6
speed_level_lo = fuzz.interp_membership(x_speed, speed_lo, speed)
speed_level_md = fuzz.interp_membership(x_speed, speed_md, speed)
speed_level_hi = fuzz.interp_membership(x_speed, speed_hi, speed)

distance_level_lo = fuzz.interp_membership(x_distance, distance_lo, distance)
distance_level_md = fuzz.interp_membership(x_distance, distance_md, distance)
distance_level_hi = fuzz.interp_membership(x_distance, distance_hi, distance)

friction_level_lo = fuzz.interp_membership(x_friction, friction_lo, friction)
friction_level_md = fuzz.interp_membership(x_friction, friction_md, friction)
friction_level_hi = fuzz.interp_membership(x_friction, friction_hi, friction)

rules_lo, rules_md, rules_hi = ([] for i in range(3))

rules_lo.append(
    applyAND([speed_level_lo, distance_level_hi]))
rules_lo.append(
    friction_level_lo)
rules_lo.append(
    applyAND([speed_level_lo, distance_level_md, friction_level_hi]))
rules_lo.append(
    applyAND([speed_level_hi, 1 - distance_level_lo, friction_level_hi]))
print(speed_level_hi, 1 - distance_level_lo, friction_level_hi)
brakes_activation_lo = applyAND([applyOR(rules_lo), brakes_lo])

rules_md.append(
    applyAND([speed_level_lo, distance_level_lo]))
rules_md.append(
    applyAND([speed_level_md, distance_level_md]))
rules_md.append(
    applyAND([speed_level_hi, distance_level_hi]))
rules_md.append(
    applyAND([speed_level_lo, distance_level_md, friction_level_md]))
rules_md.append(
    applyAND([speed_level_md, distance_level_lo, friction_level_hi]))
rules_md.append(
    applyAND([speed_level_hi, distance_level_md, friction_level_md]))

brakes_activation_md = applyAND([applyOR(rules_md), brakes_md])

rules_hi.append(
    applyAND([speed_level_hi, distance_level_lo]))
rules_hi.append(
    applyAND([speed_level_md, distance_level_lo, friction_level_md]))

brakes_activation_hi = applyAND([applyOR(rules_hi), brakes_hi])

aggregated = applyOR(
    [brakes_activation_lo, brakes_activation_md, brakes_activation_hi])

brakes = fuzz.defuzz(x_brakes, aggregated, 'mom')
print(brakes)

brakes0 = np.zeros_like(x_brakes)

fig, ax3 = plt.subplots(figsize=(8, 3))

ax3.fill_between(x_brakes, brakes0, brakes_activation_lo,
                 facecolor='b', alpha=0.7)
ax3.plot(x_brakes, brakes_lo, 'b', linewidth=0.5, linestyle='--', )
ax3.fill_between(x_brakes, brakes0, brakes_activation_md,
                 facecolor='g', alpha=0.7)
ax3.plot(x_brakes, brakes_md, 'g', linewidth=0.5, linestyle='--')
ax3.fill_between(x_brakes, brakes0, brakes_activation_hi,
                 facecolor='r', alpha=0.7)
ax3.plot(x_brakes, brakes_hi, 'r', linewidth=0.5, linestyle='--')
ax3.set_title('Stabdziu jega')

for ax in (ax3,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
# plt.show()
