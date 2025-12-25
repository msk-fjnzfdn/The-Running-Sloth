from constants import *


class StartManuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (128, 128, 128)
        self.start_radius = 50
        self.circle_change = 1
        self.colors = [(128, 128, 128), (129, 129, 129)]
        self.logo_texture = arcade.load_texture("assets/pictures/trs_name.png")
        self.logo_sprite = arcade.Sprite(self.logo_texture, scale=1)
        self.logo_sprite.center_x = 220
        self.logo_sprite.center_y = WINDOW_HEIGHT - 100
        self.circle_radius = [self.start_radius, 0]
        self.manager = arcade.gui.UIManager()

        self.switch_menu_button = arcade.gui.UIFlatButton(
            text="Pause", width=250)

        self.switch_menu_button.on_click = self.on_click_switch_button

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.switch_menu_button,
        )
        """
        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )
        """

    def on_click_switch_button(self, event):
        print("foo")

    def on_update(self, delta_time):
        if self.circle_radius[0] >= min(self.height, self.width):
            del self.circle_radius[0]
            del self.colors[0]
        for i in range(len(self.circle_radius)):
            self.circle_radius[i] += self.circle_change

        if self.circle_radius[-1] >= self.start_radius:
            self.circle_radius.append(0)
            color = (
                128, 128, 128) if self.colors[-1] == (129, 129, 129) else (129, 129, 129)
            self.colors.append(color)

    def on_draw(self):
        self.clear()
        for ind, rad in enumerate(self.circle_radius):
            arcade.draw_circle_filled(self.width // 2, self.height // 2, rad, self.colors[ind])
        arcade.draw_sprite(self.logo_sprite)
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            #game = StartManuView1()
            #self.window.show_view(game)
            self.window.set_fullscreen(not self.window.fullscreen)

            if self.window.fullscreen:
                self.logo_sprite.center_y = WINDOW_HEIGHT + 70
            else:
                self.logo_sprite.center_y = WINDOW_HEIGHT - 100


    def on_key_release(self, key, modifiers):
        pass

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()