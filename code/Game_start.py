from id1_character import *
from constants import *


class PlayView(arcade.View):
    def __init__(self, character_id=1):
        super().__init__()
        self.character_id = character_id

        # Списки спрайтов
        self.player_list = None
        self.wall_list = None
        self.chests_list = None
        self.exit_list = None
        self.collision_list = None
        self.background_list = None

        # Игрок
        self.player_sprite = None
        self.physics_engine = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,  # Трястись будет только то, что попадает в объектив мировой камеры
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.tiled_map = None

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        self.keys_pressed = set()

        self.setup()

    def setup(self):
        """Настройка игры"""
        # Создаём списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.chests_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # Загружаем карту
        self._load_map()

        print("Игра загружена! Используйте стрелки для движения.")

    def _load_map(self):
        """Загрузка карты из TMX файла"""
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
                self.tiled_map = arcade.load_tilemap(path, scaling=TILE_SCALING)
                print(f"Карта успешно загружена из: {path}")
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
            self.world_width = int(self.tiled_map.width * self.tiled_map.tile_width * TILE_SCALING)
            self.world_height = int(self.tiled_map.height * self.tiled_map.tile_height * TILE_SCALING)
            print(f"Границы мир: {self.world_width} x {self.world_height}")
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
        print(f"Координаты по умолчанию установлены: x({start_x}) y({start_y})")

        # Создаём игрока
        self._create_player(start_x, start_y)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
        self.player_sprite, self.collision_list
        )

    def _create_player(self, start_x, start_y):
        """Создание спрайта игрока"""
        self.player_sprite = Hero()
        self.player_sprite.center_x = start_x
        self.player_sprite.center_y = start_y
        self.player_list.append(self.player_sprite)

    def on_show_view(self):
        """Вызывается при показе View"""
        arcade.set_background_color(COLOR_BACKGROUND)
        print("Игровой экран показан")

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()


        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.world_camera.use()
        self.wall_list.draw()
        self.player_list.draw()
<<<<<<< HEAD
        #self.bomb_list.draw()
=======
>>>>>>> msk-fjnzfdn's-branch
        self.chests_list.draw()
        self.camera_shake.readjust_camera()

        self.gui_camera.use()

        # Рисуем UI
        self._draw_ui()

    def _draw_ui(self):
        """Отрисовка интерфейса"""
        # Информация об управлении
        self.a = arcade.Text(
            "Управление: Стрелки - движение, ESC - в лобби, E - использовать выход",
            10, SCREEN_HEIGHT - 30,
            arcade.color.LIGHT_GRAY, 16
        )
        self.a.draw()
        # Информация о персонаже
        character_names = {1: "Зориан", 2: "???", 3: "???"}
        character_name = character_names.get(self.character_id, "Неизвестный")

        self.b = arcade.Text(
            f"Персонаж: {character_name}",
            10, SCREEN_HEIGHT - 60,
            arcade.color.WHITE, 20,
            bold=True
        )
        self.b.draw()
        # Счётчик сундуков
        self.c = arcade.Text(
            f"Сундуков: {len(self.chests_list)}",
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60,
            arcade.color.GOLD, 20
        )
        self.c.draw()
    def on_update(self, delta_time):
        self.camera_shake.update(delta_time)

        self.player_list.update(delta_time, self.keys_pressed)

        self.player_list.update_animation()

        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            0.15,  # Плавность следования камеры
        )
        
        """Обновление состояния каждый кадр"""
        # Обновляем движение игрока
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_sprite.speed
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_sprite.speed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.player_sprite.speed
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -self.player_sprite.speed

        # Обновляем физику
        if self.physics_engine:
            self.physics_engine.update()

        # Проверяем сбор сундуков
        chest_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.chests_list)
        for chest in chest_hit_list:
            print(f"Собран сундук на координатах: x({chest.center_x}) y({chest.center_y})")
            chest.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
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
        elif key == arcade.key.F11:
            # Полноэкранный режим
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.E:
            # Проверяем, достиг ли игрок выхода
            exit_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.exit_list)
            if exit_hit_list:
                print("Выход достигнут!")
                # Здесь можно добавить переход на следующий уровень

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
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