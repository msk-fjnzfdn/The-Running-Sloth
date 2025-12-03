from constants import *

class StartManuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.csscolor.DARK_SLATE_GRAY

        self.logo_texture = arcade.load_texture("assets/pictures/trs_name.png")
        self.logo_sprite = arcade.Sprite(self.logo_texture, scale=1)
        self.logo_sprite.center_x = 220
        self.logo_sprite.center_y = WINDOW_HEIGHT - 100

        self.manager = arcade.gui.UIManager()

        self.switch_menu_button = arcade.gui.UIFlatButton(text="Pause", width=250)

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
        menu_view = StartManuView1()
        self.window.show_view(menu_view)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.logo_sprite)
        self.manager.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            game = StartManuView1()
            self.window.show_view(game)

            """
            self.window.set_fullscreen(not self.window.fullscreen)

            if self.window.fullscreen:
                self.logo_sprite.center_y = WINDOW_HEIGHT + 70
            else:
                self.logo_sprite.center_y = WINDOW_HEIGHT - 100
            """

    def on_key_release(self, key, modifiers):
        pass

    
    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

class StartManuView1(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.csscolor.GREEN

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
            game = StartManuView()
            self.window.show_view(game)
            """
            self.window.set_fullscreen(not self.window.fullscreen)

            if self.window.fullscreen:
                self.logo_sprite.center_y = WINDOW_HEIGHT + 70
            else:
                self.logo_sprite.center_y = WINDOW_HEIGHT - 100
            """
            

    def on_key_release(self, key, modifiers):
        pass