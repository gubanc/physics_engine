import math

import pygame.draw

import Physics2D

objects = []


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_length_squared(self):
        return self.x * self.x + self.y * self.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def multiply(self, const):
        return Vector(self.x * const, self.y * const)

    def perpendicular(self):
        return Vector(self.y, -self.x)

    def normalise(self):
        try:
            length = math.sqrt(self.get_length_squared())
            return Vector(self.x / length, self.y / length)
        except:
            return Vector(0, 0)

    def __neg__(self):
        return Vector(-self.x, -self.y)


class Mat2x2:
    def __init__(self, a, b, c, d):
        self.x_column = Vector(a, c)
        self.y_column = Vector(b, d)

    def vector_multiply(self, vector):
        return Vector(vector.x * self.x_column.x + vector.y * self.y_column.x, vector.x * self.x_column.y + vector.y * self.y_column.y)

    def transpose(self):
        return Mat2x2(self.x_column.x, self.x_column.y, self.y_column.x, self.y_column.y)


class RotationMat2x2(Mat2x2):
    def __init__(self, orientation):
        Mat2x2.__init__(self, math.cos(orientation), -math.sin(orientation), math.sin(orientation), math.cos(orientation))


class Manifold:
    def __init__(self, object_a, object_b):
        self.object_a = object_a
        self.object_b = object_b
        self.collision_normal = Vector(0, 0)
        self.penetration_depth = 0
        self.restitution = min(object_a.restitution, object_b.restitution)
        self.contacts = []

    def print(self):
        print(self.object_a.id, "with", self.object_b.id)


class Shape:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def render(self, screen, colour, new_pos, new_orientation):
        pass

    def calculate_area(self):
        pass


class Polygon(Shape):
    def __init__(self, center_x, center_y, vertices: list[list]):
        Shape.__init__(self, center_x, center_y)
        self.vertices = []
        self.vertices_world_space: list[list] = []
        self.vector_vertices: list[Vector] = []
        self.rotation_matrix = RotationMat2x2(0)
        self.normals = []

        for i in range(len(vertices)):
            self.vertices.append(Vector(vertices[i][0], vertices[i][1]))
            self.vertices_world_space.append([self.vertices[i].x + center_x, self.vertices[i].y + center_y])
            self.vector_vertices.append(Vector(self.vertices_world_space[i][0], self.vertices_world_space[i][1]))

        self.generate_normals()

    def render(self, screen, colour, new_pos, new_orientation):
        self.center_x = new_pos.x
        self.center_y = new_pos.y
        self.rotation_matrix = RotationMat2x2(new_orientation)

        for i in range(len(self.vertices)):
            new_vertex = self.rotation_matrix.vector_multiply(self.vertices[i]) + Vector(self.center_x, self.center_y)
            self.vertices_world_space[i] = [new_vertex.x, new_vertex.y]
            self.vector_vertices[i] = new_vertex

        pygame.draw.polygon(surface=screen, color=colour, points=self.vertices_world_space)

    def calculate_area(self):
        area = 0
        for i in range(len(self.vector_vertices)):
            j = (i + 1) % len(self.vertices)
            area += Physics2D.cross_vectors(self.vector_vertices[i], self.vector_vertices[j])
        return abs(area) / 2

    def get_support_point(self, direction: Vector):
        best_projection = -math.inf
        best_vertex = None

        for i in range(len(self.vector_vertices)):
            v = self.vector_vertices[i]
            projection = Physics2D.dot(v, direction)

            if projection > best_projection:
                best_vertex = v
                best_projection = projection

        return best_vertex

    def generate_normals(self):
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            self.normals.append((self.vertices[j] - self.vertices[i]).perpendicular().normalise())


class Circle(Shape):
    def __init__(self, center_x, center_y, radius):
        Shape.__init__(self, center_x, center_y)
        self.radius = radius

    def render(self, screen, colour, new_pos, new_orientation):
        self.center_x = new_pos.x
        self.center_y = new_pos.y

        pygame.draw.circle(screen, colour, (self.center_x, self.center_y), self.radius)

    def calculate_area(self):
        return math.pi * self.radius * self.radius


class RigidBody:
    gravity_scale = 1000

    def __init__(self, shape: Shape, colour, mass, restitution, static_friction, dynamic_friction, orientation, inertia):
        self.shape = shape
        self.position = Vector(shape.center_x, shape.center_y)
        self.mass = mass
        if mass == 0:
            self.inv_mass = 0
        else:
            self.inv_mass = 1 / mass
        self.inertia = inertia
        if inertia == 0:
            self.inv_inertia = 0
        else:
            self.inv_inertia = 1 / inertia
        self.restitution = restitution
        self.resultant_force = Vector(0, self.gravity_scale * self.mass)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.orientation = orientation
        self.torque = 0
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.colour = colour
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.id = len(objects)
        self.colliding = False

    def update(self, screen, dt):
        self.acceleration = self.resultant_force.multiply(self.inv_mass)
        self.velocity += self.acceleration.multiply(dt)
        self.position += self.velocity.multiply(dt)

        self.angular_velocity += self.torque * self.inv_inertia * dt
        self.orientation += self.angular_velocity * dt

        self.constrain(screen)

        if self.colliding:
            self.colour = (0, 150, 0)
        else:
            self.colour = (150, 0, 0)

        self.shape.render(screen, self.colour, self.position, self.orientation)

    def constrain(self, screen):
        if self.position.y > screen.get_height():
            self.position.y = screen.get_height()
            self.velocity.y *= -1
        elif self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -1
        if self.position.x > screen.get_width():
            self.position.x = screen.get_width()
            self.velocity.x *= -1
        elif self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -1
