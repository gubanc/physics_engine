import random
import pygame
import pygame_gui
from enum import Enum

import Physics2D
from RigidBody import *
import math

global running, screen


class SpawnObject(Enum):
    NONE = -1
    CIRCLE = 0
    TRIANGLE = 1
    SQUARE = 2
    PENTAGON = 3
    HEXAGON = 4


material_dict = {
    "Wood": Material(0.1, 0.5, 0.4, 0.3, (205, 127, 50)),
    "Steel": Material(0.05, 0.5, 0.4, 0.3, (150, 150, 150)),
    "Rubber": Material(0.005, 0.5, 0.4, 0.75, (50, 50, 100)),
    "Clay": Material(0.01, 0.6, 0.5, 0.05, (255, 127, 100)),
    "Aerogel": Material(0.001, 0.3, 0.2, 0.3, (200, 200, 255)),
    "Tungsten": Material(0.1, 0.6, 0.5, 0.3, (200, 255, 200)),
    "Silicone": Material(0.01, 0.8, 0.6, 0.3, (200, 200, 200)),
    "Ice": Material(0.01, 0.1, 0.05, 0.3, (150, 150, 255)),
    "Static": Material(0, 0.2, 0.5, 0.6, (255, 255, 255))
}

gravity_dict = {
    "Earth": 1000,
    "Moon": 166,
    "Jupiter": 2500,
    "Space": 0,
    "Sun": 28000
}


pygame.init()
pygame.display.set_caption('Physics Engine')
clock = pygame.time.Clock()
fps = 120
delta_time = 1/fps
screen = pygame.display.set_mode((1500, 1000))
manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()), theme_path="physics_engine_theme.json")
x_addition = (screen.get_width() - screen.get_height()) / 2

#polygon = RigidBody(Polygon(300, 300, [[0, -25], [-25, 25], [25, 25]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 0)
#polygon2 = RigidBody(Polygon(250, 225, [[50, -25], [-50, -25], [0, 25]]), (255, 255, 255), 10, 1)
#circle = RigidBody(Circle(600, 225, 5), (255, 255, 255), 10, .5)
#objects.append(polygon)
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
#objects.append(RigidBody(Polygon(300, 100, [[-25, -25], [-25, 25], [25, 25], [25, -25]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
#objects.append(RigidBody(Polygon(350, 500, [[-25, -50], [-50, 0], [-25, 50], [25, 50], [50, 0], [25, -50]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
#objects.append(RigidBody(Polygon(350, 500, [[-25, -50], [-50, 0], [-25, 50], [25, 50], [50, 0]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
#objects.append(RigidBody(Polygon(450, 500, [[-25, -50], [-50, 0], [-25, 50], [25, 50]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 60))
#objects.append(RigidBody(Polygon(400, 1000, [[-370, -25], [-370, 25], [370, 25], [370, -25]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(450, 500, [[-370, 250], [370, 250], [-370, 25]]), Material(0, 0.2, 0.1, 1, (255, 255, 255)), 0))
#objects.append(RigidBody(Polygon(0, 500, [[-25, -600], [-25, 600], [25, 600], [25, -600]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(1000, 500, [[-25, -600], [-25, 600], [25, 600], [25, -600]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(800, 450, [[-25, -300], [-25, 300], [25, 300], [25, -300]]), (255, 255, 255), 0, 0.5))
#objects.append(RigidBody(Polygon(500, 100, [[31.5, -16.051], [-5.531, -34.92], [-34.92, -5.531], [-16.051, 31.5], [25, 25]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), math.pi / 20))
#objects.append(RigidBody(Polygon(500, 100, [[0, -25], [-23.7764, -7.7254], [-14.69463, 20.225325], [14.69463, 20.225325], [23.7764, -7.7254]]), Material(0.01, 0.2, 0.1, 0.5, (255, 255, 255)), 0))

