import math

# from RigidBody import *
import RigidBody
from RigidBody import Manifold, Vector

manifolds = []


def pythagorean_solve(a, b):
    return math.sqrt(a*a + b*b)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def cross_vectors(v1, v2):
    return v1.x * v2.y - v1.y * v2.x


def cross_scalar(scalar, v):
    return Vector(-scalar * v.y, scalar * v.x)


def generate_manifolds(objects):
    global manifolds

    manifolds.clear()
    for i in range(len(objects)):
        body_a = objects[i]
        if body_a.colliding:
            body_a.colliding = False
        for j in range(i + 1, len(objects)):
            body_b = objects[j]
            if not (body_a.inv_mass == 0 and body_b.inv_mass == 0):
                manifolds.append(Manifold(body_a, body_b))

    for manifold in manifolds:
        handle_collisions(manifold)


def handle_collisions(manifold):
    colliding = False
    if type(manifold.object_a.shape).__name__ == "Polygon" and type(manifold.object_b.shape).__name__ == "Polygon":
        colliding = polygon_v_polygon(manifold.object_a, manifold.object_b, manifold) and polygon_v_polygon(
            manifold.object_b, manifold.object_a, manifold)
    elif type(manifold.object_a.shape).__name__ == "Circle" and type(manifold.object_b.shape).__name__ == "Polygon":
        colliding = circle_v_polygon(manifold.object_a, manifold.object_b, manifold)
    elif type(manifold.object_a.shape).__name__ == "Polygon" and type(manifold.object_b.shape).__name__ == "Circle":
        colliding = polygon_v_circle(manifold.object_a, manifold.object_b, manifold)
    elif type(manifold.object_a.shape).__name__ == "Circle" and type(manifold.object_b.shape).__name__ == "Circle":
        colliding = circle_v_circle(manifold.object_a, manifold.object_b, manifold)
    if colliding:
        manifold.object_a.colliding = True
        manifold.object_b.colliding = True
        resolve_collision(manifold)
    return colliding


def resolve_collision(manifold):
    for i in range(len(manifold.contacts)):
        normalised_collision_normal = manifold.collision_normal.normalise()

        r_a = manifold.contacts[i] - manifold.object_a.position
        r_b = manifold.contacts[i] - manifold.object_b.position

        v_rel = manifold.object_b.velocity + cross_scalar(manifold.object_b.angular_velocity, r_b) - manifold.object_a.velocity - cross_scalar(manifold.object_a.angular_velocity, r_a)

        vel_along_normal = dot(v_rel, normalised_collision_normal)
        if vel_along_normal > 0:
            return

        cross_a = cross_vectors(r_a, normalised_collision_normal)
        cross_b = cross_vectors(r_b, normalised_collision_normal)
        inverse_sum = manifold.object_a.inv_mass + manifold.object_b.inv_mass + cross_a * cross_a * manifold.object_a.inv_inertia + cross_b * cross_b * manifold.object_b.inv_inertia

        impulse_magnitude = (-(1 + manifold.restitution) * dot(v_rel, normalised_collision_normal)) / inverse_sum
        impulse = normalised_collision_normal.multiply(impulse_magnitude)

        manifold.object_a.velocity -= impulse.multiply(manifold.object_a.inv_mass)
        manifold.object_a.angular_velocity -= manifold.object_a.inv_inertia * cross_vectors(r_a, impulse)
        manifold.object_b.velocity += impulse.multiply(manifold.object_b.inv_mass)
        manifold.object_b.angular_velocity += manifold.object_b.inv_inertia * cross_vectors(r_b, impulse)

        positional_correction(manifold, normalised_collision_normal)

        v_rel = manifold.object_b.velocity + cross_scalar(manifold.object_b.angular_velocity, r_b) - manifold.object_a.velocity - cross_scalar(manifold.object_a.angular_velocity, r_a)
        tangent = (v_rel - normalised_collision_normal.multiply(dot(v_rel, normalised_collision_normal))).normalise()
        cross_a = cross_vectors(r_a, tangent)
        cross_b = cross_vectors(r_b, tangent)
        inverse_sum = manifold.object_a.inv_mass + manifold.object_b.inv_mass + cross_a * cross_a * manifold.object_a.inv_inertia + cross_b * cross_b * manifold.object_b.inv_inertia
        friction_magnitude = -dot(v_rel, tangent) / inverse_sum

        static_mu = (manifold.object_a.static_friction + manifold.object_b.static_friction) / 2
        if math.fabs(friction_magnitude) < impulse_magnitude * static_mu:
            friction_impulse = tangent.multiply(friction_magnitude)
        else:
            dynamic_mu = (manifold.object_a.dynamic_friction + manifold.object_b.dynamic_friction) / 2
            friction_impulse = tangent.multiply(-impulse_magnitude * dynamic_mu)

        manifold.object_a.velocity -= friction_impulse.multiply(manifold.object_a.inv_mass)
        manifold.object_a.angular_velocity -= manifold.object_a.inv_inertia * cross_vectors(r_a, friction_impulse)
        manifold.object_b.velocity += friction_impulse.multiply(manifold.object_b.inv_mass)
        manifold.object_b.angular_velocity += manifold.object_b.inv_inertia * cross_vectors(r_b, friction_impulse)


