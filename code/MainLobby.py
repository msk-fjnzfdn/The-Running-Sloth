import arcade
import math
import random
from LobbySlot import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
    COLOR_BACKGROUND, COLOR_HIGHLIGHT, COLOR_UI_TEXT,
    COLOR_SELECTED, COLOR_BUTTON_DEFAULT,
    LobbySlot
)


class MainLobby(arcade.View):
    def __init__(self):
        super().__init__()
        
        # Слоты персонажей
        self.character_slots = []
        self.selected_character = None
        
        # UI элементы
        self.ui_elements = arcade.SpriteList()
        self.buttons = []
        
        # Эффекты
        self.particles = []
        self.game_time = 0
        
        # Текст инструкций
        self.instruction_texts = []
        
        # Заголовки (с уменьшенным размером)
        self.title_text = None
        self.subtitle_text = None
        
        # Тексты для статистики в правом нижнем углу
        self.selected_title_text = None
        self.stats_texts = []
        
        # Кнопки (серые по умолчанию)
        self.button_texts = []
        
        # Координаты мыши
        self._mouse_x = 0
        self._mouse_y = 0
        
        self.setup()
    
    def setup(self):
        # Создаем слоты для персонажей с описаниями
        # Только первый персонаж разблокирован
        slot_positions = [
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.45, 1, "Зориан", "Алхимик", True),
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.45, 2, "???", "???", False),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.45, 3, "???", "???", False)
        ]
        for x, y, char_id, name, desc, unlocked in slot_positions:
            slot = LobbySlot(x, y, char_id, name, desc, unlocked)
            self.character_slots.append(slot)
        
        # Выбираем первого персонажа по умолчанию (он разблокирован)
        if self.character_slots and self.character_slots[0].is_unlocked:
            self.character_slots[0].is_selected = True
            self.selected_character = 1
        
        # Создаем кнопку старта
        self._create_ui()
        
        # Создаем частицы для фона
        for _ in range(30):
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
        
        # Создаем текстовые объекты для инструкций
        instructions = [
            "ДОБРО ПОЖАЛОВАТЬ В ЛОББИ ПЕРСОНАЖЕЙ",
            "Выберите персонажа для начала игры",
            "Доступен только Зориан (остальные заблокированы)",
            "Нажмите ПРОБЕЛ для подтверждения выбора"
        ]
        
        for i, text in enumerate(instructions):
            color = COLOR_HIGHLIGHT if i == 0 else arcade.color.LIGHT_GRAY
            size = 16 if i == 0 else 14  # Уменьшил размер шрифта
            y_pos = SCREEN_HEIGHT - 150 - i * 28
            
            self.instruction_texts.append(
                arcade.Text(
                    text,
                    SCREEN_WIDTH // 2, y_pos,
                    color, size,
                    anchor_x="center", anchor_y="center"
                )
            )
        
        # Создаем заголовки (уменьшил размер)
        self.title_text = arcade.Text(
            "THE RUNNING SLOTH",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            COLOR_UI_TEXT,
            36,  # Уменьшил с 48 до 36
            anchor_x="center",
            font_name="Kenney Blocks",
            bold=True
        )
        
        self.subtitle_text = arcade.Text(
            "ЛОББИ ВЫБОРА ПЕРСОНАЖА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 120,  # Поднял выше
            (200, 200, 255), 22,  # Уменьшил с 28 до 22
            anchor_x="center"
        )
        
        # Создаем текстовые объекты для статистики
        stats_x = SCREEN_WIDTH - 350
        
        # Заголовок выбранного персонажа
        self.selected_title_text = arcade.Text(
            "",
            stats_x, 180,
            COLOR_SELECTED, 22,
            anchor_x="left", anchor_y="center",
            bold=True
        )
        
        # Создаем 3 текстовых объекта для статистики (максимум 3 строки)
        for i in range(3):
            y_pos = 180 - 40 - i * 30
            self.stats_texts.append(
                arcade.Text(
                    "",
                    stats_x, y_pos,
                    arcade.color.LIGHT_GRAY, 16,
                    anchor_x="left", anchor_y="center"
                )
            )
    
    def _create_ui(self):
        # Кнопка "НАЧАТЬ ИГРУ" - серый цвет по умолчанию
        start_btn = arcade.SpriteSolidColor(300, 60, COLOR_BUTTON_DEFAULT)
        start_btn.center_x = SCREEN_WIDTH // 2
        start_btn.center_y = 120
        start_btn.label = "НАЧАТЬ ИГРУ"
        start_btn.is_hovered = False
        start_btn.is_enabled = True  # Кнопка всегда активна, т.к. есть разблокированный персонаж
        self.ui_elements.append(start_btn)
        self.buttons.append(start_btn)
        
        # Текст кнопки - серый по умолчанию
        self.button_texts.append(
            arcade.Text(
                "НАЧАТЬ ИГРУ",
                start_btn.center_x, start_btn.center_y,
                (180, 180, 180), 24,  # Серый цвет текста
                anchor_x="center", anchor_y="center",
                bold=True
            )
        )
        
        # Кнопка "НАЗАД" - серый цвет по умолчанию
        back_btn = arcade.SpriteSolidColor(200, 50, COLOR_BUTTON_DEFAULT)
        back_btn.center_x = 120
        back_btn.center_y = SCREEN_HEIGHT - 40
        back_btn.label = "НАЗАД"
        back_btn.is_hovered = False
        self.ui_elements.append(back_btn)
        self.buttons.append(back_btn)
        
        # Текст кнопки - серый по умолчанию
        self.button_texts.append(
            arcade.Text(
                "НАЗАД",
                back_btn.center_x, back_btn.center_y,
                (180, 180, 180), 24,  # Серый цвет текста
                anchor_x="center", anchor_y="center",
                bold=True
            )
        )
    
    def on_draw(self):
        self.clear(COLOR_BACKGROUND)
        
        # Рисуем фон с частицами
        self._draw_background()
        
        # Рисуем заголовки (уменьшенные)
        self.title_text.draw()
        self.subtitle_text.draw()
        
        # Рисуем слоты персонажей
        for slot in self.character_slots:
            slot.draw()
        
        # Рисуем UI элементы
        self.ui_elements.draw()
        
        # Рисуем текст на кнопках
        self._draw_ui_text()
        
        # Рисуем инструкции
        for text in self.instruction_texts:
            text.draw()
        
        # Рисуем информацию о выбранном персонаже
        self._draw_selected_info()
    
    def _draw_background(self):
        # Градиентный фон
        for i in range(10):
            t = i / 10
            height = SCREEN_HEIGHT / 10
            y = i * height
            
            color = (
                int(20 * (1 - t) + 10 * t),
                int(15 * (1 - t) + 5 * t),
                int(30 * (1 - t) + 15 * t)
            )
            
            arcade.draw_lbwh_rectangle_filled(
                0, y,
                SCREEN_WIDTH, height,
                color
            )
        
        # Плавающие частицы
        for particle in self.particles:
            if 0 <= particle['x'] <= SCREEN_WIDTH and 0 <= particle['y'] <= SCREEN_HEIGHT:
                pulse = (math.sin(self.game_time * particle['speed'] + particle['offset']) + 1) * 0.5
                alpha = int(50 + pulse * 50)
                size = particle['size'] * (0.8 + pulse * 0.4)
                
                arcade.draw_circle_filled(
                    particle['x'],
                    particle['y'],
                    size,
                    (*particle['color'][:3], alpha)
                )
    
    def _draw_ui_text(self):
        for i, btn in enumerate(self.buttons):
            if btn.is_hovered:
                # При наведении кнопка подсвечивается
                if btn.label == "НАЧАТЬ ИГРУ" and self.selected_character:
                    color = (80, 220, 120)  # Зеленый для активной кнопки старта
                    text_color = arcade.color.WHITE
                elif btn.label == "НАЗАД":
                    color = (120, 120, 140)  # Более светлый серый для кнопки назад
                    text_color = arcade.color.WHITE
                else:
                    color = COLOR_BUTTON_DEFAULT
                    text_color = (180, 180, 180)
                
                # Меняем цвет кнопки при наведении
                btn.color = color
            else:
                # Обычное состояние - серый
                text_color = (180, 180, 180)
                btn.color = COLOR_BUTTON_DEFAULT
            
            # Обновляем цвет текста
            if i < len(self.button_texts):
                self.button_texts[i].color = text_color
        
        for text in self.button_texts:
            text.draw()
    
    def _draw_selected_info(self):
        if self.selected_character:
            selected_slot = next((s for s in self.character_slots if s.character_id == self.selected_character), None)
            if selected_slot:
                # Обновляем заголовок
                self.selected_title_text.text = f"ВЫБРАН: {selected_slot.name}"
                self.selected_title_text.draw()
                
                # Статистика выбранного персонажа
                stats = {
                    1: ["⚔️ УРОН: ВЫСОКАЯ", "🛡️ ЗАЩИТА: НИЗКИЙ", "⚡ СКОРОСТЬ: ВЫСОКАЯ"],
                    2: ["⚔️ УРОН: ???", "🛡️ ЗАЩИТА: ???", "⚡ СКОРОСТЬ: ???"],
                    3: ["⚔️ УРОН: ???", "🛡️ ЗАЩИТА: ???", "⚡ СКОРОСТЬ: ???"]
                }
                
                current_stats = stats.get(self.selected_character, [])
                
                # Обновляем и рисуем статистику
                for i, stat_text in enumerate(self.stats_texts):
                    if i < len(current_stats):
                        stat_text.text = current_stats[i]
                        stat_text.draw()
                    else:
                        # Очищаем лишние строки
                        stat_text.text = ""
    
    def on_update(self, delta_time):
        self.game_time += delta_time
        
        for particle in self.particles:
            particle['x'] += math.sin(self.game_time * 0.5 + particle['offset']) * 0.5
            particle['y'] += math.cos(self.game_time * 0.3 + particle['offset']) * 0.3
            
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
        
        for btn in self.buttons:
            btn.is_hovered = (
                abs(self._mouse_x - btn.center_x) <= btn.width / 2 and
                abs(self._mouse_y - btn.center_y) <= btn.height / 2
            )
    
    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y
        
        for slot in self.character_slots:
            # Показываем ховер только для разблокированных персонажей
            if slot.is_unlocked:
                slot.is_hovered = (
                    abs(x - slot.center_x) <= 100 and
                    abs(y - slot.center_y) <= 125
                )
            else:
                slot.is_hovered = False
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Обработка кликов по персонажам
        for slot in self.character_slots:
            if abs(x - slot.center_x) <= 100 and abs(y - slot.center_y) <= 125:
                # Выбираем персонажа только если он разблокирован
                if slot.is_unlocked:
                    for s in self.character_slots:
                        s.is_selected = False
                    slot.is_selected = True
                    self.selected_character = slot.character_id
                    print(f"Выбран персонаж: {slot.name} (ID: {slot.character_id})")
                else:
                    print(f"Персонаж {slot.name} заблокирован!")
        
        # Обработка кликов по кнопкам
        for i, btn in enumerate(self.buttons):
            if abs(x - btn.center_x) <= btn.width / 2 and abs(y - btn.center_y) <= btn.height / 2:
                if btn.label == "НАЧАТЬ ИГРУ":
                    if self.selected_character:
                        print(f"Запуск игры с персонажем ID: {self.selected_character}")
                        # Здесь будет переход к основной игре
                    else:
                        print("Сначала выберите персонажа!")
                elif btn.label == "НАЗАД":
                    print("Возврат в стартовое меню...")
    
    def on_key_press(self, key, modifiers):
        # Стрелки работают только для переключения между разблокированных персонажей
        if key == arcade.key.LEFT:
            if self.selected_character:
                # Ищем предыдущего разблокированного персонажа
                current_index = self.selected_character - 1
                for offset in range(len(self.character_slots)):
                    new_index = (current_index - offset - 1) % len(self.character_slots)
                    if self.character_slots[new_index].is_unlocked:
                        self._select_character(new_index + 1)
                        break
        
        elif key == arcade.key.RIGHT:
            if self.selected_character:
                # Ищем следующего разблокированного персонажа
                current_index = self.selected_character - 1
                for offset in range(len(self.character_slots)):
                    new_index = (current_index + offset + 1) % len(self.character_slots)
                    if self.character_slots[new_index].is_unlocked:
                        self._select_character(new_index + 1)
                        break
        
        elif key == arcade.key.SPACE:
            if self.selected_character:
                print(f"Запуск игры с персонажем ID: {self.selected_character}")
        
        elif key == arcade.key.ESCAPE:
            print("Возврат в стартовое меню...")
    
    def _select_character(self, character_id):
        for slot in self.character_slots:
            slot.is_selected = (slot.character_id == character_id and slot.is_unlocked)
        self.selected_character = character_id
        print(f"Выбран персонаж ID: {character_id}")


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    lobby_view = MainLobby()
    window.show_view(lobby_view)
    arcade.run()


if __name__ == "__main__":
    main()
