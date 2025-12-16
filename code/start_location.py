import arcade
import math
import random

# Константы окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Running Sloth - Character Lobby"

# Цвета для лобби
COLOR_BACKGROUND = (20, 15, 30)
COLOR_PLATFORM = (40, 35, 60)
COLOR_PLATFORM_LIGHT = (60, 55, 90)
COLOR_HIGHLIGHT = (100, 200, 255)
COLOR_UI_TEXT = (240, 240, 200)
COLOR_SELECTED = (255, 215, 0)
COLOR_UNSELECTED = (150, 150, 180)
COLOR_SELECTION_RECT = (255, 215, 0, 80)  # Полупрозрачный желтый для прямоугольника выделения


class CharacterSlot:
    def __init__(self, x, y, character_id, name, description):
        self.center_x = x
        self.center_y = y
        self.character_id = character_id
        self.name = name
        self.description = description
        self.is_selected = False
        self.is_hovered = False
        self.color = COLOR_UNSELECTED
        
        # Создаем текстовые объекты заранее
        self.text_code = arcade.Text(
            "КОД ПЕРСОНАЖА",
            x, y + 40,
            arcade.color.WHITE, 14,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_subcode = arcade.Text(
            "записан здесь!",
            x, y + 20,
            arcade.color.LIGHT_GRAY, 12,
            anchor_x="center", anchor_y="center"
        )
        
        self.text_name = arcade.Text(
            name,
            x, y - 70,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_desc = arcade.Text(
            description,
            x, y - 100,
            arcade.color.LIGHT_GRAY, 14,
            anchor_x="center", anchor_y="center",
            align="center",
            width=180
        )
        
        self.text_selected = arcade.Text(
            "✓ ВЫБРАН",
            x, y - 130,
            COLOR_SELECTED, 16,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
    def draw(self):
        """Отрисовка слота персонажа"""
        # Полупрозрачный прямоугольник выделения для выбранного персонажа
        if self.is_selected:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    self.center_x,
                    self.center_y + 10,
                    210,  # Ширина
                    260   # Высота
                ),
                COLOR_SELECTION_RECT
            )
        
        # Персонаж (пока просто кружок с комментом)
        arcade.draw_circle_filled(
            self.center_x, self.center_y + 40,
            60,
            (100, 150, 200) if self.character_id == 1 else 
            (200, 100, 150) if self.character_id == 2 else
            (150, 200, 100)
        )
        
        # Отображаем заранее созданные текстовые объекты
        self.text_code.draw()
        self.text_subcode.draw()
        self.text_name.draw()
        self.text_desc.draw()
        
        # Индикатор выбора
        if self.is_selected:
            self.text_selected.draw()


class CharacterLobbyView(arcade.View):
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
        
        # Заголовки
        self.title_text = None
        self.subtitle_text = None
        
        # Тексты для статистики в правом нижнем углу
        self.selected_title_text = None
        self.stats_texts = []
        
        # Кнопки
        self.button_texts = []
        
        # Координаты мыши
        self._mouse_x = 0
        self._mouse_y = 0
        
        self.setup()
    
    def setup(self):
        # Создаем слоты для персонажей
        slot_positions = [
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.55, 1, "ЛЕНИВЕЦ БОБИ", ""),
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.55, 2, "ПАНДА ПИТ", ""),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.55, 3, "ЁЖИК СПИДИ", "")
        ]
        for x, y, char_id, name, desc in slot_positions:
            slot = CharacterSlot(x, y, char_id, name, desc)
            self.character_slots.append(slot)
        
        # Выбираем первого персонажа по умолчанию
        if self.character_slots:
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
            "Нажмите ПРОБЕЛ для подтверждения выбора",
            "Используйте ← → для навигации"
        ]
        
        for i, text in enumerate(instructions):
            color = COLOR_HIGHLIGHT if i == 0 else arcade.color.LIGHT_GRAY
            size = 18 if i == 0 else 16
            y_pos = SCREEN_HEIGHT - 200 - i * 30
            
            self.instruction_texts.append(
                arcade.Text(
                    text,
                    SCREEN_WIDTH // 2, y_pos,
                    color, size,
                    anchor_x="center", anchor_y="center"
                )
            )
        
        # Создаем заголовки
        self.title_text = arcade.Text(
            "THE RUNNING SLOTH",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            COLOR_UI_TEXT,
            48,
            anchor_x="center",
            font_name="Kenney Blocks",
            bold=True
        )
        
        self.subtitle_text = arcade.Text(
            "ЛОББИ ВЫБОРА ПЕРСОНАЖА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            (200, 200, 255), 28,
            anchor_x="center"
        )
        
        # Создаем текстовые объекты для статистики - ЛЕВЕЕ на 250 пикселей
        stats_x = SCREEN_WIDTH - 350  # Было -100, стало -350 (левее на 250)
        
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
        # Кнопка "НАЧАТЬ ИГРУ"
        start_btn = arcade.SpriteSolidColor(300, 60, (80, 180, 100))
        start_btn.center_x = SCREEN_WIDTH // 2
        start_btn.center_y = 120
        start_btn.label = "НАЧАТЬ ИГРУ"
        start_btn.is_hovered = False
        self.ui_elements.append(start_btn)
        self.buttons.append(start_btn)
        
        # Текст кнопки
        self.button_texts.append(
            arcade.Text(
                "НАЧАТЬ ИГРУ",
                start_btn.center_x, start_btn.center_y,
                arcade.color.WHITE, 24,
                anchor_x="center", anchor_y="center",
                bold=True
            )
        )
        
        # Кнопка "НАЗАД" (в стартовое меню)
        back_btn = arcade.SpriteSolidColor(200, 50, (100, 100, 120))
        back_btn.center_x = 120
        back_btn.center_y = SCREEN_HEIGHT - 40
        back_btn.label = "НАЗАД"
        back_btn.is_hovered = False
        self.ui_elements.append(back_btn)
        self.buttons.append(back_btn)
        
        # Текст кнопки
        self.button_texts.append(
            arcade.Text(
                "НАЗАД",
                back_btn.center_x, back_btn.center_y,
                arcade.color.WHITE, 24,
                anchor_x="center", anchor_y="center",
                bold=True
            )
        )
    
    def on_draw(self):
        self.clear(COLOR_BACKGROUND)
        
        # Рисуем фон с частицами
        self._draw_background()
        
        # Рисуем заголовок
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
                color = COLOR_HIGHLIGHT
            else:
                color = arcade.color.WHITE
            
            if i < len(self.button_texts):
                self.button_texts[i].color = color
        
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
                    1: ["⚔️ УРОН: СРЕДНИЙ", "🛡️ ЗАЩИТА: ВЫСОКАЯ", "⚡ СКОРОСТЬ: ОЧЕНЬ МЕДЛЕННО"],
                    2: ["⚔️ УРОН: ВЫСОКИЙ", "🛡️ ЗАЩИТА: СРЕДНЯЯ", "⚡ СКОРОСТЬ: СРЕДНЯЯ"],
                    3: ["⚔️ УРОН: НИЗКИЙ", "🛡️ ЗАЩИТА: НИЗКАЯ", "⚡ СКОРОСТЬ: ОЧЕНЬ БЫСТРО"]
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
            slot.is_hovered = (
                abs(x - slot.center_x) <= 100 and
                abs(y - slot.center_y) <= 125
            )
    
    def on_mouse_press(self, x, y, button, modifiers):
        for slot in self.character_slots:
            if abs(x - slot.center_x) <= 100 and abs(y - slot.center_y) <= 125:
                for s in self.character_slots:
                    s.is_selected = False
                slot.is_selected = True
                self.selected_character = slot.character_id
                print(f"Выбран персонаж: {slot.name} (ID: {slot.character_id})")
        
        for i, btn in enumerate(self.buttons):
            if abs(x - btn.center_x) <= btn.width / 2 and abs(y - btn.center_y) <= btn.height / 2:
                if btn.label == "НАЧАТЬ ИГРУ":
                    if self.selected_character:
                        print(f"Запуск игры с персонажем ID: {self.selected_character}")
                    else:
                        print("Сначала выберите персонажа!")
                elif btn.label == "НАЗАД":
                    print("Возврат в стартовое меню...")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.selected_character:
                new_id = self.selected_character - 1
                if new_id < 1:
                    new_id = len(self.character_slots)
                self._select_character(new_id)
        
        elif key == arcade.key.RIGHT:
            if self.selected_character:
                new_id = self.selected_character + 1
                if new_id > len(self.character_slots):
                    new_id = 1
                self._select_character(new_id)
        
        elif key == arcade.key.SPACE:
            if self.selected_character:
                print(f"Запуск игры с персонажем ID: {self.selected_character}")
        
        elif key == arcade.key.ESCAPE:
            print("Возврат в стартовое меню...")
    
    def _select_character(self, character_id):
        for slot in self.character_slots:
            slot.is_selected = (slot.character_id == character_id)
        self.selected_character = character_id
        print(f"Выбран персонаж ID: {character_id}")


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    lobby_view = CharacterLobbyView()
    window.show_view(lobby_view)
    arcade.run()


if __name__ == "__main__":
    main()