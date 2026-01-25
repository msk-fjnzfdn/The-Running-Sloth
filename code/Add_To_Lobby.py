from constants import *


class LobbyUIManager:
    def __init__(self, screen_width, screen_height, buttons):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Текст инструкций
        self.instruction_texts = []

        # Заголовки
        self.title_text = None
        self.subtitle_text = None

        # Тексты для статистики
        self.selected_title_text = None
        self.stats_texts = []

        # Кнопки
        self.button_texts = []

        # Инициализация UI
        self._initialize_ui()

        # Создание текстов для кнопок
        self._create_button_texts(buttons)

    def _initialize_ui(self):
        # Создаем заголовки
        self.title_text = arcade.Text(
            "THE RUNNING SLOTH",
            self.screen_width // 2,
            self.screen_height - 50,
            COLOR_SELECTED,  # Изменено с COLOR_UI_TEXT на COLOR_SELECTED
            56,
            anchor_x="center",
            font_name="Kenney Blocks",
            bold=True
        )

        # Подзаголовок "ЛОББИ ВЫБОРА ПЕРСОНАЖА"
        self.subtitle_text = arcade.Text(
            "ЛОББИ ВЫБОРА ПЕРСОНАЖА",
            self.screen_width // 2,
            self.screen_height - 90,
            (200, 200, 255), 32,
            anchor_x="center"
        )

        # Инструкции оформлены так же как подзаголовок
        instruction_y = self.screen_height - 140  # Ниже подзаголовка

        # Первая строка инструкций (как подзаголовок)
        self.instruction_texts.append(
            arcade.Text(
                "ДОБРО ПОЖАЛОВАТЬ В ЛОББИ ПЕРСОНАЖЕЙ",
                self.screen_width // 2,
                instruction_y,
                (200, 200, 255), 32,  # Тот же цвет и размер что у подзаголовка
                anchor_x="center", anchor_y="center"
            )
        )

        # Вторая строка инструкций
        self.instruction_texts.append(
            arcade.Text(
                "Выберите персонажа для начала игры",
                self.screen_width // 2,
                instruction_y - 40,
                (200, 200, 255), 24,  # Чуть меньше размер
                anchor_x="center", anchor_y="center"
            )
        )

        # Третья строка инструкций
        self.instruction_texts.append(
            arcade.Text(
                "Доступен только Зориан (остальные заблокированы)",
                self.screen_width // 2,
                instruction_y - 70,
                (200, 200, 255), 24,
                anchor_x="center", anchor_y="center"
            )
        )

        # Четвертая строка инструкций
        self.instruction_texts.append(
            arcade.Text(
                "Нажмите ПРОБЕЛ для подтверждения выбора",
                self.screen_width // 2,
                instruction_y - 100,
                (200, 200, 255), 24,
                anchor_x="center", anchor_y="center"
            )
        )

        # Создаем текстовые объекты для статистики
        stats_x = self.screen_width - 400

        # Заголовок выбранного персонажа (УВЕЛИЧЕН)
        self.selected_title_text = arcade.Text(
            "",
            stats_x, 180,
            COLOR_SELECTED, 26,  # Увеличено с 22 до 26
            anchor_x="left", anchor_y="center",
            bold=True
        )

        # Создаем 3 текстовых объекта для статистики (УВЕЛИЧЕНЫ)
        for i in range(3):
            y_pos = 180 - 40 - i * 30
            self.stats_texts.append(
                arcade.Text(
                    "",
                    stats_x, y_pos,
                    arcade.color.LIGHT_GRAY, 20,  # Увеличено с 16 до 20
                    anchor_x="left", anchor_y="center"
                )
            )

    def _create_button_texts(self, buttons):
        for btn in buttons:
            self.button_texts.append(
                arcade.Text(
                    btn.label,
                    btn.center_x, btn.center_y,
                    (180, 180, 180), 24,
                    anchor_x="center", anchor_y="center",
                    bold=True
                )
            )

    def update_positions(self, scale_factor, offset_x, offset_y, buttons):
        # Обновляем позиции заголовков
        if self.title_text:
            self.title_text.position = (
                self.screen_width / 2 * scale_factor + offset_x,
                (self.screen_height - 50) * scale_factor + offset_y
            )
            self.title_text.font_size = int(56 * scale_factor)

        if self.subtitle_text:
            self.subtitle_text.position = (
                self.screen_width / 2 * scale_factor + offset_x,
                (self.screen_height - 90) * scale_factor + offset_y
            )
            self.subtitle_text.font_size = int(32 * scale_factor)

        # Обновляем позиции инструкций
        instruction_base_y = (self.screen_height - 140) * \
            scale_factor + offset_y

        if len(self.instruction_texts) >= 1:
            self.instruction_texts[0].position = (
                self.screen_width / 2 * scale_factor + offset_x,
                instruction_base_y
            )
            self.instruction_texts[0].font_size = int(32 * scale_factor)

        if len(self.instruction_texts) >= 2:
            self.instruction_texts[1].position = (
                self.screen_width / 2 * scale_factor + offset_x,
                instruction_base_y - 40 * scale_factor
            )
            self.instruction_texts[1].font_size = int(24 * scale_factor)

        if len(self.instruction_texts) >= 3:
            self.instruction_texts[2].position = (
                self.screen_width / 2 * scale_factor + offset_x,
                instruction_base_y - 70 * scale_factor
            )
            self.instruction_texts[2].font_size = int(24 * scale_factor)

        if len(self.instruction_texts) >= 4:
            self.instruction_texts[3].position = (
                self.screen_width / 2 * scale_factor + offset_x,
                instruction_base_y - 100 * scale_factor
            )
            self.instruction_texts[3].font_size = int(24 * scale_factor)

        # Обновляем позиции кнопок и их текста
        for i, btn in enumerate(buttons):
            if btn.label == "НАЧАТЬ ИГРУ":
                btn.center_x = self.screen_width / 2 * scale_factor + offset_x
                btn.center_y = 120 * scale_factor + offset_y
                btn.width = 300 * scale_factor
                btn.height = 60 * scale_factor
            elif btn.label == "НАЗАД":
                btn.center_x = (100 - 20) * scale_factor + offset_x
                btn.center_y = (self.screen_height - 40) * \
                    scale_factor + offset_y
                btn.width = 200 * scale_factor
                btn.height = 50 * scale_factor

            if i < len(self.button_texts):
                self.button_texts[i].position = (btn.center_x, btn.center_y)
                self.button_texts[i].font_size = int(24 * scale_factor)

        # Обновляем позиции статистики
        if self.selected_title_text:
            stats_x = (self.screen_width - 400) * scale_factor + offset_x
            self.selected_title_text.position = (
                stats_x,
                180 * scale_factor + offset_y
            )
            self.selected_title_text.font_size = int(26 * scale_factor)

        for i, stat_text in enumerate(self.stats_texts):
            stats_x = (self.screen_width - 400) * scale_factor + offset_x
            y_pos = (180 - 40 - i * 30) * scale_factor + offset_y
            stat_text.position = (stats_x, y_pos)
            stat_text.font_size = int(20 * scale_factor)

    def draw(self, selected_character, character_slots):
        """
        Отрисовка всех UI элементов
        """
        # Рисуем заголовки
        if self.title_text:
            self.title_text.draw()
        if self.subtitle_text:
            self.subtitle_text.draw()

        # Рисуем инструкции
        for text in self.instruction_texts:
            text.draw()

        # Рисуем информацию о выбранном персонаже
        self._draw_selected_info(selected_character, character_slots)

    def _draw_selected_info(self, selected_character, character_slots):
        if selected_character and self.selected_title_text:
            selected_slot = next(
                (s for s in character_slots if s.character_id == selected_character), None)
            if selected_slot:
                # Увеличенный заголовок "ВЫБРАН:"
                self.selected_title_text.text = f"ВЫБРАН: {selected_slot.name}"
                self.selected_title_text.draw()

                # Увеличенная статистика с пробелами для лучшей читаемости
                stats = {
                    1: ["⚔️    УРОН: ВЫСОКИЙ", "🛡️    ЗАЩИТА: НИЗКАЯ", "⚡    СКОРОСТЬ: ВЫСОКАЯ"],
                    2: ["⚔️    УРОН: ???", "🛡️    ЗАЩИТА: ???", "⚡    СКОРОСТЬ: ???"],
                    3: ["⚔️    УРОН: ???", "🛡️    ЗАЩИТА: ???", "⚡    СКОРОСТЬ: ???"]
                }

                current_stats = stats.get(selected_character, [])

                for i, stat_text in enumerate(self.stats_texts):
                    if i < len(current_stats):
                        stat_text.text = current_stats[i]
                        stat_text.draw()
                    else:
                        stat_text.text = ""

    def draw_ui_text(self, buttons, selected_character):
        for i, btn in enumerate(buttons):
            if btn.is_hovered:
                if btn.label == "НАЧАТЬ ИГРУ" and selected_character:
                    color = (80, 220, 120)
                    text_color = arcade.color.WHITE
                elif btn.label == "НАЗАД":
                    color = (120, 120, 140)
                    text_color = arcade.color.WHITE
                else:
                    color = COLOR_BUTTON_DEFAULT
                    text_color = (180, 180, 180)

                btn.color = color
            else:
                text_color = (180, 180, 180)
                btn.color = COLOR_BUTTON_DEFAULT

            if i < len(self.button_texts):
                self.button_texts[i].color = text_color

        for text in self.button_texts:
            text.draw()

    def update(self, mouse_x, mouse_y, buttons):
        pass