def positional_correction(manifold, normalised_collision_normal):
    percent = 0.4
    slop = 0.05
    correction = normalised_collision_normal.multiply((max(manifold.penetration_depth - slop, 0.0) / (
                manifold.object_a.inv_mass + manifold.object_b.inv_mass)) * percent)
    manifold.object_a.position -= correction.multiply(manifold.object_a.inv_mass)
    manifold.object_b.position += correction.multiply(manifold.object_b.inv_mass)


def find_axis_least_penetration(body1, body2, manifold):
    best_separation = -math.inf
    best_index = -1

    for i in range(len(body1.shape.vector_vertices)):
        j = (i + 1) % len(body1.shape.vector_vertices)
        normal = (body1.shape.vector_vertices[i] - body1.shape.vector_vertices[j]).perpendicular().normalise()
        support_body2 = body2.shape.get_support_point(-normal)
        separation = dot(normal, support_body2 - body1.shape.vector_vertices[j])

        if separation > best_separation:
            best_separation = separation
            best_index = i
            manifold.collision_normal = normal

    return best_separation


def polygon_v_polygon(body1, body2, manifold):
    penetration_a = find_axis_least_penetration(body1, body2, manifold)
    if penetration_a >= 0:
        return False
    penetration_b = find_axis_least_penetration(body2, body1, manifold)
    if penetration_b >= 0:
        return False

    manifold.penetration_depth = -min(penetration_a, penetration_b)
    return True


def polygon_v_circle(polygon, circle, manifold):
    separation = math.inf
    normal_of_col = None
    v1 = None
    v2 = None

    center = polygon.shape.rotation_matrix.transpose().vector_multiply(circle.position - polygon.position)

    for i in range(len(polygon.shape.vertices)):
        normal = polygon.shape.normals[i]
        s = dot(normal, center - polygon.shape.vertices[i])
        if s + circle.shape.radius < 0:
            return False
        if s < separation:
            separation = s
            normal_of_col = normal
            v1 = polygon.shape.vertices[i]
            v2 = polygon.shape.vertices[(i+1) % len(polygon.shape.vertices)]

    if separation > 0:
        manifold.collision_normal = -polygon.shape.rotation_matrix.vector_multiply(normal_of_col)
        manifold.penetration_depth = circle.shape.radius
        manifold.contacts.append(manifold.collision_normal.multiply(circle.shape.radius) + circle.position)
        return True

    dot1 = dot(center - v1, v2 - v1)
    dot2 = dot(center - v2, v1 - v2)
    manifold.penetration_depth = circle.shape.radius + separation

    if dot1 <= 0:
        if (center - v1).get_length_squared() > circle.shape.radius * circle.shape.radius:
            return False
        normal_of_col = polygon.shape.rotation_matrix.vector_multiply(center - v1).normalise()
        manifold.collision_normal = normal_of_col
        manifold.contacts.append(polygon.shape.rotation_matrix.vector_multiply(v1) + polygon.position)
        return True
    elif dot2 <= 0:
        if (center - v2).get_length_squared() > circle.shape.radius * circle.shape.radius:
            return False
        normal_of_col = polygon.shape.rotation_matrix.vector_multiply(center - v2).normalise()
        manifold.collision_normal = normal_of_col
        manifold.contacts.append(polygon.shape.rotation_matrix.vector_multiply(v2) + polygon.position)
        return True
    else:
        if dot(center - v1, normal_of_col) > circle.shape.radius:
            return False
        manifold.collision_normal = -polygon.shape.rotation_matrix.vector_multiply(normal_of_col)
        manifold.contacts.append(manifold.collision_normal.multiply(circle.shape.radius) + circle.position)
        return True


def circle_v_polygon(circle, polygon, manifold):
    colliding = polygon_v_circle(polygon, circle, manifold)
    manifold.collision_normal = -manifold.collision_normal
    return colliding


def circle_v_circle(body1, body2, manifold):
    radius_sum = body1.shape.radius + body2.shape.radius
    distance_squared = (body2.position - body1.position).get_length_squared()
    if distance_squared <= (radius_sum * radius_sum):
        distance = math.sqrt(distance_squared)

        if distance == 0:
            manifold.collision_normal = Vector(1, 0)
            manifold.penetration_depth = body1.shape.radius
            manifold.contacts.append(body1.position)
        else:
            manifold.collision_normal = (body2.position - body1.position).multiply(1/distance)
            manifold.penetration_depth = radius_sum - distance
            manifold.contacts.append(manifold.collision_normal.multiply(body1.shape.radius) + body1.position)
        return True
    else:
        return False
