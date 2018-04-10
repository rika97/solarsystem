import pygame
from datetime import datetime
from collections import deque
from functools import partial
from planet import Planet

sidereal_year = 365.25636
tropical_year = 365.24219
music = {
    'jupiter': 'music/jupiter.ogg',
}

G = 6.6741 * 10**(-11)
t = 0
sun = Planet(
    name='Sun',
    mass=1.9886 * 10**30,
    radius=695508000 / 5,
    x=6.442860875172776e8,
    y=2.748913433991132e8,
    z=-9.109887801915727e6,
    vx=-3.151184859677259,
    vy=9.185194654328578,
    vz=3.355974894379355e-2,
)
mercury = Planet(
    name='Mercury',
    mass=3.3011 * 10**23,
    radius=2439700 * 10,
    x=3.901558897485410e10,
    y=2.904514484583830e10,
    z=-1.184916870002620e9,
    vx=-3.879081706909912e4,
    vy=4.110223749127960e4,
    vz=6.918492572855968e3,
)
venus = Planet(
    name='Venus',
    mass=4.8675 * 10**24,
    radius=6051800 * 10,
    x=-4.733027208737938e9,
    y=-1.083207490477231e11,
    z=-1.173858328641228e9,
    vx=3.473833166185593e4,
    vy=-1.856561942705289e3,
    vz=-2.031472118202770e3,
)
earth = Planet(
    name='Earth',
    mass=5.9722 * 10**24,
    radius=6371000 * 10,
    x=-2.636314250687937e10,
    y=1.448755934863529e11,
    z=5.775629234984517e5,
    vx=-2.977359332571185e4,
    vy=-5.558856867535258e3,
    vz=4.295648228174187e-1,
)
mars = Planet(
    name='Mars',
    mass=6.4171 * 10**23,
    radius=3389500 * 10,
    x=1.990267404151246e11,
    y=7.450413194711113e10,
    z=-3.343950327278871e9,
    vx=-7.560777278212286e3,
    vy=2.477045044227772e4,
    vz=7.047794087480170e2,
)
jupiter = Planet(
    name='Jupiter',
    mass=1.8982 * 10**27,
    radius=69911000 * 10,
    x=-7.490058923208621e11,
    y=-3.198963469147586e11,
    z=1.810247444226952e10,
    vx=4.979372429276186e3,
    vy=-1.140864402759292e4,
    vz=-6.463117944665164e1,
)
saturn = Planet(
    name='Saturn',
    mass=5.6834 * 10**26,
    radius=58232000 * 10,
    x=1.083450373301071e12,
    y=8.513589642487608e11,
    z=-5.794398668223530e10,
    vx=-6.490272475844968e3,
    vy=7.575137300943099e3,
    vz=1.254753987994750e2,
)
uranus = Planet(
    name='Uranus',
    mass=8.6810 * 10**25,
    radius=25362000 * 10,
    x=-2.723971684699241e12,
    y=-2.891270404270630e11,
    z=3.427913027050830e10,
    vx=6.680837052485776e2,
    vy=-7.089916083324308e3,
    vz=-3.525223272928191e1,
)
neptune = Planet(
    name='Neptune',
    mass=1.0243 * 10**26,
    radius=24622000 * 10,
    x=-2.327426565170483e12,
    y=-3.890812806779972e12,
    z=1.337348733534796e11,
    vx=4.630808049977051e3,
    vy=-2.758234623717188e3,
    vz=-4.954053085827870e1,
)
camera = {
    'x': 0,
    'y': 0,
    'z': 0,
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
location = deque(maxlen=15000)
selected_planet = earth
pygame.font.init()
title_font = pygame.font.Font("font/star.ttf", 20)
label_font = pygame.font.Font("font/menlo.ttc", 20)


def print_status():
    dt = datetime.fromtimestamp(t)
    date_string = dt.strftime('%Y-%m-%d %H:%M:%S')
    text_image = label_font.render(date_string, True, (255, 255, 255))
    screen.blit(text_image, (550, 580))
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
        planet.position += planet.velocity * duration

    for i, planet_1 in enumerate(planets):
        for j in range(i):
            planet_2 = planets[j]

            cubed_distance = (
                planet_1.position - planet_2.position).magnitude()**3
            force = G * planet_1.mass * planet_2.mass / cubed_distance * (
                planet_1.position - planet_2.position)
            for sign, planet in [(-1, planet_1), (1, planet_2)]:
                acceleration = sign * force / planet.mass
                planet.velocity += acceleration * duration
    t += duration
    render()
    get_input()
    return


screen_positions = {}


def distance_to_click(x, y, planet):
    u, v, r = screen_positions[planet]
    return ((x - u)**2 + (y - v)**2)**0.5 - r


def render():
    redraw_orbits()
    for planet in planets:
        # pygame.draw.circle(
        #     canvas, (0, 150, 255),
        #     (int((planet['x'] - camera['x']) / scale + screen_width / 2),
        #      int((planet['y'] - camera['y']) / scale + screen_height / 2)),
        #     int(1))
        location.append(planet.copy())
    screen.blit(canvas, (0, 0))
    for planet in planets:
        x = int((planet.position.x - camera['x']) / scale + screen_width / 2)
        y = int((planet.position.y - camera['y']) / scale + screen_height / 2)
        r = int(planet.radius / scale * 100)
        screen_positions[planet] = (x, y, r)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), r)
        if planet is selected_planet:
            pygame.draw.circle(screen, (0, 200, 255), (x, y),
                               max(r + 5, int(r * 1.5)), 1)
    print_status()
    pygame.display.update()


keys_pressed = {}


def get_input():
    global scale, selected_planet
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                scale *= 1.1
                redraw_orbits()
            elif event.button == 5:
                scale /= 1.1
                redraw_orbits()
            elif event.button == 1:
                x, y = event.pos
                distance_fn = partial(distance_to_click, x, y)
                closest = min(planets, key=distance_fn)
                if distance_fn(closest) < 20:
                    selected_planet = closest
                    print(selected_planet.name)
                else:
                    selected_planet = None

    if keys_pressed.get(pygame.K_MINUS, False):
        scale *= 1.1
        redraw_orbits()
    if keys_pressed.get(pygame.K_EQUALS, False):
        scale /= 1.1
        redraw_orbits()
    if keys_pressed.get(pygame.K_DOWN, False):
        camera['y'] += 10 * scale
        redraw_orbits()
    if keys_pressed.get(pygame.K_UP, False):
        camera['y'] -= 10 * scale
        redraw_orbits()
    if keys_pressed.get(pygame.K_RIGHT, False):
        camera['x'] += 10 * scale
        redraw_orbits()
    if keys_pressed.get(pygame.K_LEFT, False):
        camera['x'] -= 10 * scale
        redraw_orbits()


def redraw_orbits():
    canvas.fill((0, 0, 0))
    m = len(location)
    for i, planet in enumerate(location):
        pygame.draw.circle(
            canvas, (0, 150 * i / m, 255 * i / m),
            (int((planet.position.x - camera['x']) / scale + screen_width / 2),
             int((planet.position.y - camera['y']) / scale + screen_height / 2)
             ), int(1))


dur = float(input("Enter duration: "))
steps = int(input("Enter number of steps: "))

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Solar System Simulator")
canvas = pygame.Surface((screen_width, screen_height))

pygame.mixer.init()
sound = pygame.mixer.Sound(music['jupiter'])
sound.play()

pygame.display.set_icon(pygame.image.load('images/icon.jpg'))

print_status()
print('\n----\n')

while steps > 0:
    do_step(dur)
    steps -= 1
