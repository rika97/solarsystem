import pygame
from datetime import datetime

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Solar System Simulator")

canvas = pygame.Surface((screen_width, screen_height))
sidereal_year = 365.25636
tropical_year = 365.24219

G = 6.6741 * 10**(-11)
t = 1167882180
sun = {
    'mass': 1.9886 * 10**30,
    'radius': 695508000 / 5,
    'x': 0,
    'y': 0,
    'z': 0,
    'vx': 0,
    'vy': 0,
    'vz': 0,
}
mercury = {
    'mass': 3.3011 * 10**23,
    'radius': 2439700 * 10,
    'x': sun['x'] + 69816900000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 47362,  #not accurate
    'vz': sun['vz'],
}
venus = {
    'mass': 4.8675 * 10**24,
    'radius': 6051800 * 10,
    'x': sun['x'] + 108939000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 35020,  #not accurate
    'vz': sun['vz'],
}
earth = {
    'mass': 5.9722 * 10**24,
    'radius': 6371000 * 10,
    'x': sun['x'] + 147098291000,
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 30280,
    'vz': sun['vz'],
}
mars = {
    'mass': 6.4171 * 10**23,
    'radius': 3389500 * 10,
    'x': sun['x'] + 249200000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 24007,  #not accurate
    'vz': sun['vz'],
}
jupiter = {
    'mass': 1.8982 * 10**27,
    'radius': 69911000 * 10,
    'x': sun['x'] + 816620000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 13070,  #not accurate
    'vz': sun['vz'],
}
saturn = {
    'mass': 5.6834 * 10**26,
    'radius': 58232000 * 10,
    'x': sun['x'] + 1514500000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 9680,  #not accurate
    'vz': sun['vz'],
}
uranus = {
    'mass': 8.6810 * 10**25,
    'radius': 25362000 * 10,
    'x': sun['x'] + 3008410000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 6800,  #not accurate
    'vz': sun['vz'],
}
neptune = {
    'mass': 1.0243 * 10**26,
    'radius': 24622000 * 10,
    'x': sun['x'] + 4537300000000,  #not accurate
    'y': sun['y'],
    'z': sun['z'],
    'vx': sun['vx'],
    'vy': sun['vy'] + 5430,  #not accurate
    'vz': sun['vz'],
}
planets = [
    sun,
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune,
]
scale = 10**10


def print_status():
    dt = datetime.fromtimestamp(t)
    date_string = dt.strftime('%Y-%m-%d %H:%M:%S')
    print("\rTime: " + date_string, end='')
    # print(
    #     "  Earth position:",
    #     earth['x'],
    #     earth['y'],
    #     earth['z'],
    # )
    # print(
    #     "  Sun position:",
    #     sun['x'],
    #     sun['y'],
    #     sun['z'],
    # )


def do_step(duration):
    global t
    for planet in planets:
        for dimension in ['x', 'y', 'z']:
            planet[dimension] += planet['v' + dimension] * duration

    for i, planet_1 in enumerate(planets):
        for j in range(i):
            planet_2 = planets[j]

            cubed_distance = ((planet_1['x'] - planet_2['x'])**2 +
                              (planet_1['y'] - planet_2['y'])**2 +
                              (planet_1['z'] - planet_2['z'])**2)**(3 / 2)
            for dimension in ['x', 'y', 'z']:
                force = G * planet_1['mass'] * planet_2[
                    'mass'] / cubed_distance * (
                        planet_1[dimension] - planet_2[dimension])
                for sign, planet in [(-1, planet_1), (1, planet_2)]:
                    acceleration = sign * force / planet['mass']
                    planet['v' + dimension] += acceleration * duration
    t += duration
    render()
    return


def render():
    for planet in planets:
        pygame.draw.circle(canvas, (0, 150, 255),
                           (int(planet['x'] / scale + screen_width / 2),
                            int(planet['y'] / scale + screen_height / 2)),
                           int(1))
    screen.blit(canvas, (0, 0))
    for planet in planets:
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(planet['x'] / scale + screen_width / 2),
                            int(planet['y'] / scale + screen_height / 2)),
                           int(planet['radius'] / scale * 100))
    pygame.display.update()


dur = float(input("Enter duration: "))
steps = int(input("Enter number of steps: "))

print_status()

while steps > 0:
    do_step(dur)
    steps -= 1
    print_status()
