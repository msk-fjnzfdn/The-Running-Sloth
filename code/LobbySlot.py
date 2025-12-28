import arcade
import os

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
COLOR_SELECTION_RECT = (255, 215, 0, 80)
COLOR_DISABLED = (80, 80, 100, 150)  # Цвет для заблокированных персонажей
COLOR_LOCKED = (60, 60, 80)  # Цвет для заблокированных слотов
COLOR_BUTTON_DEFAULT = (100, 100, 100)  # Серый цвет для кнопок по умолчанию


class LobbySlot:
    def __init__(self, x, y, character_id, name, description, is_unlocked=True):
        self.center_x = x
        self.center_y = y
        self.character_id = character_id
        self.name = name
        self.description = description
        self.is_selected = False
        self.is_hovered = False
        self.is_unlocked = is_unlocked  # Флаг разблокирован ли персонаж
        self.color = COLOR_UNSELECTED if is_unlocked else COLOR_LOCKED
        
        # SpriteList для отрисовки спрайта
        self.sprite_list = arcade.SpriteList()
        
        # Загружаем спрайт для персонажа
        self.sprite = None
        if self.character_id == 1 and self.is_unlocked:
            # Проверяем существование файла
            if os.path.exists("assets/resource_packs/default/alchimic/Default_alchimic_png.png"):
                self.sprite = arcade.Sprite("assets/resource_packs/default/alchimic/Default_alchimic_png.png", scale=1.4)
                
            else:
                # Если файл не найден, создаем текстовую метку
                print("Внимание: файл HA.png не найден!")
                self.sprite = None
        else:
            self.sprite = None
        
        if self.sprite:
            self.sprite.center_x = x
            self.sprite.center_y = y + 120
            self.sprite_list.append(self.sprite)
        
        # Создаем текстовые объекты заранее
        self.text_code = arcade.Text(
            "",
            x, y + 40,
            arcade.color.WHITE, 14,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_subcode = arcade.Text(
            "",
            x, y + 20,
            arcade.color.LIGHT_GRAY, 12,
            anchor_x="center", anchor_y="center"
        )
        
        self.text_name = arcade.Text(
            name,
            x, y - 70,
            arcade.color.WHITE if is_unlocked else COLOR_LOCKED, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_desc = arcade.Text(
            description,
            x, y - 100,
            (arcade.color.LIGHT_GRAY if is_unlocked else COLOR_LOCKED), 14,
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
        
        # Текст "ЗАБЛОКИРОВАНО" для неразблокированных персонажей
        self.text_locked = arcade.Text(
            "ЗАБЛОКИРОВАНО",
            x, y + 90,
            (180, 60, 60), 18,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
    def draw(self):
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
        
        # Рисуем спрайт или кружок
        if self.sprite:
            self.sprite_list.draw()
        else:
            # Если спрайт не загружен, рисуем кружок
            arcade.draw_circle_filled(
                self.center_x, self.center_y + 40,
                60,
                (100, 150, 200) if self.character_id == 1 else 
                (200, 100, 150) if self.character_id == 2 else
                (150, 200, 100)
            )
            
            # Если файл HA.png не найден, показываем текст
            if self.character_id == 1 and self.is_unlocked:
                arcade.draw_text(
                    "HA",
                    self.center_x, self.center_y + 40,
                    arcade.color.WHITE, 36,
                    anchor_x="center", anchor_y="center",
                    bold=True
                )
        
        # Отображаем заранее созданные текстовые объекты
        self.text_code.draw()
        self.text_subcode.draw()
        self.text_name.draw()
        self.text_desc.draw()
        
        # Индикатор выбора
        if self.is_selected:
            self.text_selected.draw()
        
        # Показываем "ЗАБЛОКИРОВАНО" для неразблокированных персонажей
        if not self.is_unlocked:
            self.text_locked.draw()
