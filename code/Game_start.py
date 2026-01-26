from id1_character import *
from id1_attack import *
from enemy import *
from constants import *
from wave_effect import *


class PlayView(arcade.View):
    def __init__(self, character_id=1, obj=None):
        super().__init__()

        self.parent = obj

        self.character_id = character_id

        # Списки спрайтов
        self.player_list = None
        self.wall_list = None
        self.chests_list = None
        self.exit_list = None
        self.collision_list = None
        self.background_list = None
        self.potion_list = None
        self.effect_list = None

        # Игрок
        self.player_sprite = None
        self.physics_engine = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.can_attack = True

        # Шкала здоровья
        self.hp_bar = []
        for i in range(6):
            hp_sprite = arcade.Sprite(
                f"assets/resource_packs/gui/HP_bar/HP_Bar_{i}.png", center_x=240, center_y=self.window.height - 50, scale=0.6)
            self.hp_bar.append(hp_sprite)

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            # Трястись будет только то, что попадает в объектив мировой камеры
            self.world_camera.view_data,
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.shoot_cooldown = 1

        self.tiled_map = None

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        self.keys_pressed = set()

        self.setup()

    def setup(self):
        """
        Настройка игры
        """
        # Создаём списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.chests_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.potion_list = arcade.SpriteList()
        self.effect_list = arcade.SpriteList()

        # Загружаем карту
        self._load_map()

    def _load_map(self):
        """
        Загрузка карты из TMX файла
        """
        map_name = "forest_map.tmx"

        # Список возможных путей
        possible_paths = [
            "assets/maps/forest_map.tmx",
            "assets/pictures/forest_map.tmx",
            map_name,
            f"pictures/{map_name}",
            f"assets/pictures/{map_name}",
            f"assets/{map_name}",
            "forest_map.tmx",
            "maps/forest_map.tmx",
            "code/forest_map.tmx"
        ]

        for path in possible_paths:
            try:
                self.tiled_map = arcade.load_tilemap(
                    path, scaling=TILE_SCALING)
                break
            except Exception:
                print("❗Ошибка загрузки карты")

        try:
            self.wall_list = self.tiled_map.sprite_lists["walls"]
            self.chests_list = self.tiled_map.sprite_lists["chest"]
            self.exit_list = self.tiled_map.sprite_lists["exit"]
            self.collision_list = self.tiled_map.sprite_lists["collision"]
        except KeyError as e:
            print(f"❗Ошибка: В карте TMX отсутствует слой {e}")

        try:
            self.world_width = int(
                self.tiled_map.width * self.tiled_map.tile_width * TILE_SCALING)
            self.world_height = int(
                self.tiled_map.height * self.tiled_map.tile_height * TILE_SCALING)
        except Exception as e:
            print(f"❗Ошибка загрузки границ карты: {e}")

        # Ищем стартовую позицию игрока
        if "PlayerStart" in self.tiled_map.sprite_lists and self.tiled_map.sprite_lists["PlayerStart"]:
            start_pos = self.tiled_map.sprite_lists["PlayerStart"][0]
            start_x = start_pos.center_x
            start_y = start_pos.center_y
        else:
            start_x = 1500
            start_y = 1500

        # Создаём игрока
        self._create_player(start_x, start_y)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def _create_player(self, start_x, start_y):
        """
        Создание спрайта игрока
        """
        self.player_sprite = Hero()
        self.player_sprite.center_x = start_x
        self.player_sprite.center_y = start_y
        self.player_list.append(self.player_sprite)

    def on_show_view(self):
        """
        Вызывается при показе View
        """
        arcade.set_background_color(COLOR_BACKGROUND)

    def on_draw(self):
        """
        Отрисовка игры
        """
        self.clear()

        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.world_camera.use()
        self.wall_list.draw()
        self.player_list.draw()
        self.chests_list.draw()
        self.effect_list.draw()
        self.potion_list.draw()
        self.camera_shake.readjust_camera()

        self.gui_camera.use()

        # Рисуем UI
        self._draw_ui()

    def _draw_ui(self):
        """
        Отрисовка интерфейса
        """
        arcade.draw_sprite(self.hp_bar[self.player_sprite.health // 1])
        self.hp_percent = arcade.Text(
            f"{int(self.player_sprite.health / 5 * 100)}%",
            140, self.window.height - 46,
            arcade.color.BLACK, 16
        )
        self.hp_percent.draw()

    def on_update(self, delta_time):
        self.camera_shake.update(delta_time)

        self.player_list.update(delta_time, self.keys_pressed)

        self.effect_list.update()

        self.potion_list.update()

        self.player_list.update_animation()

        self.effect_list.update_animation()

        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            0.15,  # Плавность следования камеры
        )

        # Обновляем движение игрока
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_sprite.speed * delta_time
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_sprite.speed * delta_time
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.player_sprite.speed * delta_time
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -self.player_sprite.speed * delta_time

        # Обновляем физику
        if self.physics_engine:
            self.physics_engine.update()

        # Проверяем сбор сундуков
        chest_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.chests_list)
        for chest in chest_hit_list:
            chest.remove_from_sprite_lists()

        for potion in self.potion_list:
            # Проверяем столкновение с одним спрайтом
            hit_list = arcade.check_for_collision_with_list(
                potion, self.collision_list)
            if hit_list:
                wave = WEffect(x=potion.center_x, y=potion.center_y)
                self.effect_list.append(wave)
                potion.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """
        Обработка нажатия клавиш
        """
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
            self.keys_pressed.add(key)
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True
            self.keys_pressed.add(key)
        elif key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
            self.keys_pressed.add(key)
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
            self.keys_pressed.add(key)
        elif key == arcade.key.Q:
            self.player_sprite.health = self.player_sprite.health - \
                1 if self.player_sprite.health - 1 >= 0 else 0
            print(f"Здоровье: {self.player_sprite.health}")
        elif key == arcade.key.F11:
            # Полноэкранный режим
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.E:
            # Проверяем, достиг ли игрок выхода
            exit_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.exit_list)
            if exit_hit_list:
                pass
                # Здесь можно добавить переход на следующий уровень
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.parent)

    def on_key_release(self, key, modifiers):
        """
        Обработка отпускания клавиш
        """
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)
        elif key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.can_attack:
            self.create_potion(x, y)
            self.can_attack = False
            arcade.schedule(self.attack_ready, self.shoot_cooldown)

    def create_potion(self, x, y):
        world_x = self.world_camera.position[0] - \
            (self.window.width / 2) + x
        world_y = self.world_camera.position[1] - \
            (self.window.height / 2) + y
        potion = Potion(
            self.player_sprite.center_x,
            self.player_sprite.center_y - 45,
            world_x,
            world_y, world_y=self.world_height, world_x=self.world_width
        )
        self.potion_list.append(potion)
        # Проигрываем звук выстрела
        # arcade.play_sound(self.shoot_sound)

    def attack_ready(self, delta_time):
        self.can_attack = True
        arcade.unschedule(self.attack_ready)
