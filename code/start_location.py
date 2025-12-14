from constants import *


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
        
    def draw(self):
        # Фон слота
        color = COLOR_SELECTED if self.is_selected else (COLOR_HIGHLIGHT if self.is_hovered else self.color)
        
        # Платформа персонажа
        '''
        arcade.draw_rectangle_filled(
            self.center_x, self.center_y,
            200, 250,
            COLOR_PLATFORM
        )
        '''
        '''
        # Выделение если выбран/наведен
        if self.is_selected or self.is_hovered:
            arcade.draw_rectangle_outline(
                self.center_x, self.center_y,
                210, 260,
                color, 3
            )
        '''
        # Персонаж (пока просто кружок с комментом)
        arcade.draw_circle_filled(
            self.center_x, self.center_y + 40,
            60,
            (100, 150, 200) if self.character_id == 1 else 
            (200, 100, 150) if self.character_id == 2 else
            (150, 200, 100)
        )
        
        # Коммент "Код персонажа записан здесь!"
        arcade.draw_text(
            "КОД ПЕРСОНАЖА",
            self.center_x, self.center_y + 40,
            arcade.color.WHITE, 14,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        arcade.draw_text(
            "записан здесь!",
            self.center_x, self.center_y + 20,
            arcade.color.LIGHT_GRAY, 12,
            anchor_x="center", anchor_y="center"
        )
        
        # Имя персонажа
        arcade.draw_text(
            self.name,
            self.center_x, self.center_y - 70,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        # Описание
        arcade.draw_text(
            self.description,
            self.center_x, self.center_y - 100,
            arcade.color.LIGHT_GRAY, 14,
            anchor_x="center", anchor_y="center",
            align="center",
            width=180
        )
        
        # Индикатор выбора
        if self.is_selected:
            arcade.draw_text(
                "✓ ВЫБРАН",
                self.center_x, self.center_y - 130,
                COLOR_SELECTED, 16,
                anchor_x="center", anchor_y="center",
                bold=True
            )

class CharacterLobby(arcade.View):
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
        self.instructions = [
            "ДОБРО ПОЖАЛОВАТЬ В ЛОББИ ПЕРСОНАЖЕЙ",
            "Выберите персонажа для начала игры",
            "Нажмите ПРОБЕЛ для подтверждения выбора",
            "Используйте ← → для навигации"
        ]
    
    def setup(self):
        # Создаем слоты для персонажей
        slot_positions = [
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.55, 1, "ЛЕНИВЕЦ БОБИ", "Медленный, но сильный\nВысокая защита"),
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.55, 2, "ПАНДА ПИТ", "Баланс скорости и силы\nУниверсальный боец"),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.55, 3, "ЁЖИК СПИДИ", "Быстрый и ловкий\nНизкий урон, высокая мобильность")
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
        for _ in range(50):
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
    
    def _create_ui(self):
        # Кнопка "НАЧАТЬ ИГРУ"
        start_btn = arcade.SpriteSolidColor(300, 60, (80, 180, 100))
        start_btn.center_x = SCREEN_WIDTH // 2
        start_btn.center_y = 120
        start_btn.label = "НАЧАТЬ ИГРУ"
        start_btn.is_hovered = False
        self.ui_elements.append(start_btn)
        self.buttons.append(start_btn)
        
        # Кнопка "НАЗАД" (в стартовое меню)
        back_btn = arcade.SpriteSolidColor(200, 50, (100, 100, 120))
        back_btn.center_x = 120
        back_btn.center_y = SCREEN_HEIGHT - 40
        back_btn.label = "НАЗАД"
        back_btn.is_hovered = False
        self.ui_elements.append(back_btn)
        self.buttons.append(back_btn)
    
    def on_draw(self):
        self.clear(COLOR_BACKGROUND)
        
        # Рисуем фон с частицами
        self._draw_background()
        
        # Рисуем заголовок
        self._draw_header()
        
        # Рисуем слоты персонажей
        for slot in self.character_slots:
            slot.draw()
        
        # Рисуем UI элементы
        self.ui_elements.draw()
        
        # Рисуем текст на кнопках
        self._draw_ui_text()
        
        # Рисуем инструкции
        self._draw_instructions()
        
        # Рисуем информацию о выбранном персонаже
        self._draw_selected_info()
    
    def _draw_background(self):
        # Градиентный фон
        for i in range(100):
            t = i / 100
            height = SCREEN_HEIGHT / 100
            y = i * height
            
            # Темно-синий градиент
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
            pulse = (math.sin(self.game_time * particle['speed'] + particle['offset']) + 1) * 0.5
            alpha = int(50 + pulse * 50)
            size = particle['size'] * (0.8 + pulse * 0.4)
            
            arcade.draw_circle_filled(
                particle['x'],
                particle['y'],
                size,
                (*particle['color'][:3], alpha)
            )
    
    def _draw_header(self):
        # Большой заголовок
        arcade.draw_text(
            "THE RUNNING SLOTH",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            COLOR_UI_TEXT,
            48,
            anchor_x="center",
            font_name="Kenney Blocks",
            bold=True
        )
        
        arcade.draw_text(
            "ЛОББИ ВЫБОРА ПЕРСОНАЖА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            (200, 200, 255), 28,
            anchor_x="center"
        )
    
    def _draw_ui_text(self):
        for btn in self.buttons:
            color = COLOR_HIGHLIGHT if btn.is_hovered else arcade.color.WHITE
            
            # Обводка при наведении
            '''
            if btn.is_hovered:
                arcade.draw_rectangle_outline(
                    btn.center_x, btn.center_y,
                    btn.width + 8, btn.height + 8,
                    COLOR_HIGHLIGHT, 3
                )
            '''
            # Текст кнопки
            arcade.draw_text(
                btn.label,
                btn.center_x, btn.center_y,
                color, 24,
                anchor_x="center", anchor_y="center",
                bold=True
            )
    
    def _draw_instructions(self):
        for i, text in enumerate(self.instructions):
            y_pos = SCREEN_HEIGHT - 200 - i * 30
            color = COLOR_HIGHLIGHT if i == 0 else arcade.color.LIGHT_GRAY
            
            arcade.draw_text(
                text,
                SCREEN_WIDTH // 2, y_pos,
                color, 18 if i == 0 else 16,
                anchor_x="center", anchor_y="center"
            )
    
    def _draw_selected_info(self):
        if self.selected_character:
            selected_slot = next((s for s in self.character_slots if s.character_id == self.selected_character), None)
            if selected_slot:
                arcade.draw_text(
                    f"ВЫБРАН: {selected_slot.name}",
                    SCREEN_WIDTH // 2, 200,
                    COLOR_SELECTED, 22,
                    anchor_x="center", anchor_y="center",
                    bold=True
                )
                
                # Статистика выбранного персонажа
                stats = {
                    1: ["⚔️ УРОН: СРЕДНИЙ", "🛡️ ЗАЩИТА: ВЫСОКАЯ", "⚡ СКОРОСТЬ: ОЧЕНЬ МЕДЛЕННО"],
                    2: ["⚔️ УРОН: ВЫСОКИЙ", "🛡️ ЗАЩИТА: СРЕДНЯЯ", "⚡ СКОРОСТЬ: СРЕДНЯЯ"],
                    3: ["⚔️ УРОН: НИЗКИЙ", "🛡️ ЗАЩИТА: НИЗКАЯ", "⚡ СКОРОСТЬ: ОЧЕНЬ БЫСТРО"]
                }
                
                for i, stat in enumerate(stats.get(self.selected_character, [])):
                    arcade.draw_text(
                        stat,
                        SCREEN_WIDTH // 2, 160 - i * 25,
                        arcade.color.LIGHT_GRAY, 16,
                        anchor_x="center", anchor_y="center"
                    )
    
    def on_update(self, delta_time):
        self.game_time += delta_time
        
        # Обновляем частицы
        for particle in self.particles:
            particle['x'] += math.sin(self.game_time * 0.5 + particle['offset']) * 0.5
            particle['y'] += math.cos(self.game_time * 0.3 + particle['offset']) * 0.3
            
            # Возвращаем частицы если они ушли за границы
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
        
        # Обновляем состояние кнопок
        for btn in self.buttons:
            btn.is_hovered = (
                abs(self._mouse_x - btn.center_x) <= btn.width / 2 and
                abs(self._mouse_y - btn.center_y) <= btn.height / 2
            )
    
    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y
        
        # Проверяем наведение на слоты персонажей
        for slot in self.character_slots:
            slot.is_hovered = (
                abs(x - slot.center_x) <= 100 and
                abs(y - slot.center_y) <= 125
            )
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Проверяем клик по слотам персонажей
        for slot in self.character_slots:
            if abs(x - slot.center_x) <= 100 and abs(y - slot.center_y) <= 125:
                # Снимаем выделение со всех слотов
                for s in self.character_slots:
                    s.is_selected = False
                # Выделяем выбранный слот
                slot.is_selected = True
                self.selected_character = slot.character_id
                print(f"Выбран персонаж: {slot.name} (ID: {slot.character_id})")
        
        # Проверяем клик по кнопкам
        for btn in self.buttons:
            if abs(x - btn.center_x) <= btn.width / 2 and abs(y - btn.center_y) <= btn.height / 2:
                if btn.label == "НАЧАТЬ ИГРУ":
                    if self.selected_character:
                        print(f"Запуск игры с персонажем ID: {self.selected_character}")
                        # Здесь будет переход на основную карту
                    else:
                        print("Сначала выберите персонажа!")
                elif btn.label == "НАЗАД":
                    print("Возврат в стартовое меню...")
                    # Здесь будет переход в стартовое меню
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            # Выбор предыдущего персонажа
            if self.selected_character:
                new_id = self.selected_character - 1
                if new_id < 1:
                    new_id = len(self.character_slots)
                self._select_character(new_id)
        
        elif key == arcade.key.RIGHT:
            # Выбор следующего персонажа
            if self.selected_character:
                new_id = self.selected_character + 1
                if new_id > len(self.character_slots):
                    new_id = 1
                self._select_character(new_id)
        
        elif key == arcade.key.SPACE:
            # Подтверждение выбора - запуск игры
            if self.selected_character:
                print(f"Запуск игры с персонажем ID: {self.selected_character}")
                # Здесь будет переход на основную карту
        
        elif key == arcade.key.ESCAPE:
            # Возврат в стартовое меню
            print("Возврат в стартовое меню...")
            # Здесь будет переход в стартовое меню
    def _select_character(self, character_id):
        """Выбирает персонажа по ID"""
        for slot in self.character_slots:
            slot.is_selected = (slot.character_id == character_id)
        self.selected_character = character_id
        print(f"Выбран персонаж ID: {character_id}")