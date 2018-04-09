class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __truediv__(self, scalar):
        return Vector(
            x=self.x / scalar,
            y=self.y / scalar,
            z=self.z / scalar,
        )

    def __mul__(self, scalar):
        return Vector(
            x=self.x * scalar,
            y=self.y * scalar,
            z=self.z * scalar,
        )

    def __rmul__(self, scalar):
        return self * scalar

    def __sub__(self, other):
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5


class Planet:
    def __init__(self, name, mass, radius, x, y, z, vx, vy, vz):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = Vector(x, y, z)
        self.velocity = Vector(vx, vy, vz)

    def copy(self):
        return Planet(
            name=self.name,
            mass=self.mass,
            radius=self.radius,
            x=self.position.x,
            y=self.position.y,
            z=self.position.z,
            vx=self.velocity.x,
            vy=self.velocity.y,
            vz=self.velocity.z,
        )
