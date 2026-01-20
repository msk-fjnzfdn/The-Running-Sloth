import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Running Sloth - Game"
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5

# Цвета для игры
COLOR_BACKGROUND = (20, 30, 40, 0)


class PlayView(arcade.View):
    def __init__(self, character_id=None):
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
        possible_paths = "code/forest_map.tmx"

        tiled_map = None

        tiled_map = arcade.load_tilemap(possible_paths, scaling=TILE_SCALING)
        print(f"Карта успешно загружена из: {possible_paths}")


        try:
            self.wall_list = tiled_map.sprite_lists["walls"]
            self.chests_list = tiled_map.sprite_lists["chest"]
            self.exit_list = tiled_map.sprite_lists["exit"]
            self.collision_list = tiled_map.sprite_lists["collision"]
        except KeyError as e:
            print(f"Ошибка: В карте TMX отсутствует слой {e}")

        # Ищем стартовую позицию игрока
        if "PlayerStart" in tiled_map.sprite_lists and tiled_map.sprite_lists["PlayerStart"]:
            start_pos = tiled_map.sprite_lists["PlayerStart"][0]
            start_x = start_pos.center_x
            start_y = start_pos.center_y
        else:
            # Стартовая позиция по умолчанию
            start_x = 100
            start_y = 100

        # Создаём игрока
        self._create_player(start_x, start_y)

        # Создаём физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
        self.player_sprite, self.collision_list
        )

    def _create_player(self, start_x, start_y):
        """Создание спрайта игрока"""
        try:
            # Пробуем разные пути к спрайту игрока
            possible_paths = [
                "assets/resource_packs/default/alchimic/НА.png",
                "НА.png",
                "assets/НА.png",
                "assets/resource_packs/default/alchimic/alchimic.png",
                "alchimic.png"
            ]

            sprite_loaded = False

            for path in possible_paths:
                try:
                    self.player_sprite = arcade.Sprite(path, scale=0.5)
                    sprite_loaded = True
                    print(f"Спрайт игрока успешно загружен из: {path}")
                    break
                except Exception:
                    continue

            if not sprite_loaded:
                colors = {
                    1: arcade.color.BLUE,
                    2: arcade.color.PINK,
                    3: arcade.color.GREEN
                }
                player_color = colors.get(self.character_id, arcade.color.RED)
                self.player_sprite = arcade.SpriteCircle(30, player_color)
                print("Картинка не найдена. Используется запасной цветной спрайт")

        except Exception as e:
            print(f"Критическая ошибка создания игрока: {e}")
            self.player_sprite = arcade.SpriteCircle(30, arcade.color.BLUE)

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

        # Рисуем задний фон (если есть)
        if self.background_list:
            self.background_list.draw()

        # Рисуем стены
        self.wall_list.draw()

        # Рисуем сундуки
        self.chests_list.draw()

        # Рисуем выход
        self.exit_list.draw()

        # Рисуем игрока
        self.player_list.draw()

        # Рисуем UI
        self._draw_ui()

    def _draw_ui(self):
        """Отрисовка интерфейса"""
        # Информация об управлении
        arcade.draw_text(
            "Управление: Стрелки - движение, ESC - в лобби, E - использовать выход",
            10, SCREEN_HEIGHT - 30,
            arcade.color.LIGHT_GRAY, 16
        )

        # Информация о персонаже
        character_names = {1: "Зориан", 2: "???", 3: "???"}
        character_name = character_names.get(self.character_id, "Неизвестный")

        arcade.draw_text(
            f"Персонаж: {character_name}",
            10, SCREEN_HEIGHT - 60,
            arcade.color.WHITE, 20,
            bold=True
        )

        # Счётчик сундуков
        arcade.draw_text(
            f"Сундуков: {len(self.chests_list)}",
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60,
            arcade.color.GOLD, 20
        )

    def on_update(self, delta_time):
        """Обновление состояния каждый кадр"""
        # Обновляем движение игрока
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Обновляем физику
        if self.physics_engine:
            self.physics_engine.update()

        # Проверяем сбор сундуков
        chest_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.chests_list)
        for chest in chest_hit_list:
            chest.remove_from_sprite_lists()
            print("Сундук собран!")

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
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
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_resize(self, width, height):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)