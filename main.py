import random

import pygame
import Physics2D
from RigidBody import *
import math

global running, screen

pygame.init()
clock = pygame.time.Clock()
fps = 120
delta_time = 1/fps
screen = pygame.display.set_mode((1000, 1000))
polygon = RigidBody(Polygon(400, 225, [[50, -25], [-50, -25], [0, 25]]), (255, 255, 255), 10, 0.5, 0.2, 0.1, 0, 1)
#polygon2 = RigidBody(Polygon(250, 225, [[50, -25], [-50, -25], [0, 25]]), (255, 255, 255), 10, 1)
#circle = RigidBody(Circle(600, 225, 5), (255, 255, 255), 10, .5)
objects.append(polygon)
#objects.append(polygon2)
#objects.append(circle)
#objects.append(RigidBody(Circle(200, 200, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(100, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(50, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(400, 225, 20), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(500, 225, 30), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(25, 200, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(75, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(125, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(150, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(175, 225, 15), (255, 255, 255), 20, 1))
#objects.append(RigidBody(Circle(400, 1000, 700), (255, 255, 255), 0, 1))
#objects.append(RigidBody(Circle(0, 200, 180), (255, 255, 255), 0, 1))
#objects.append(RigidBody(Circle(800, 200, 180), (255, 255, 255), 0, 1))
objects.append(RigidBody(Polygon(450, 500, [[-25, -25], [-25, 25], [25, 25], [25, -25]]), (255, 255, 255), 10, 0.5, 0.2, 0.1, 0, 100))
#objects.append(RigidBody(Polygon(400, 1000, [[-370, -25], [-370, 25], [370, 25], [370, -25]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(500, 1000, [[-500, -100], [-500, 100], [500, 100], [500, -100]]), (255, 255, 255), 0, 0.5, 0.2, 0.1, 0, 0))
#objects.append(RigidBody(Polygon(400, 450, [[-370, 250], [370, 250], [-370, 25]]), (255, 255, 255), 0, 0.2))
#objects.append(RigidBody(Polygon(0, 500, [[-25, -600], [-25, 600], [25, 600], [25, -600]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(1000, 500, [[-25, -600], [-25, 600], [25, 600], [25, -600]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(800, 450, [[-25, -300], [-25, 300], [25, 300], [25, -300]]), (255, 255, 255), 0, 0.5))


def main():
    global running
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                objects.append(RigidBody(Circle(pos[0], pos[1], random.randint(5,50)), (255, 255, 255), random.randint(5, 50), 1, 0.2, 0.1, 0, 10))
            elif event.type == pygame.KEYDOWN:
                pos = pygame.mouse.get_pos()
                objects.append(
                    RigidBody(Polygon(pos[0], pos[1], [[-25, -25], [-25, 25], [25, 25], [25, -25]]), (255, 255, 255), 10, 0.5,
                              0.2, 0.1, 0, 100))
        screen.fill((0, 0, 0))
        Physics2D.generate_manifolds(objects)
        for obj in objects:
            obj.update(screen, delta_time)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
