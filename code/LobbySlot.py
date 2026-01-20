from constants import *
from id1_character import *


SCREEN_TITLE = "The Running Sloth - Character Lobby"

class LobbySlot:
    def __init__(self, x, y, character_id, name, description, is_unlocked=True):
        self.base_x = x  # Базовые координаты для разрешения 1200x800
        self.base_y = y
        self.center_x = x  # Текущие координаты (будут обновляться при масштабировании)
        self.center_y = y
        self.character_id = character_id
        self.name = name
        self.description = description
        self.is_selected = False
        self.is_hovered = False
        self.is_unlocked = is_unlocked
        self.color = COLOR_UNSELECTED if is_unlocked else COLOR_LOCKED
        self.scale_factor = 1.0  # Фактор масштабирования
        self.keys_pressed = ()
        
        # SpriteList для отрисовки спрайта
        self.sprite_list = arcade.SpriteList()
        
        # Загружаем спрайт для персонажа
        self.sprite = None
        if self.character_id == 1 and self.is_unlocked:
            """
            # Проверяем существование файла HA.png
            possible_paths = [
                "HA.png",  # В корневой папке
                "assets/HA.png",  # В папке assets
                "assets/resource_packs/default/alchimic/HA.png",  # В папке с ресурсами
                "assets/resource_packs/default/alchimic/Default_alchimic_png.png",  # Старый путь
                "assets/resource_packs/default/alchimic/static/Default_alchimic_png.png"
            ]
            
            sprite_loaded = False
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        self.sprite = arcade.Sprite(path, scale=1.4)
                        sprite_loaded = True
                        print(f"Загружен спрайт: {path}")
                        break
                    except Exception as e:
                        print(f"Ошибка загрузки {path}: {e}")
            
            if not sprite_loaded:
                print("Внимание: файл alchimic.png не найден! Будут использованы запасные варианты.")
                self.sprite = None
            """
            self.sprite = Hero()
        else:
            self.sprite = None

        if self.sprite:
            self.sprite.center_x = self.center_x
            self.sprite.center_y = self.center_y + 120
            self.sprite_list.append(self.sprite)
        
        # Текст "ZA" для первого персонажа (если нет спрайта)
        self.ha_text = arcade.Text(
            "ZA",
            self.center_x, self.center_y + 40,
            arcade.color.WHITE, 36,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        # Создаем текстовые объекты заранее
        self.text_code = arcade.Text(
            "",
            self.center_x, self.center_y + 40,
            arcade.color.WHITE, 14,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_subcode = arcade.Text(
            "",
            self.center_x, self.center_y + 20,
            arcade.color.LIGHT_GRAY, 12,
            anchor_x="center", anchor_y="center"
        )
        
        self.text_name = arcade.Text(
            name,
            self.center_x, self.center_y - 70,
            arcade.color.WHITE if is_unlocked else COLOR_LOCKED, 20,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        self.text_desc = arcade.Text(
            description,
            self.center_x, self.center_y - 100,
            (arcade.color.LIGHT_GRAY if is_unlocked else COLOR_LOCKED), 14,
            anchor_x="center", anchor_y="center",
            align="center",
            width=180
        )
        
        self.text_selected = arcade.Text(
            "✓ ВЫБРАН",
            self.center_x, self.center_y - 130,
            COLOR_SELECTED, 16,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        # Текст "ЗАБЛОКИРОВАНО" для неразблокированных персонажей
        self.text_locked = arcade.Text(
            "ЗАБЛОКИРОВАНО",
            self.center_x, self.center_y + 90,
            (180, 60, 60), 18,
            anchor_x="center", anchor_y="center",
            bold=True
        )
        
        # Также сохраняем информацию о цвете кружков для каждого персонажа
        self.character_colors = {
            1: (100, 150, 200),   # Синий для Зориана
            2: (200, 100, 150),   # Розовый для второго персонажа
            3: (150, 200, 100)    # Зеленый для третьего персонажа
        }
    
    def update_position(self, scale_factor, offset_x=0, offset_y=0, delta_time: float = 1/60):
        """Обновляет позиции всех элементов слота в соответствии с масштабом и смещением"""
        self.scale_factor = scale_factor
        
        # Масштабируем позиции и добавляем смещение
        self.center_x = self.base_x * scale_factor + offset_x
        self.center_y = self.base_y * scale_factor + offset_y
        
        # Обновляем позицию спрайта
        if self.sprite:
            self.sprite.center_x = self.center_x
            self.sprite.center_y = self.center_y + 120 * scale_factor
            self.sprite.scale = 1.4 * scale_factor
            self.sprite_list.update(delta_time, self.keys_pressed)
            self.sprite_list.update_animation()
        
        # Обновляем позиции текстовых элементов
        self.ha_text.position = (self.center_x, self.center_y + 40 * scale_factor)
        self.ha_text.font_size = int(36 * scale_factor)
        
        self.text_code.position = (self.center_x, self.center_y + 40 * scale_factor)
        self.text_code.font_size = int(14 * scale_factor)
        
        self.text_subcode.position = (self.center_x, self.center_y + 20 * scale_factor)
        self.text_subcode.font_size = int(12 * scale_factor)
        
        self.text_name.position = (self.center_x, self.center_y - 70 * scale_factor)
        self.text_name.font_size = int(20 * scale_factor)
        
        self.text_desc.position = (self.center_x, self.center_y - 100 * scale_factor)
        self.text_desc.font_size = int(14 * scale_factor)
        self.text_desc.width = 180 * scale_factor
        
        self.text_selected.position = (self.center_x, self.center_y - 130 * scale_factor)
        self.text_selected.font_size = int(16 * scale_factor)
        
        self.text_locked.position = (self.center_x, self.center_y + 90 * scale_factor)
        self.text_locked.font_size = int(18 * scale_factor)
        
    def draw(self):
        # Полупрозрачный прямоугольник выделения для выбранного персонажа
        if self.is_selected:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    self.center_x,
                    self.center_y + 10 * self.scale_factor,
                    210 * self.scale_factor,  # Ширина с масштабированием
                    260 * self.scale_factor   # Высота с масштабированием
                ),
                COLOR_SELECTION_RECT
            )
        
        # Затемнение для заблокированных персонажей
        if not self.is_unlocked:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    self.center_x,
                    self.center_y + 10 * self.scale_factor,
                    210 * self.scale_factor,
                    260 * self.scale_factor
                ),
                COLOR_DISABLED
            )
        
        # Рисуем спрайт или кружок
        if self.sprite:
            self.sprite_list.draw()
        else:
            # Если спрайт не загружен, рисуем кружок с масштабированием
            circle_color = self.character_colors.get(self.character_id, (100, 150, 200))
            arcade.draw_circle_filled(
                self.center_x, 
                self.center_y + 40 * self.scale_factor,
                60 * self.scale_factor,
                circle_color
            )
            
            # Если файл не найден, показываем текст (только для разблокированного 1-го персонажа)
            if self.character_id == 1 and self.is_unlocked:
                self.ha_text.draw()
        
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
            
    def is_point_inside(self, x, y):
        """Проверяет, находится ли точка внутри зоны слота (для кликов и ховера)"""
        # Рассчитываем размеры зоны взаимодействия с учетом масштаба
        click_width = 100 * self.scale_factor
        click_height = 125 * self.scale_factor
        
        return (
            abs(x - self.center_x) <= click_width and
            abs(y - self.center_y) <= click_height
        )



