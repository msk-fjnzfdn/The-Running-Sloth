from constants import *


class WEffect(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Основные характеристики
        self.scale = 0.4
        self.damage = 7

        # Загрузка текстур

        self.idle_texture_moving = []
        for i in range(1, 4):
            texture = arcade.load_texture(
                f"assets/resource_packs/default/alchimic/attack_effect/attack_effect_{i}.png")
            self.idle_texture_moving.append(texture)

        self.texture = arcade.load_texture("assets/resource_packs/default/alchimic/attack_effect/attack_effect_1.png")


        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.15  # секунд на кадр

        self.center_x = x
        self.center_y = y

        self.count = 0

    def update_animation(self, delta_time: float = 1/60):
        """
        Обновление анимации
        """
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.count += 1
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.idle_texture_moving):
                self.current_texture = 0
            self.texture = self.idle_texture_moving[self.current_texture]
        
   
    def update(self, delta_time):
        if self.count == 3:
            self.remove_from_sprite_lists()