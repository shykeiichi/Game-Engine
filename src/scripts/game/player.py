import pygame, math
from src.scripts.modules.entity import *
from .bullet import bullet_shooty_thingy
from src.scripts.modules.gui import * 

class player_movement_component:
    def __init__(self, game, parent) -> None:
        self.game = game
        self.parent = parent

    def update(self):
        move_speed = 300 * self.game.delta_time
        if self.game.input.is_pressed("a"):
            self.parent.transform.x -= move_speed
        if self.game.input.is_pressed("d"):
            self.parent.transform.x += move_speed
        if self.game.input.is_pressed("w"):
            self.parent.transform.y-= move_speed
        if self.game.input.is_pressed("s"):
            self.parent.transform.y += move_speed

    def render(self):
        pass

class player_renderer_component:
    def __init__(self, game, parent) -> None:
        self.game = game
        self.parent = parent

        self.image = self.game.image.load("player.png")

    def update(self):
        pass
    
    def render(self):
        image = pygame.transform.scale(self.image, (64, 64))
        img, rect = self.game.math.rotate_center(image, 0, self.parent.transform.x, self.parent.transform.y)
        self.game.renderer.screen.blit(img, rect)

class enemy_renderer_component:
    def __init__(self, game, parent) -> None:
        self.game = game
        self.parent = parent

        self.image = self.game.image.load("enemy.png")

    def update(self):
        pass
    
    def render(self):
        if self.parent.health > 0:
            image = pygame.transform.scale(self.image, (88, 88))
            img, rect = self.game.math.rotate_center(image, 0, self.parent.transform.x, self.parent.transform.y)
            self.game.renderer.screen.blit(img, rect)

class player_health_system:
    def __init__(self, game, parent) -> None:
        self.game = game
        self.parent = parent

        self.parent.health = 10
        self.cant_get_hit_by = []

        self.health_bar_rect = gui_rect(game)
        self.health_bar_rect.set_y_constraint(percentage_constraint(0.02))
        self.health_bar_rect.set_x_constraint(percentage_constraint(0.67))
        self.health_bar_rect.set_width_constraint(percentage_constraint(0.3))
        self.health_bar_rect.set_height_constraint(pixel_constraint(5))
        self.health_bar_rect.set_border_radius(10)
        self.health_bar_rect.set_draw_color(self.game.color_handler.get_rgb('player.health_bar'))

    def update(self):
        self.health_bar_rect.tween_size(percentage_constraint(0.3 - (0.03 * (10 - self.parent.health))), pixel_constraint(5), 24)
        self.health_bar_rect.update()
    
    def render(self):
        self.health_bar_rect.render()

class Player(Entity):
    def __init__(self, game) -> None:
        self.game = game

        self.game.player = self

        self.components = []

        self.transform = Transform()
        self.transform.y = 500

        self.add_component(bullet_shooty_thingy(game, self))
        self.add_component(player_health_system(game, self))
        self.add_component(player_movement_component(game, self))
        self.add_component(player_renderer_component(game, self))
