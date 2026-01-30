from constants import *
from mainlobby import *


class StartMenuView(arcade.View):
    def __init__(self, obj=None):
        super().__init__()
        self.background_color = (128, 128, 128)
        self.start_radius = 50
        self.circle_change = 1
        self.music_player = None
        self.colors = [(128, 128, 128), (130, 130, 130)]
        self.btn_select_sound = arcade.load_sound("assets/music/button_sound.mp3")
        self.logo_texture = arcade.load_texture("assets/pictures/trs_name.png")
        self.escape_sound = arcade.load_sound("assets/music/idk_sound.mp3")
        self.logo_sprite = arcade.Sprite(
        self.logo_texture, scale=0.75, center_x=165, center_y=self.window.height - 75)
        self.music_volume = self.window.user_settings["music_volume"]
        self.circle_radius = [self.start_radius]
        self.manager = arcade.gui.UIManager()
        self.create_btns()
        self._setup_music()

    def set_fullscreen(self):
        self.window.set_fullscreen(not self.window.fullscreen)
        self.window.user_settings["fullscreen"] = not self.window.user_settings["fullscreen"]
        self.save_settings()
        self.update_positions(fullscreen=self.window.fullscreen)

    def switch_btn(self, event=None):
        self.btn_select_sound.play()
        lobby = MainLobby(obj=self)
        self.window.show_view(lobby)

    def close_btn(self, event=None):
        self.escape_sound.play()
        self.save_settings()
        self.window.close()

    def settings_show(self, event=None):
        pass

    def save_settings(self):
        with open("code/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.window.user_settings, f, indent=4, ensure_ascii=False)

    def on_update(self, delta_time):
        if self.circle_radius[0] >= min(self.height, self.width):
            del self.circle_radius[0]
            del self.colors[0]
        for i in range(len(self.circle_radius)):
            self.circle_radius[i] += self.circle_change

        if self.circle_radius[-1] >= self.start_radius:
            self.circle_radius.append(0)
            color = (
                128, 128, 128) if self.colors[-1] == (130, 130, 130) else (130, 130, 130)
            self.colors.append(color)

    def on_draw(self):
        self.clear()
        for ind, rad in enumerate(self.circle_radius):
            arcade.draw_circle_filled(
                self.width // 2, self.height // 2, rad, self.colors[ind])
        arcade.draw_sprite(self.logo_sprite)
        self.manager.draw()
        arcade.draw_line(start_x=self.settings_btn.center_x - self.settings_btn.width // 2 - 5, start_y=self.settings_btn.center_y + self.settings_btn.height // 2 + 5,
                         end_x=self.settings_btn.center_x + self.settings_btn.width // 2 + 5, end_y=self.settings_btn.center_y - self.settings_btn.height // 2 - 5, color=(100, 100, 100), line_width=4)
        arcade.draw_line(start_x=self.settings_btn.center_x - self.settings_btn.width // 2 - 5, start_y=self.settings_btn.center_y - self.settings_btn.height // 2 - 5,
                         end_x=self.settings_btn.center_x + self.settings_btn.width // 2 + 5, end_y=self.settings_btn.center_y + self.settings_btn.height // 2 + 5, color=(100, 100, 100), line_width=4)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.set_fullscreen()

        elif key == arcade.key.ESCAPE:
            self.close_btn()

        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            if self.music_volume < 1.0:
                self.music_volume = min(1.0, self.music_volume + 0.1)
                print(f"Громкость музыки: {int(self.music_volume * 100)}%")
                self.window.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                self._update_music_volume()

        elif key == arcade.key.MINUS:
            if self.music_volume > 0.0:
                self.music_volume = max(0.0, self.music_volume - 0.1)
                print(f"Громкость музыки: {int(self.music_volume * 100)}%")
                self.window.user_settings["music_volume"] = float(
                    int(self.music_volume * 100)) / 100
                self.save_settings()
                self._update_music_volume()

        elif key == arcade.key.M:
            if self.lobby_music:
                if self.music_player:
                    try:
                        arcade.stop_sound(self.music_player)
                        self.music_player = None
                    except Exception as e:
                        print(f"❗Ошибка при остановке музыки: {e}")
                        self.music_player = None
                else:
                    self.music_player = arcade.play_sound(
                        self.lobby_music, volume=self.music_volume, loop=True)

    def on_key_release(self, key, modifiers):
        pass

    def on_show_view(self):
        if self.window.user_settings.get("fullscreen", False):
            self.window.set_fullscreen(True)
        self.update_positions(fullscreen=self.window.fullscreen)
        self.manager.enable()
        if self.lobby_music and not self.music_player:
            self.music_player = arcade.play_sound(
                self.lobby_music, volume=self.music_volume, loop=True)

    def on_hide_view(self):
        self.manager.disable()
        if self.music_player:
            try:
                arcade.stop_sound(self.music_player)
                self.music_player = None
            except:
                pass

    def update_positions(self, fullscreen=False):
        self.logo_sprite.center_y = self.window.height - 100
        if fullscreen:
            self.logo_sprite.scale = 1
            self.logo_sprite.center_y = self.window.height - 100
            self.logo_sprite.center_x = 220
            for x in self.list_btn:
                x.width = 250
                x.center_x = self.window.width // 2
        else:
            self.logo_sprite.scale = 0.75
            self.logo_sprite.center_y = self.window.height - 75
            self.logo_sprite.center_x = 165
            for x in self.list_btn:
                x.width = 200
                x.center_x = self.window.width // 2

    def create_btns(self):
        self.game_btn = arcade.gui.UIFlatButton(
            text="Game", width=200, x=500, y=370)
        self.game_btn.center_x = self.window.width // 2
        self.game_btn.on_click = self.switch_btn
        self.settings_btn = arcade.gui.UIFlatButton(
            text="Settings", width=200, x=500, y=290)
        self.settings_btn.center_x = self.window.width // 2
        self.settings_btn.disabled = True
        self.exit_btn = arcade.gui.UIFlatButton(
            text="Exit", width=200, x=500, y=210)
        self.exit_btn.center_x = self.window.width // 2
        self.exit_btn.on_click = self.close_btn
        self.list_btn = [self.game_btn, self.settings_btn, self.exit_btn]
        self.manager.add(self.game_btn)
        self.manager.add(self.settings_btn)
        self.manager.add(self.exit_btn)

    def _setup_music(self):
        try:
            # Пробуем разные пути к файлу
            music_paths = [
                "assets/music/menu_music.mp3"
            ]
            for path in music_paths:
                if os.path.exists(path):
                    self.lobby_music = arcade.load_sound(path)
                    break

            if self.lobby_music:
                pass
            else:
                print(
                    "❗Файл музыки не найден. Проверьте наличие файла в директории проекта.")

        except Exception as e:
            print(f"❗Ошибка при загрузке музыки: {e}")
    
    def _update_music_volume(self):
        if self.lobby_music and self.music_player:
            try:
                # Останавливаем текущее воспроизведение
                arcade.stop_sound(self.music_player)
                # Перезапускаем с новой громкостью
                self.music_player = arcade.play_sound(
                    self.lobby_music, volume=self.music_volume, loop=True)
            except:
                pass