from constants import *


fullscreen=True

class StartManuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.csscolor.DARK_SLATE_GRAY

        self.logo_texture = arcade.load_texture("assets/pictures/trs_name.png")
        self.logo_sprite = arcade.Sprite(self.logo_texture, scale=1)
        self.logo_sprite.center_x = 220
        self.logo_sprite.center_y = WINDOW_HEIGHT - 100
        

        """
        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )
        """
        
    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.logo_sprite)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)

            if self.window.fullscreen:
                self.logo_sprite.center_y = WINDOW_HEIGHT + 70
            else:
                self.logo_sprite.center_y = WINDOW_HEIGHT - 100

    def on_key_release(self, key, modifiers):
        pass
