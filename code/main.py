from constants import *
from start_menu import *
from mainlobby import *
from game_start import *


class GameMainWindow(arcade.Window):
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        try:
            with open("code/settings.json", "r", encoding="utf-8") as f:
                self.user_settings = json.load(f)
            print(f'Настройки загружены: {self.user_settings}')
        except Exception:
            print("❗Файл настроек не был загружен")
            print("↳Применены настройки по умолчанию")
            self.user_settings = {
                "name": "The running sloth",
                "fullscreen": False,
                "music_volume": 0.3
            }


def main():
    window = GameMainWindow(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.set_icon(pyglet_load("assets/pictures/trs_logo.png"))
    first_screen = StartMenuView()
    window.show_view(first_screen)
    arcade.run()


if __name__ == "__main__":
    main()
