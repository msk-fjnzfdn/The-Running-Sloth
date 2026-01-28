from constants import *


class AEffect(arcade.Sprite):
    def __init__(self, x, y, face_direction=FaceDirection.RIGHT):
        super().__init__()

        # Основные характеристики
        self.scale = 0.3
        self.damage = 7

        # Загрузка текстур

        self.attack_texture_moving = []
        for i in range(1, 6):
            texture = arcade.load_texture(
                f"assets/resource_packs/default/alchimic/attack/alchimic_attack_{i}.png")
            self.attack_texture_moving.append(texture)

        self.texture = arcade.load_texture(
            "assets/resource_packs/default/alchimic/attack/alchimic_attack_1.png")

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.15  # секунд на кадр

        self.center_x = x
        self.center_y = y

        self.count = 0

        self.face_direction = face_direction

    def update_animation(self, delta_time: float = 1/60):
        """
        Обновление анимации
        """
        self.texture_change_time += delta_time * 3
        if self.texture_change_time >= self.texture_change_delay:
            self.count += 1
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.attack_texture_moving):
                self.current_texture = 0
            # Поворачиваем текстуру в зависимости от направления взгляда
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.attack_texture_moving[self.current_texture]
            else:
                self.texture = self.attack_texture_moving[self.current_texture].flip_horizontally(
                )

    def update(self, delta_time):
        if self.count == 5:
            self.remove_from_sprite_lists()
