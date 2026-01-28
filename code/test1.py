import time
import math
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
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.tiled_map = None

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        self.keys_pressed = set()

        # Новые переменные для отслеживания
        self.start_time = None
        self.chests_collected = 0
        self.total_chests = 0
        self.show_victory = False
        self.victory_time = None

        # Портал как белый круг
        self.portal_radius = 50  # Радиус портала
        self.portal_glow = 0  # Для анимации свечения
        self.portal_position = (0, 0)  # Позиция портала

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

        # Инициализируем таймер и счетчик сундуков
        self.start_time = time.time()
        self.total_chests = len(self.chests_list)
        self.chests_collected = 0
        self.show_victory = False
        self.victory_time = None
        self.portal_glow = 0

        print("Игра загружена! Используйте стрелки для движения.")

    def _load_map(self):
        """Загрузка карты из TMX файла"""
        map_name = "forest_map.tmx"

        # Список возможных путей
        possible_paths = [
            "assets/maps/forest_map1.tmx",
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

        # Ищем позицию портала (выхода)
        if self.exit_list and len(self.exit_list) > 0:
            portal_sprite = self.exit_list[0]
            self.portal_position = (portal_sprite.center_x, portal_sprite.center_y)
            print(f"Портал найден на позиции: x({portal_sprite.center_x}) y({portal_sprite.center_y})")
        else:
            # Если портала нет на карте, ставим в случайное место
            self.portal_position = (self.world_width // 2, self.world_height // 2)
            print(f"Портал установлен в центре: x({self.portal_position[0]}) y({self.portal_position[1]})")

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

        self.camera_shake.update_camera()
        self.world_camera.use()
        
        # Рисуем стены
        self.wall_list.draw()
        
        # Рисуем игрока
        self.player_list.draw()
        
        # Рисуем сундуки
        self.chests_list.draw()
        
        # Рисуем портал как белый круг с анимацией
        self._draw_portal()
        
        self.camera_shake.readjust_camera()

        self.gui_camera.use()

        # Рисуем UI
        self._draw_ui()

    def _draw_portal(self):
        """Отрисовка портала как белого круга с анимацией"""
        portal_x, portal_y = self.portal_position
        
        # Анимация пульсации
        glow_radius = self.portal_radius + math.sin(self.portal_glow) * 10
        
        # Внешнее свечение (полупрозрачное)
        arcade.draw_circle_filled(
            portal_x, portal_y,
            glow_radius + 15,
            (255, 255, 255, 80)  # Белый с прозрачностью
        )
        
        # Основной круг портала
        arcade.draw_circle_filled(
            portal_x, portal_y,
            glow_radius,
            arcade.color.WHITE
        )
        
        # Внутренний круг (эффект глубины)
        arcade.draw_circle_filled(
            portal_x, portal_y,
            glow_radius * 0.7,
            (230, 230, 255)  # Слегка голубоватый белый
        )
        
        # Яркое ядро портала
        arcade.draw_circle_filled(
            portal_x, portal_y,
            glow_radius * 0.4,
            (255, 255, 200)  # Теплый белый
        )
        
        # Контур портала
        arcade.draw_circle_outline(
            portal_x, portal_y,
            glow_radius + 5,
            arcade.color.LIGHT_BLUE,
            3
        )

    def _draw_ui(self):
        """Отрисовка интерфейса"""
        if not self.show_victory:
            # Информация об управлении
            self.a = arcade.Text(
                "Управление: Стрелки - движение, ESC - в лобби",
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
                f"Сундуков: {self.chests_collected}/{self.total_chests}",
                SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60,
                arcade.color.GOLD, 20
            )
            self.c.draw()
            
            # Таймер
            current_time = time.time() - self.start_time
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            self.d = arcade.Text(
                f"Время: {minutes:02d}:{seconds:02d}",
                SCREEN_WIDTH - 150, SCREEN_HEIGHT - 90,
                arcade.color.LIGHT_BLUE, 20
            )
            self.d.draw()
            
            # Подсказка о портале
            self.e = arcade.Text(
                "Дойдите до белого круга (портала) для завершения",
                SCREEN_WIDTH // 2, 30,
                arcade.color.LIGHT_YELLOW, 18,
                anchor_x="center"
            )
            self.e.draw()
        else:
            # Показываем окно победы поверх игры
            self._draw_victory_screen()

    def _draw_victory_screen(self):
        """Отрисовка окна победы"""
        # Полупрозрачный фон
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (0, 0, 0, 200)  # Черный с прозрачностью
        )
        
        # Рамка для статистики
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200,
            arcade.color.DARK_GREEN
        )
        
        # Отображаем сообщение о победе
        arcade.draw_text(
            "ВЫ ПОБЕДИЛИ!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            arcade.color.GOLD,
            50,
            anchor_x="center",
            bold=True
        )
        
        # Отображаем статистику
        arcade.draw_text(
            f"Собрано сундуков: {self.chests_collected}/{self.total_chests}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )
        
        # Отображаем время
        elapsed_time = self.victory_time - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        arcade.draw_text(
            f"Время: {minutes:02d}:{seconds:02d}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )
        
        # Инструкция для продолжения
        arcade.draw_text(
            "Нажмите ESC для возврата в лобби",
            SCREEN_WIDTH // 2,
            100,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center"
        )

    def on_update(self, delta_time):
        if self.show_victory:
            return  # Останавливаем игру при показе окна победы
            
        # Обновляем анимацию портала
        self.portal_glow += delta_time * 2  # Скорость пульсации
        
        self.camera_shake.update(delta_time)

        self.player_list.update(delta_time, self.keys_pressed)

        self.player_list.update_animation()

        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            0.15,
        )
        
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
            self.chests_collected += 1

        # Проверяем достижение портала (белого круга)
        portal_x, portal_y = self.portal_position
        distance_to_portal = math.sqrt(
            (self.player_sprite.center_x - portal_x) ** 2 +
            (self.player_sprite.center_y - portal_y) ** 2
        )
        
        # Если игрок находится в радиусе портала
        if distance_to_portal < self.portal_radius and not self.show_victory:
            print("Портал достигнут! Поздравляем с победой!")
            self.show_victory = True
            self.victory_time = time.time()

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if self.show_victory:
            # Управление в окне победы
            if key == arcade.key.ESCAPE:
                # Возврат в лобби
                from lobby import LobbyView  # Импортируем здесь, чтобы избежать циклических импортов
                lobby_view = LobbyView()
                self.window.show_view(lobby_view)
            return
            
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
            # Правильный полноэкранный режим
            if self.window.fullscreen:
                self.window.set_fullscreen(False)
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                self.window.set_fullscreen(True)
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        elif key == arcade.key.ESCAPE:
            # Возврат в лобби из игры
            from lobby import LobbyView
            lobby_view = LobbyView()
            self.window.show_view(lobby_view)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if self.show_victory:
            return
            
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