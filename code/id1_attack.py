from constants import *

class Potion(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, speed=400, damage=10, world_x=1200, world_y=800):
        super().__init__()
        self.texture = arcade.load_texture("assets/resource_packs/gui/Spells/potion_attack.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage
        self.world_x = world_x
        self.world_y = world_y
        self.scale = 0.2
        
        # Рассчитываем направление
        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        # И скорость
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        # Если текстура ориентирована по умолчанию вправо, то поворачиваем пулю в сторону цели
        # Для другой ориентации нужно будет подправить угол
        self.angle = math.degrees(-angle)  # Поворачиваем пулю
        
    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > self.world_x or
            self.center_y < 0 or self.center_y > self.world_y):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.angle += 10
