import arcade
import random
import math

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Soul Knight Clone"
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.health = 100
        self.coins = 0
        self.weapon = "Pistol"
        self.shoot_cooldown = 0

    def update(self):
        # Обработка перезарядки оружия
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/animated_characters/zombie/zombie_idle.png", 0.5)
        self.center_x = x
        self.center_y = y
        self.health = 30
        self.speed = ENEMY_SPEED

    def follow_player(self, player_sprite):
        # Простой AI для следования за игроком
        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)
            
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)

class Bullet(arcade.Sprite):
    def __init__(self, x, y, angle):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.5)
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.change_x = math.cos(math.radians(angle)) * BULLET_SPEED
        self.change_y = math.sin(math.radians(angle)) * BULLET_SPEED

class SoulKnightGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        
        # Используем SpriteList для всех объектов
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.wall_list = None
        self.coin_list = None
        
        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False

    def setup(self):
        # Создание SpriteList
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        
        # Создание игрока
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)
        
        # Создание стен
        for x in range(0, SCREEN_WIDTH + 64, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
            
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT - 32
            self.wall_list.append(wall)
            
        for y in range(200, SCREEN_HEIGHT - 64, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
            wall.center_x = 100
            wall.center_y = y
            self.wall_list.append(wall)
            
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
            wall.center_x = SCREEN_WIDTH - 100
            wall.center_y = y
            self.wall_list.append(wall)
        
        # Создание врагов
        for i in range(100):
            enemy = Enemy(
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(100, SCREEN_HEIGHT - 100)
            )
            self.enemy_list.append(enemy)
        
        # Создание монет
        for i in range(10):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.3)
            coin.center_x = random.randint(100, SCREEN_WIDTH - 100)
            coin.center_y = random.randint(100, SCREEN_HEIGHT - 100)
            self.coin_list.append(coin)
        
        # Создание физического движка
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        self.clear()
        
        # Отрисовка всех объектов через SpriteList
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        # Отрисовка HUD
        arcade.draw_text(f"Health: {int(self.player_sprite.health)}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Coins: {self.player_sprite.coins}", 10, SCREEN_HEIGHT - 60, arcade.color.GOLD, 16)
        arcade.draw_text(f"Weapon: {self.player_sprite.weapon}", 10, SCREEN_HEIGHT - 90, arcade.color.WHITE, 16)
        
        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                           arcade.color.RED, 48, anchor_x="center")

    def on_update(self, delta_time):
        if self.game_over:
            return
            
        # Обновление игрока без передачи delta_time
        self.player_sprite.update()
        
        # Обновление остальных списков (Arcade сам обрабатывает delta_time для SpriteList)
        self.bullet_list.update()
        self.physics_engine.update()
        
        # Обновление врагов
        for enemy in self.enemy_list:
            enemy.follow_player(self.player_sprite)
        
        # Проверка столкновений пуль с врагами
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                bullet.remove_from_sprite_lists()
                enemy.health -= 10
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()
                    # Шанс выпадения монеты
                    if random.random() < 0.3:
                        coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.3)
                        coin.center_x = enemy.center_x
                        coin.center_y = enemy.center_y
                        self.coin_list.append(coin)
        
        # Проверка столкновений игрока с монетами
        coins_collected = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_collected:
            coin.remove_from_sprite_lists()
            self.player_sprite.coins += 1
        
        # Проверка столкновений игрока с врагами
        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            self.player_sprite.health -= 0.5
            if self.player_sprite.health <= 0:
                self.game_over = True
        
        # Удаление пуль за пределами экрана
        for bullet in self.bullet_list:
            if (bullet.center_x < 0 or bullet.center_x > SCREEN_WIDTH or
                bullet.center_y < 0 or bullet.center_y > SCREEN_HEIGHT):
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.player_sprite.shoot_cooldown == 0:
            # Создание пули
            angle = math.degrees(math.atan2(y - self.player_sprite.center_y, 
                                          x - self.player_sprite.center_x))
            bullet = Bullet(self.player_sprite.center_x, self.player_sprite.center_y, angle)
            self.bullet_list.append(bullet)
            self.player_sprite.shoot_cooldown = 15

def main():
    window = SoulKnightGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()