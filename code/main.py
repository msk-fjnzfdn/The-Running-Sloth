from constants import *
from start_menu import *

class GameMainWindow(arcade.Window):
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)


    def setup(self):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass


def main():
    window = GameMainWindow(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.set_icon(pyglet_load("assets/pictures/trs_logo.png"))
    start_menu = StartManuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()