from id1_character import *
from id1_attack import *
from enemy import *
from constants import *
from wave_effect import *
from id1_attack_effect import *


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
        self.enemy_spawn_list = None

        # Игрок
        self.player_sprite = None
        self.physics_engine = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.can_attack = True

        # Экран смерти
        self.is_dead = False

        # Шкала здоровья
        self.hp_bar = []
        for i in range(6):
            hp_sprite = arcade.Sprite(
                f"assets/resource_packs/gui/HP_bar/HP_Bar_{i}.png",
                center_x=240,
                center_y=self.window.height - 50,
                scale=0.6
            )
            self.hp_bar.append(hp_sprite)

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.shoot_cooldown = 0.75
        self.level = 1
        self.last_level = 2
        self.tiled_map = None
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        self.keys_pressed = set()

        self.potion_cd = arcade.Sprite("assets/resource_packs/gui/Spells/potion_attack.png", center_x=34,
                                       center_y=self.window.height - 80,
                                       scale=0.2)

        # Новые переменные для отслеживания
        self.start_time = None
        self.chests_collected = 0
        self.total_chests = 0
        self.monster_collected = 0
        self.show_victory = False
        self.pause = False
        self.victory_time = None
        self.E_pressed = False
        self.immortality = False
        self.hp_lvl = 0
        self.music_volume = self.window.user_settings["music_volume"]
        self.music_player = None
        self.win_the_game = False

        self.portal_radius = 50  # Радиус портала
        self.portal_glow = 0  # Для анимации свечения
        self.portal_position = (0, 0)  # Позиция портала

        self.win_sound = None
        self.death_sound = None
        self.monster_attack_sound = None
        self.player_attack_sound = None
        self.player_lose_hp_sound = None
        self.escape_sound = None

        self.setup()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.world_camera.match_window()
        self.gui_camera.match_window()

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
        self.enemy_spawn_list = arcade.SpriteList()

        # Сбрасываем состояние смерти
        self.is_dead = False
        self.show_victory = False
        self.win_the_game = True if self.level == self.last_level else False

        try:
            self.win_sound = arcade.load_sound("assets/music/win_sound.mp3")
            self.death_sound = arcade.load_sound(
                "assets/music/death_sound.mp3")
            self.monster_attack_sound = arcade.load_sound("assets/music/monster_attack_sound.mp3")
            self.player_attack_sound = arcade.load_sound("assets/music/player_attack_sound.mp3")
            self.player_lose_hp_sound = None
            self.escape_sound = arcade.load_sound("assets/music/idk_sound.mp3")
        except Exception as e:
            print(f"❗Ошибка загрузки звуков игры: {e}")

        # Загружаем карту
        self._load_map()

        self._setup_music()

        # Инициализируем таймер и счетчик сундуков
        self.start_time = time.time()
        self.total_chests = len(self.chests_list)
        self.chests_collected = 0
        self.monster_collected = 0
        self.show_victory = False
        self.victory_time = None
        self.portal_glow = 0

    def _load_map(self):
        """
        Загрузка карты из TMX файла
        """

        map_name = f"forest_map{self.level}.tmx"

        possible_paths = [
            f"assets/maps/{map_name}",
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

        if "PlayerStart" in self.tiled_map.sprite_lists and self.tiled_map.sprite_lists["PlayerStart"]:
            start_pos = self.tiled_map.sprite_lists["PlayerStart"][0]
            start_x = start_pos.center_x
            start_y = start_pos.center_y
        else:
            start_x = 1500
            start_y = 1500

        if "exit" in self.tiled_map.sprite_lists and self.tiled_map.sprite_lists["exit"]:
            portal_sprite = self.exit_list[0]
            self.portal_position = (
                portal_sprite.center_x, portal_sprite.center_y)
        else:
            self.portal_position = (
                self.world_width // 2, self.world_height // 2)

        self.total_chests = len(self.chests_list)

        self._create_player(start_x, start_y, self.hp_lvl)
        self._create_enemies()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def _create_player(self, start_x, start_y, hp_lvl=0):
        """
        Создание спрайта игрока
        """
        self.player_sprite = Hero()
        self.player_sprite.health -= hp_lvl
        self.player_sprite.center_x = start_x
        self.player_sprite.center_y = start_y
        self.player_list.append(self.player_sprite)

    def _create_enemies(self):
        for enemy_spawn in self.tiled_map.sprite_lists["EnemyStart"]:
            monster = Enemy(x=enemy_spawn.center_x, y=enemy_spawn.center_y)
            self.enemy_spawn_list.append(monster)

    def _draw_portal(self):
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

        self.camera_shake.update_camera()
        self.world_camera.use()
        self.wall_list.draw()
        self._draw_portal()
        self.player_list.draw()
        self.chests_list.draw()
        self.enemy_spawn_list.draw()
        self.effect_list.draw()
        self.potion_list.draw()
        self.camera_shake.readjust_camera()

        # GUI камера - для интерфейса поверх всего
        self.gui_camera.use()
        self.gui_camera.position = (
            self.window.width / 2, self.window.height / 2)

        # Рисуем HP бар всегда (даже при смерти)
        self._draw_ui()

    def _draw_ui(self):
        """
        Отрисовка интерфейса
        """
        hp_index = min(int(self.player_sprite.health), 5)
        arcade.draw_sprite(self.hp_bar[hp_index])

        self.hp_percent = arcade.Text(
            f"{self.player_sprite.health} / 5",
            140,
            self.window.height - 46,
            arcade.color.BLACK,
            16,
            font_name="Comic"
        )
        self.hp_percent.draw()
        arcade.draw_sprite(self.potion_cd)

        current_time = time.time() - self.start_time
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        self.game_timer = arcade.Text(
            f"Время: {minutes:02d}:{seconds:02d}",
            0, self.window.height - 150,
            arcade.color.LIGHT_BLUE, 20
        )
        self.game_timer.draw()
        if self.show_victory:
            if self.win_the_game:
                self._draw_victory_screen(text="ПОЗДРАВЛЯЕМ, ВЫ ПРОШЛИ ИГРУ!")
            else:
                self._draw_victory_screen()
        elif self.is_dead:
            self._draw_death_screen()
        elif self.pause:
            self._draw_pause_screen()

    def _draw_victory_screen(self, text="ВЫ ПРОШЛИ УРОВЕНЬ!"):
        """Отрисовка окна победы"""
        # Полупрозрачный фон
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.window.width // 2,
                self.window.height // 2,
                self.window.width,
                self.window.height
            ),
            (0, 175, 0, 150)  # Красный с прозрачностью
        )

        # Отображаем сообщение о победе
        win = arcade.Text(
            f"{text}",
            self.width // 2,
            self.height - 150,
            arcade.color.GOLD,
            50,
            anchor_x="center",
            bold=True
        )
        win.draw()

        # Отображаем статистику
        chest = arcade.Text(
            f"Собрано сундуков: {self.chests_collected}/{self.total_chests}",
            self.width // 2,
            self.height // 2,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )
        chest.draw()

        # Отображаем время
        elapsed_time = self.victory_time - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time = arcade.Text(
            f"Время: {minutes:02d}:{seconds:02d}",
            self.width // 2,
            self.height // 2 - 50,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )
        time.draw()

        monster = arcade.Text(f"Убито монстров: {self.monster_collected}",
                              self.width // 2,
                              self.height // 2 - 100,
                              arcade.color.WHITE,
                              30,
                              anchor_x="center")
        monster.draw()
        # Инструкция для продолжения
        escape = arcade.Text(
            "Нажмите ESC для возврата в лобби",
            self.width // 2,
            100,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center"
        )
        escape.draw()

    def _draw_death_screen(self):
        # Красный полупрозрачный прямоугольник на весь экран
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.window.width // 2,
                self.window.height // 2,
                self.window.width,
                self.window.height
            ),
            (255, 0, 0, 150)  # Красный с прозрачностью
        )

        # Белая надпись "ВЫ ПОГИБЛИ" по центру
        self.dead = arcade.Text(
            "ВЫ ПОГИБЛИ",
            self.window.width // 2,
            self.window.height // 2 + 50,
            arcade.color.WHITE,
            64,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        self.dead.draw()
        # Инструкция для продолжения
        self.esc = arcade.Text(
            "Нажмите ESC для выхода в меню",
            self.window.width // 2,
            self.window.height // 2 - 100,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )
        self.esc.draw()

    def _draw_pause_screen(self):
        # Красный полупрозрачный прямоугольник на весь экран
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                self.window.width // 2,
                self.window.height // 2,
                self.window.width,
                self.window.height
            ),
            (150, 150, 150, 150)  # Красный с прозрачностью
        )

        # Белая надпись "ВЫ ПОГИБЛИ" по центру
        self.dead = arcade.Text(
            "ПАУЗА",
            self.window.width // 2,
            self.window.height // 2 + 50,
            arcade.color.WHITE,
            64,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )
        self.dead.draw()
        # Инструкция для продолжения
        self.esc = arcade.Text(
            "Нажмите SPACE, чтобы возобновить игру",
            self.window.width // 2,
            self.window.height // 2 - 100,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center"
        )
        self.esc.draw()

    def on_update(self, delta_time):
        # Проверяем смерть
        if self.player_sprite.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.victory_time = time.time()
        if self.is_dead or self.show_victory or self.pause:
            self.keys_pressed = set()
            # Останавливаем движение
            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False
            return
        self.portal_glow += delta_time * 2
        self.camera_shake.update(delta_time)
        self.player_list.update(delta_time, self.keys_pressed)
        self.enemy_spawn_list.update(delta_time)
        self.player_enemy()
        self.potion_enemy()
        self.wave_enemy()
        self.potion_list.update()
        self.player_list.update_animation()
        self.enemy_spawn_list.update_animation()
        self.effect_list.update(x=self.player_sprite.center_x, y=self.player_sprite.center_y - 20)
        self.potion_list.update()
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

        # Обновляем физику
        if self.physics_engine:
            self.physics_engine.update()

        # Проверяем сбор сундуков
        chest_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.chests_list)
        for chest in chest_hit_list:
            chest.remove_from_sprite_lists()
            self.chests_collected += 1

        for potion in self.potion_list:
            # Проверяем столкновение с одним спрайтом
            hit_list = arcade.check_for_collision_with_list(
                potion, self.collision_list)
            if hit_list:
                wave = WEffect(x=potion.center_x, y=potion.center_y)
                self.effect_list.append(wave)
                potion.remove_from_sprite_lists()

        portal_x, portal_y = self.portal_position
        distance_to_portal = math.sqrt(
            (self.player_sprite.center_x - portal_x) ** 2 +
            (self.player_sprite.center_y - portal_y) ** 2
        )

        # Если игрок находится в радиусе портала
        if distance_to_portal - 50 < self.portal_radius and not self.show_victory and self.E_pressed and self.chests_collected == self.total_chests:
            self.show_victory = True
            self.victory_time = time.time()

        for monster in self.enemy_spawn_list:
            distance_to_monster = math.sqrt(
                (self.player_sprite.center_x - monster.center_x) ** 2 +
                (self.player_sprite.center_y - monster.center_y) ** 2
            )
            if distance_to_monster <= 500:
                monster.logic(delta_time, self.player_sprite.center_x,
                              self.player_sprite.center_y)
            if distance_to_monster <= 50:
                monster.attack()

    def potion_enemy(self):
        """
        Проверяем столкновения снарядов с врагами
        """
        for potion in self.potion_list:
            # Проверяем столкновение с врагами
            enemy_hit_list = arcade.check_for_collision_with_list(
                potion,
                self.enemy_spawn_list
            )

            for enemy in enemy_hit_list:
                # Удаляем снаряд
                potion.remove_from_sprite_lists()

                # Наносим урон врагу
                enemy.health -= potion.damage

                # Если враг умер
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    self.monster_collected += 1
                break

    def wave_enemy(self):
        for effect in self.effect_list:
            enemy_hit_list = arcade.check_for_collision_with_list(
                effect,
                self.enemy_spawn_list
            )
            for enemy in enemy_hit_list:
                enemy.health -= effect.damage

                # Если враг умер
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    self.monster_collected += 1
                break

    def player_enemy(self):
        """
        Проверяем столкновения игрока с врагами
        """
        # Проверяем, столкнулся ли игрок с каким-либо врагом
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.enemy_spawn_list
        )

        for enemy in enemy_hit_list:
            self.monster_attack_sound.play(volume=0.5)
            # Уменьшаем здоровье игрока при столкновении
            if not self.immortality:
                #self.player_lose_hp_sound.play()
                self.player_sprite.health -= enemy.damage

                # Отталкиваем игрока от врага
                self.push_player_away(enemy)

                # Добавляем тряску камеры для эффекта удара
                self.camera_shake.start()

        # Если здоровье кончилось
        if self.player_sprite.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.victory_time = time.time()

    def push_player_away(self, enemy):
        """
        Отталкивает игрока от врага при столкновении
        """
        # Вычисляем направление от врага к игроку
        dx = self.player_sprite.center_x - enemy.center_x
        dy = self.player_sprite.center_y - enemy.center_y

        # Нормализуем вектор
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance

        # Отталкиваем игрока на некоторое расстояние
        push_distance = 50  # Можно настроить
        self.player_sprite.center_x += dx * push_distance
        self.player_sprite.center_y += dy * push_distance

        # Проверяем, чтобы игрок не вышел за границы мира
        self.player_sprite.center_x = max(
            0, min(self.player_sprite.center_x, self.world_width))
        self.player_sprite.center_y = max(
            0, min(self.player_sprite.center_y, self.world_height))

    def on_key_press(self, key, modifiers):
        # Если игрок умер
        if self.is_dead:
            self.death_sound.play()
            if key == arcade.key.ESCAPE:
                self.escape_sound.play()
                self.window.show_view(self.parent)
            return
        elif self.show_victory:
            if key != arcade.key.ESCAPE:
                self.win_sound.play()
                self.new_level()
                self.show_victory = False
            elif key == arcade.key.ESCAPE:
                self.escape_sound.play()
                self.window.show_view(self.parent)
            return
        elif self.pause:
            if key == arcade.key.SPACE:
                self.escape_sound.play()
                self.pause = False
            else:
                self.death_sound.play()
            return
        # Если игрок жив
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
        elif key == arcade.key.SPACE:
            self.pause = True
        elif key == arcade.key.Q:
            self.player_sprite.health = self.player_sprite.health - \
                1 if self.player_sprite.health - 1 >= 0 else 0
        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.user_settings["fullscreen"] = not self.window.user_settings["fullscreen"]
            self.save_settings()
            self.update_pos(self.hp_bar, True)
            self.update_pos(self.potion_cd)
            self.window.user_settings["fullscreen"] = self.window.fullscreen
        elif key == arcade.key.E:
            self.E_pressed = True
        elif key == arcade.key.R:
            self.new_level()
        elif key == arcade.key.ESCAPE:
            self.escape_sound.play()
            self.window.show_view(self.parent)
        elif key == arcade.key.Z:
            self.win_sound.play()
            self.immortality = not self.immortality

        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            if self.music_volume < 1.0:
                self.music_volume = min(1.0, self.music_volume + 0.1)
                print(f"Громкость музыки: {int(self.music_volume * 100)}%")
                self.window.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                self._update_music_volume()

        elif key == arcade.key.MINUS:
            if self.music_volume > 0.0:
                self.music_volume = max(0.0, self.music_volume - 0.1)
                print(f"Громкость музыки: {int(self.music_volume * 100)}%")
                self.window.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                self._update_music_volume()

        elif key == arcade.key.M:
            if self.lobby_music:
                if self.music_player:
                    try:
                        arcade.stop_sound(self.music_player)
                        self.music_player = None
                    except Exception as e:
                        print(f"❗Ошибка при остановке музыки: {e}")
                        self.music_player = None
                else:
                    self.music_player = arcade.play_sound(
                        self.lobby_music, volume=self.music_volume, loop=True)

    def on_key_release(self, key, modifiers):
        if self.is_dead:
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
        elif key == arcade.key.E:
            self.E_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_dead or self.pause:
            self.death_sound.play()
            return
        elif self.show_victory:
            self.win_sound.play()
            return

        if button == arcade.MOUSE_BUTTON_LEFT and self.can_attack:
            splash = AEffect(x=self.player_sprite.center_x, y=self.player_sprite.center_y -
                             20, face_direction=self.player_sprite.face_direction)
            self.effect_list.append(splash)
            self.player_attack_sound.play(volume=0.5)
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

    def attack_ready(self, delta_time):
        self.can_attack = True
        arcade.unschedule(self.attack_ready)

    def new_level(self):
        if self.win_the_game:
            self.window.show_view(self.parent.parent)
        if self.level + 1 == self.last_level:
            self.win_the_game = True
        self.update_pos(self.hp_bar, True)
        self.update_pos(self.potion_cd)
        self.level = min(self.level + 1, 2)
        self.chests_collected = 0
        self.enemy_spawn_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.hp_lvl = 5 - self.player_sprite.health
        self._load_map()

    def update_pos(self, sprite, list=False):
        if list:
            for x in sprite:
                x.center_x = x.center_x
                x.center_y = self.window.height - 50
        else:
            sprite.center_x = sprite.center_x
            sprite.center_y = self.window.height - 80

    def _setup_music(self):
        try:
            # Пробуем разные пути к файлу
            music_paths = ["assets/music/game_music.mp3"]
            for path in music_paths:
                if os.path.exists(path):
                    self.lobby_music = arcade.load_sound(path)
                    break

            if self.lobby_music:
                pass
            else:
                print(
                    "❗Файл музыки не найден. Проверьте наличие файла в директории проекта.")

        except Exception as e:
            print(f"❗Ошибка при загрузке музыки: {e}")
    
    def _update_music_volume(self):
        if self.lobby_music and self.music_player:
            try:
                # Останавливаем текущее воспроизведение
                arcade.stop_sound(self.music_player)
                # Перезапускаем с новой громкостью
                self.music_player = arcade.play_sound(
                    self.lobby_music, volume=self.music_volume, loop=True)
            except:
                pass

    def on_hide_view(self):
        if self.music_player:
            try:
                arcade.stop_sound(self.music_player)
                self.music_player = None
            except:
                pass
    
    def on_show_view(self):
        if self.window.user_settings.get("fullscreen", False):
            self.window.set_fullscreen(True)
            self.update_pos(self.hp_bar, True)
            self.update_pos(self.potion_cd)
        if self.lobby_music and not self.music_player:
            self.music_player = arcade.play_sound(
                self.lobby_music, volume=self.music_volume, loop=True)
    
    def save_settings(self):
        with open("code/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.window.user_settings, f, indent=4, ensure_ascii=False)