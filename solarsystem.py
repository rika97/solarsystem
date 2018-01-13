G = 6.6741 * 10**(-11)
t = 0
solar_mass = 1.9886 * 10**30
solar_x = 0
solar_y = 0
solar_z = 0
solar_vx = 0
solar_vy = 0
solar_vz = 0
earth_mass = 5.9722 * 10**24
earth_x = solar_x + 1.496 * 10**11
earth_y = solar_y
earth_z = solar_z
earth_vx = solar_vx
earth_vy = solar_vy + 2.9786 * 10**4
earth_vz = solar_vz


def print_status():
    print("Time:", t)
    print("  Earth position:", earth_x, earth_y, earth_z)
    print("  Sun position:", solar_x, solar_y, solar_z)


def do_step(duration):
    global solar_x, solar_y, solar_z, solar_vx, solar_vy, solar_vz
    global earth_x, earth_y, earth_z, earth_vx, earth_vy, earth_vz
    global t
    solar_x += solar_vx * duration
    solar_y += solar_vy * duration
    solar_z += solar_vz * duration
    earth_x += earth_vx * duration
    earth_y += earth_vy * duration
    earth_z += earth_vz * duration
    cubed_distance = ((solar_x - earth_x)**2 + (solar_y - earth_y)**2 +
                      (solar_z - earth_z)**2)**(3 / 2)
    force_x = G * solar_mass * earth_mass / cubed_distance * (
        solar_x - earth_x)
    earth_ax = force_x / earth_mass
    earth_vx += earth_ax * duration
    solar_ax = -force_x / solar_mass
    solar_vx += solar_ax * duration
    force_y = G * solar_mass * earth_mass / cubed_distance * (
        solar_y - earth_y)
    earth_ay = force_y / earth_mass
    earth_vy += earth_ay * duration
    solar_ay = -force_y / solar_mass
    solar_vy += solar_ay * duration
    force_z = G * solar_mass * earth_mass / cubed_distance * (
        solar_z - earth_z)
    earth_az = force_z / earth_mass
    earth_vz += earth_az * duration
    solar_az = -force_z / solar_mass
    solar_vz += solar_az * duration
    t += duration
    return


dur = float(input("Enter duration: "))
steps = int(input("Enter number of steps: "))

print_status()
while steps > 0:
    do_step(dur)
    print_status()
    steps -= 1
