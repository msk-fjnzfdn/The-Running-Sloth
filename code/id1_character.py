from constants import *

class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1

class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        
        # Основные характеристики
        self.scale = 0.4
        self.speed = 5
        self.health = 25
        self.damage = 100
        
        # Загрузка текстур

        self.idle_texture_moving = []
        for i in range(1, 7):
            texture = arcade.load_texture(f"assets/resource_packs/default/alchimic/idle/Default_alchimic_idle_{i}.png")
            self.idle_texture_moving.append(texture)

        self.idle_texture = arcade.load_texture("assets/resource_packs/default/alchimic/static/Default_alchimic_png.png")
        
        self.texture = self.idle_texture
        
        self.walk_textures = []
        for i in range(1, 9):
            texture = arcade.load_texture(f"assets/resource_packs/default/alchimic/walk_run/Default_alchimic_walk_{i}.png")
            self.walk_textures.append(texture)
            
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
        
        self.is_walking = False # Никуда не идём
        self.face_direction = FaceDirection.RIGHT  # и смотрим вправо

        # Центрируем персонажа
        self.center_x = 1500
        self.center_y = 1500

    def update_animation(self, delta_time: float = 1/60):
        """ Обновление анимации """
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()

        else:
            self.texture_change_time += delta_time / 1.5
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_texture_moving):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.idle_texture_moving[self.current_texture]
                else:
                    self.texture = self.idle_texture_moving[self.current_texture].flip_horizontally()

       
    def update(self, delta_time, keys_pressed):
        """ Перемещение персонажа """
        # В зависимости от нажатых клавиш определяем направление движения
        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy
        # Поворачиваем персонажа в зависимости от направления движения
        # Если никуда не идём, то не меняем направление взгляда
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT


        # Проверка на движение
        self.is_walking = dx or dy