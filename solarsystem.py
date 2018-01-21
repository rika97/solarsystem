G = 6.6741 * 10**(-11)
t = 0
sun = {
    'mass': 1.9886 * 10**30,
    'x': 0,
    'y': 0,
    'z': 0,
    'vx': 0,
    'vy': 0,
    'vz': 0,
}
earth = {
    'mass': 5.9722 * 10**24,
    'x': sun['x'] + 1.496 * 10**11,
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 2.9786 * 10**4,
    'vz': sun['vz'],
}


def print_status():
    print("Time:", t)
    print(
        "  Earth position:",
        earth['x'],
        earth['y'],
        earth['z'],
    )
    print(
        "  Sun position:",
        sun['x'],
        sun['y'],
        sun['z'],
    )


def do_step(duration):
    global t
    for planet in [earth, sun]:
        for dimension in ['x', 'y', 'z']:
            planet[dimension] += planet['v' + dimension] * duration
    cubed_distance = ((sun['x'] - earth['x'])**2 + (sun['y'] - earth['y'])**2 +
                      (sun['z'] - earth['z'])**2)**(3 / 2)
    for dimension in ['x', 'y', 'z']:
        force = G * sun['mass'] * earth['mass'] / cubed_distance * (
            sun[dimension] - earth[dimension])
        for sign, planet in [(1, earth), (-1, sun)]:
            acceleration = sign * force / planet['mass']
            planet['v' + dimension] += acceleration * duration
    t += duration
    return


dur = float(input("Enter duration: "))
steps = int(input("Enter number of steps: "))

print_status()
while steps > 0:
    do_step(dur)
    print_status()
    steps -= 1