objects.append(RigidBody(Polygon(500, 1000, [[-500, -100], [-500, 100], [500, 100], [500, -100]]), Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
objects.append(RigidBody(Polygon(0, screen.get_height()/2, [[-2.5, -screen.get_height()/2], [-2.5, screen.get_height()/2], [2.5, screen.get_height()/2], [2.5, -screen.get_height()/2]]), Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
objects.append(RigidBody(Polygon(screen.get_height(), screen.get_height()/2, [[-2.5, -screen.get_height()/2], [-2.5, screen.get_height()/2], [2.5, screen.get_height()/2], [2.5, -screen.get_height()/2]]), Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))

selected_object = SpawnObject.NONE
circle_button = pygame_gui.elements.UIButton(pygame.Rect((25, 25), (100, 100)), '', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#circle_button'))
triangle_button = pygame_gui.elements.UIButton(pygame.Rect((125, 25), (100, 100)), '', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#triangle_button'))
square_button = pygame_gui.elements.UIButton(pygame.Rect((25, 125), (100, 100)), '', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#square_button'))
pentagon_button = pygame_gui.elements.UIButton(pygame.Rect((125, 125), (100, 100)), '', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#pentagon_button'))

collision_colour_enabled = False
collision_colour_button = pygame_gui.elements.UIButton(pygame.Rect((1275, 100), (30, 30)), '', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#collision_colour_button_disabled'))
collision_colour_label = pygame_gui.elements.UILabel(pygame.Rect((1300, 102.5), (150, 25)), 'Coloured collisions', manager)

size_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((1275, 150), (150, 25)), 10, (1, 50), manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#size_slider'))
size_slider_label = pygame_gui.elements.UILabel(pygame.Rect((1375, 150), (150, 25)), 'Size', manager)

material_dropdown = pygame_gui.elements.UIDropDownMenu(["Wood", "Steel", "Rubber", "Clay", "Aerogel", "Tungsten", "Silicone", "Ice", "Static"], "Wood", pygame.Rect((1275, 200), (150, 25)), manager)
print(material_dropdown.selected_option[0])

orientation_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((1275, 250), (125, 25)), 0, (0, math.pi * 2), manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#size_slider'))
orientation_slider_label = pygame_gui.elements.UILabel(pygame.Rect((1375, 250), (150, 25)), 'Orientation', manager)

gravity_dropdown = pygame_gui.elements.UIDropDownMenu(["Earth", "Moon", "Jupiter", "Space", "Sun"], "Earth", pygame.Rect((1275, 300), (150, 25)), manager)

reset_button = pygame_gui.elements.UIButton(pygame.Rect((1275, 25), (100, 50)), 'Reset', manager, object_id=pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#reset_button'))


def handle_object_spawning(obj: SpawnObject):
    global x_addition
    size = size_slider.current_value / 10
    orientation = orientation_slider.current_value
    material = material_dict[material_dropdown.selected_option[0]]
    pos = pygame.mouse.get_pos()

    if obj == SpawnObject.CIRCLE:
        objects.append(RigidBody(Circle(pos[0] - x_addition, pos[1], size * 25),
                                 material, orientation))
    elif obj == SpawnObject.SQUARE:
        objects.append(RigidBody(Polygon(pos[0] - x_addition, pos[1], [[size * -25, size * -25], [size * -25, size * 25], [size * 25, size * 25], [size * 25, size * -25]]),
                                 material, orientation))
    elif obj == SpawnObject.TRIANGLE:
        objects.append(RigidBody(Polygon(pos[0] - x_addition, pos[1], [[0, size * -25], [size * -25, size * 25], [size * 25, size * 25]]),
                                 material, orientation))
    elif obj == SpawnObject.PENTAGON:
        objects.append(RigidBody(Polygon(pos[0] - x_addition, pos[1],
                                         [[0, size * -25], [size * -23.7764, size * -7.7254], [size * -14.69463, size * 20.225325], [size * 14.69463, size * 20.225325],
                                          [size * 23.7764, size * -7.7254]]), material, orientation))


def main():
    global running, selected_object, collision_colour_enabled
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == circle_button:
                    selected_object = SpawnObject.CIRCLE
                elif event.ui_element == triangle_button:
                    selected_object = SpawnObject.TRIANGLE
                elif event.ui_element == square_button:
                    selected_object = SpawnObject.SQUARE
                elif event.ui_element == pentagon_button:
                    selected_object = SpawnObject.PENTAGON
                elif event.ui_element == collision_colour_button:
                    if not collision_colour_enabled:
                        collision_colour_enabled = True
                        collision_colour_button.change_object_id(pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#collision_colour_button_enabled'))
                    else:
                        collision_colour_enabled = False
                        collision_colour_button.change_object_id(pygame_gui.core.ObjectID(class_id='@spawn_buttons', object_id='#collision_colour_button_disabled'))
                elif event.ui_element == reset_button:
                    objects.clear()
                    objects.append(RigidBody(Polygon(500, 1000, [[-500, -100], [-500, 100], [500, 100], [500, -100]]), Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
                    objects.append(RigidBody(Polygon(0, screen.get_height() / 2,
                                                     [[-2.5, -screen.get_height() / 2], [-2.5, screen.get_height() / 2],
                                                      [2.5, screen.get_height() / 2], [2.5, -screen.get_height() / 2]]),
                                             Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
                    objects.append(RigidBody(Polygon(screen.get_height(), screen.get_height() / 2,
                                                     [[-2.5, -screen.get_height() / 2], [-2.5, screen.get_height() / 2],
                                                      [2.5, screen.get_height() / 2], [2.5, -screen.get_height() / 2]]),
                                             Material(0, 0.2, 0.1, 0.5, (255, 255, 255)), 0))
            elif event.type == pygame.MOUSEBUTTONDOWN and x_addition < pygame.mouse.get_pos()[
                0] < screen.get_height() + x_addition:
                handle_object_spawning(selected_object)
            manager.process_events(event)
        manager.update(delta_time)
        screen.fill((0, 0, 0))
        RigidBody.gravity_scale = gravity_dict[gravity_dropdown.selected_option[0]]
        Physics2D.generate_manifolds(objects)
        for obj in objects:
            obj.update(screen, delta_time, collision_colour_enabled)
        manager.draw_ui(screen)
        pygame.draw.line(screen, (255, 255, 255), (x_addition, 0), (x_addition, screen.get_height()), 5)
        pygame.draw.line(screen, (255, 255, 255), (screen.get_height() + x_addition, 0), (screen.get_height() + x_addition, screen.get_height()), 5)
        pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, screen.get_height()), 10)
        pygame.draw.line(screen, (255, 255, 255), (0, 0), (screen.get_width(), 0), 10)
        pygame.draw.line(screen, (255, 255, 255), (screen.get_width(), screen.get_height()), (0, screen.get_height()), 10)
        pygame.draw.line(screen, (255, 255, 255), (screen.get_width(), screen.get_height()), (screen.get_width(), 0), 10)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()

