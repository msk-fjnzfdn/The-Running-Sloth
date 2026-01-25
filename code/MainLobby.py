from constants import *
from LobbySlot import *
from Add_To_Lobby import LobbyUIManager
from Game_start import *
from id1_character import *


class MainLobby(arcade.View):
    def __init__(self, obj=None):
        super().__init__()

        self.parent = obj

        # Загрузка настроек
        self.load_settings()

        # Переменные для масштабирования
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Дополнительные настройки для корректировки позиций
        self.left_margin = 50
        self.right_margin = 50
        self.top_margin = 50
        self.bottom_margin = 50

        # Слоты персонажей
        self.character_slots = []
        self.selected_character = None

        # UI элементы
        self.ui_elements = arcade.SpriteList()
        self.buttons = []

        # Эффекты
        self.particles = []
        self.game_time = 0

        # Координаты мыши
        self._mouse_x = 0
        self._mouse_y = 0

        # UI менеджер
        self.ui_manager = None

        # Музыка
        self.lobby_music = None
        self.music_volume = 0.3
        self.music_player = None

        self.setup()

    def load_settings(self):
        try:
            with open("code/settings.json", "r", encoding="utf-8") as f:
                self.user_settings = json.load(f)

            # Загружаем сохраненную громкость музыки
            if "music_volume" in self.user_settings:
                self.music_volume = self.user_settings["music_volume"]
            else:
                self.music_volume = 0.3
        except Exception:
            self.music_volume = 0.3

    def save_settings(self):
        with open("code/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.user_settings, f, indent=4, ensure_ascii=False)

    def update_all_positions(self):
        window_width = self.window.width
        window_height = self.window.height

        # Вычисляем доступное пространство с учетом отступов
        available_width = window_width - self.left_margin - self.right_margin
        available_height = window_height - self.top_margin - self.bottom_margin

        # Вычисляем масштабный коэффициент с учетом отступов
        scale_x = available_width / SCREEN_WIDTH
        scale_y = available_height / SCREEN_HEIGHT
        self.scale_factor = min(scale_x, scale_y)

        # Вычисляем смещение с учетом отступов
        self.offset_x = (window_width - SCREEN_WIDTH * self.scale_factor) / 2
        self.offset_x -= 20 * self.scale_factor

        self.offset_y = (window_height - SCREEN_HEIGHT * self.scale_factor) / 2

        # Обновляем позиции слотов
        for slot in self.character_slots:
            slot.update_position(
                self.scale_factor, self.offset_x, self.offset_y)

        # Обновляем позиции UI элементов через UI менеджер
        if self.ui_manager:
            self.ui_manager.update_positions(
                self.scale_factor,
                self.offset_x,
                self.offset_y,
                self.buttons
            )

    def setup(self):
        self.load_settings()
        # Создаем слоты для персонажей
        slot_positions = [
            (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT *
             0.45, 1, "Зориан", "Алхимик", True),
            (SCREEN_WIDTH * 0.47, SCREEN_HEIGHT * 0.45, 2, "???", "???", False),
            (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.45, 3, "???", "???", False)
        ]

        for x, y, char_id, name, desc, unlocked in slot_positions:
            slot = LobbySlot(x, y, char_id, name, desc, unlocked)
            self.character_slots.append(slot)

        # Выбираем первого персонажа по умолчанию
        if self.character_slots and self.character_slots[0].is_unlocked:
            self.character_slots[0].is_selected = True
            self.selected_character = 1

        # Создаем кнопки
        self._create_ui()

        # Создаем частицы для фона
        for _ in range(60):
            self.particles.append({
                'x': random.uniform(0, SCREEN_WIDTH),
                'y': random.uniform(0, SCREEN_HEIGHT),
                'size': random.uniform(2, 6),
                'speed': random.uniform(0.5, 2),
                'color': random.choice([
                    (100, 200, 255, 100),
                    (255, 100, 200, 100),
                    (200, 255, 100, 100)
                ]),
                'offset': random.uniform(0, math.pi * 2)
            })

        # Создаем UI менеджер
        self.ui_manager = LobbyUIManager(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.buttons
        )

        # Загружаем музыку (но НЕ запускаем)
        self._setup_music()

        # Сразу обновляем позиции
        self.update_all_positions()

    def _setup_music(self):
        try:
            # Пробуем разные пути к файлу
            music_paths = [
                "assets/music/lobby_music.mp3"
            ]
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

    def _create_ui(self):
        # Кнопка "НАЧАТЬ ИГРУ"
        start_btn = arcade.SpriteSolidColor(300, 60, COLOR_BUTTON_DEFAULT)
        start_btn.center_x = SCREEN_WIDTH // 2
        start_btn.center_y = 120
        start_btn.label = "НАЧАТЬ ИГРУ"
        start_btn.is_hovered = False
        start_btn.is_enabled = True
        self.ui_elements.append(start_btn)
        self.buttons.append(start_btn)

        # Кнопка "НАЗАД"
        back_btn = arcade.SpriteSolidColor(200, 50, COLOR_BUTTON_DEFAULT)
        back_btn.center_x = 100
        back_btn.center_y = SCREEN_HEIGHT - 40
        back_btn.label = "НАЗАД"
        back_btn.is_hovered = False
        self.ui_elements.append(back_btn)
        self.buttons.append(back_btn)

    def on_show_view(self):
        if self.user_settings.get("fullscreen", False):
            self.window.set_fullscreen(True)

        # Запускаем музыку при показе лобби, только если она еще не играет
        if self.lobby_music and not self.music_player:
            self.music_player = arcade.play_sound(
                self.lobby_music, volume=self.music_volume, loop=True)

        self.update_all_positions()

    def on_hide_view(self):
        # Останавливаем музыку при выходе из лобби
        if self.music_player:
            try:
                arcade.stop_sound(self.music_player)
                self.music_player = None
            except:
                pass

    def on_draw(self):
        self.clear(COLOR_BACKGROUND)

        # Рисуем фон с частицами
        self._draw_background()

        # Рисуем UI через менеджер
        if self.ui_manager:
            self.ui_manager.draw(self.selected_character, self.character_slots)

        # Рисуем слоты персонажей
        for slot in self.character_slots:
            slot.draw()

        # Рисуем UI элементы
        self.ui_elements.draw()

        # Рисуем текст на кнопках через UI менеджер
        if self.ui_manager:
            self.ui_manager.draw_ui_text(self.buttons, self.selected_character)

    def _draw_background(self):
        window_width = self.window.width
        window_height = self.window.height

        # Градиентный фон
        for i in range(10):
            t = i / 10
            height = window_height / 10
            y = i * height

            color = (
                int(20 * (1 - t) + 10 * t),
                int(15 * (1 - t) + 5 * t),
                int(30 * (1 - t) + 15 * t)
            )

            arcade.draw_lbwh_rectangle_filled(
                0, y,
                window_width, height,
                color
            )

        # Плавающие частицы
        for particle in self.particles:
            x = particle['x'] * self.scale_factor + self.offset_x
            y = particle['y'] * self.scale_factor + self.offset_y

            is_visible = (
                -50 <= x <= window_width + 50 and
                -50 <= y <= window_height + 50
            )

            if is_visible:
                pulse = (math.sin(self.game_time *
                         particle['speed'] + particle['offset']) + 1) * 0.5
                alpha = int(50 + pulse * 50)
                size = particle['size'] * \
                    self.scale_factor * (0.8 + pulse * 0.4)

                arcade.draw_circle_filled(
                    x, y, size,
                    (*particle['color'][:3], alpha)
                )

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

    def on_update(self, delta_time):
        self.game_time += delta_time

        # Обновляем частицы
        window_width = self.window.width
        window_height = self.window.height

        for particle in self.particles:
            particle['x'] += math.sin(self.game_time *
                                      0.5 + particle['offset']) * 0.5
            particle['y'] += math.cos(self.game_time *
                                      0.3 + particle['offset']) * 0.3

            virtual_width = max(SCREEN_WIDTH, window_width /
                                max(self.scale_factor, 0.1))
            virtual_height = max(
                SCREEN_HEIGHT, window_height / max(self.scale_factor, 0.1))

            if particle['x'] < 0:
                particle['x'] = virtual_width
            elif particle['x'] > virtual_width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = virtual_height
            elif particle['y'] > virtual_height:
                particle['y'] = 0

        # Обновляем состояние кнопок
        for btn in self.buttons:
            btn.is_hovered = (
                abs(self._mouse_x - btn.center_x) <= btn.width / 2 and
                abs(self._mouse_y - btn.center_y) <= btn.height / 2
            )

        # Обновляем UI менеджер
        if self.ui_manager:
            self.ui_manager.update(self._mouse_x, self._mouse_y, self.buttons)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.update_all_positions()

    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y

        for slot in self.character_slots:
            if slot.is_unlocked:
                hover_width = 100 * self.scale_factor
                hover_height = 125 * self.scale_factor
                slot.is_hovered = (
                    abs(x - slot.center_x) <= hover_width and
                    abs(y - slot.center_y) <= hover_height
                )
            else:
                slot.is_hovered = False

    def on_mouse_press(self, x, y, button, modifiers):
        # Обработка кликов по слотам персонажей
        for slot in self.character_slots:
            click_width = 100 * self.scale_factor
            click_height = 125 * self.scale_factor

            if abs(x - slot.center_x) <= click_width and abs(y - slot.center_y) <= click_height:
                if slot.is_unlocked:
                    for s in self.character_slots:
                        s.is_selected = False
                    slot.is_selected = True
                    self.selected_character = slot.character_id
                else:
                    pass

        # Обработка кликов по кнопкам
        for btn in self.buttons:
            if abs(x - btn.center_x) <= btn.width / 2 and abs(y - btn.center_y) <= btn.height / 2:
                if btn.label == "НАЧАТЬ ИГРУ":
                    if self.selected_character:
                        self.play_view = PlayView(character_id=1, obj=self)
                        self.window.show_view(self.play_view)
                    else:
                        pass
                elif btn.label == "НАЗАД":
                    self.window.show_view(self.parent)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.selected_character:
                current_index = self.selected_character - 1
                for offset in range(len(self.character_slots)):
                    new_index = (current_index - offset -
                                 1) % len(self.character_slots)
                    if self.character_slots[new_index].is_unlocked:
                        self._select_character(new_index + 1)
                        break

        elif key == arcade.key.RIGHT:
            if self.selected_character:
                current_index = self.selected_character - 1
                for offset in range(len(self.character_slots)):
                    new_index = (current_index + offset +
                                 1) % len(self.character_slots)
                    if self.character_slots[new_index].is_unlocked:
                        self._select_character(new_index + 1)
                        break

        elif key == arcade.key.SPACE:
            if self.selected_character:
                pass

        elif key == arcade.key.ESCAPE:
            pass

        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.update_all_positions()
            self.user_settings["fullscreen"] = self.window.fullscreen
            self.save_settings()

        # Управление музыкой
        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            if self.music_volume < 1.0:
                self.music_volume = min(1.0, self.music_volume + 0.1)
                self.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                # Обновляем громкость играющей музыки
                self._update_music_volume()

        elif key == arcade.key.MINUS:
            if self.music_volume > 0.0:
                self.music_volume = max(0.0, self.music_volume - 0.1)
                print(f"Громкость музыки: {int(self.music_volume * 100)}%")
                self.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                # Обновляем громкость играющей музыки
                self._update_music_volume()

        elif key == arcade.key.M:
            # Включить/выключить музыку
            if self.lobby_music:
                if self.music_player:
                    # Проверяем, играет ли музыка
                    try:
                        # Останавливаем текущее воспроизведение
                        arcade.stop_sound(self.music_player)
                        self.music_player = None
                    except Exception as e:
                        print(f"❗Ошибка при остановке музыки: {e}")
                        # Если ошибка, просто сбрасываем player
                        self.music_player = None
                else:
                    # Запускаем музыку
                    self.music_player = arcade.play_sound(
                        self.lobby_music, volume=self.music_volume, loop=True)

    def _select_character(self, character_id):
        for slot in self.character_slots:
            slot.is_selected = (slot.character_id ==
                                character_id and slot.is_unlocked)
        self.selected_character = character_id
