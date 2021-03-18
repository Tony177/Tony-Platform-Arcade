# Author : Tony177

import arcade
import os
from cryptography.fernet import Fernet

# Costant used to represent the window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Platform Game"

# Constants used to scale the sprites from their original size
CHARACTER_SCALING = 0.8
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Costant used to establish the player's sprite speed and status(pixel per frame)
PLAYER_MOVEMENT_SPEED = 4.5
GRAVITY = 0.9
PLAYER_JUMP_SPEED = 20

# 0 Male - 1 Female - 2 Zombie - 3 Soldier
PLAYER_SPRITE = 0

# Map Starting Point
PLAYER_START_X = 96
PLAYER_START_Y = 192

DEFAULT_VOLUME = 0.6

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 700
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# Index of textures, first element faces left, second faces right
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


def save(save_list: list):
    text = "Start Signature\n"
    for value in save_list:
        text += str(value)
        text += "\n"
    text += "End Signature"
    text = str.encode(text)
    encrypt(text)


def load():
    with open("save.dat", "rb") as file_enc:
        data = file_enc.read()
    decrypted = bytes.decode(decrypt(data))
    load_list = decrypted.split("\n")
    load_list.pop(0)  # Pop first element Start
    load_list.pop(-1)  # Pop last element blank character
    return load_list


def encrypt(file: bytes):
    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(file)
    with open("save.dat", "wb") as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt(file: bytes):
    with open("game_key.key", "rb") as mykey:
        key = mykey.read()
    fernet = Fernet(key)
    original = fernet.decrypt(file)
    return original


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Default texture
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        if PLAYER_SPRITE == 0:  # Male Choosen
            main_path = "images/player_M/male"
        elif PLAYER_SPRITE == 1:  # Female Choosen
            main_path = "images/player_F/female"
        elif PLAYER_SPRITE == 2:  # Zombie Choosen
            main_path = "images/zombie/zombie"
        elif PLAYER_SPRITE == 3:  # Soldier Choosen
            main_path = "images/soldier/soldier"
        else:
            print("Error loading player texture")

        # Loading idle, jump and fall texture
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")
        # Load a left facing texture and a right facing texture.

        # Load textures for walking
        self.walk_textures = []
        texture = load_texture_pair(f"{main_path}_idle.png")
        self.walk_textures.append(texture)
        for i in range(1, 3):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        for i in range(1, 3):
            texture = arcade.load_texture(f"{main_path}_climb{i}.png")
            self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 2:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 2]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        if self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 2:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]


class PauseView(arcade.View):
    def __init__(self, game):
        super().__init__()
        self.game = game  # Return point after Resume Button is pressed

    def setup(self):
        self.resume = arcade.Sprite(
            "images/button/red_button_normal.png",
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT * 3 / 4,
        )
        self.plus_volume = arcade.Sprite(
            "images/button/red_button_normal.png",
            center_x=SCREEN_WIDTH / 2 + 100,
            center_y=SCREEN_HEIGHT * 2 / 4,
        )
        self.minus_volume = arcade.Sprite(
            "images/button/red_button_normal.png",
            center_x=SCREEN_WIDTH / 2 - 100,
            center_y=SCREEN_HEIGHT * 2 / 4,
        )
        self.exit = arcade.Sprite(
            "images/button/red_button_normal.png",
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT * 1 / 4,
        )

    def on_show(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.csscolor.WHITE_SMOKE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()

        self.resume.draw()
        self.plus_volume.draw()
        self.minus_volume.draw()
        self.exit.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        global DEFAULT_VOLUME
        if self.resume.collides_with_point((_x,_y)):
            self.window.show_view(self.game)

        if DEFAULT_VOLUME < 1 and self.plus_volume.collides_with_point((_x,_y)):
            DEFAULT_VOLUME += 0.1
        if DEFAULT_VOLUME > 0 and self.minus_volume.collides_with_point((_x,_y)):
            DEFAULT_VOLUME -= 0.1
        if self.exit.collides_with_point((_x,_y)):
            # TO BE DONE: Save config file and data
            self.window.close()


class StartingView(arcade.View):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_RED)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        # Setting mouse visible to permit selection
        self.window.set_mouse_visible(True)
        # Drawing instruction on starting view
        start_text_title = "Instruction to play:"
        start_text_body = "Press A,D or ARROW LEFT, RIGHT to move \n Press W or ARROW UP or SPACE to jump\n \
            Press S or ARROW DOWN to move down on ladder \n Press ESC to open menu"
        start_text_end = "If you collect 100 coins you get an extra life \n If you lose all the lifes you've lost"
        start_text_begin = "Click with the mouse to start character selection \n Click on one of the four image to select a character"
        arcade.draw_text(
            start_text_title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 350,
            arcade.csscolor.WHITE,
            anchor_x="center",
            anchor_y="top",
            align="center",
            font_size=72,
        )
        arcade.draw_text(
            start_text_body,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.csscolor.WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_size=32,
        )
        arcade.draw_text(
            start_text_end,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.csscolor.WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_size=32,
        )
        arcade.draw_text(
            start_text_begin,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 200,
            arcade.csscolor.WHITE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            font_size=48,
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        character_view = CharacterView()
        character_view.setup()
        self.window.show_view(character_view)


class CharacterView(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_sound = arcade.load_sound("sounds/upgrade2.wav", False)

    def setup(self):
        # Adding all idle images to a sprites list

        X_LEFT = SCREEN_WIDTH * 1 / 4
        X_RIGHT = SCREEN_WIDTH * 3 / 4
        Y_BOTTOM = SCREEN_HEIGHT * 1 / 4
        Y_TOP = SCREEN_HEIGHT * 3 / 4
        self.sprites = []
        self.sprites.append(
            arcade.Sprite(
                "images/player_M/male_idle.png",
                scale=2,
                center_x=X_LEFT,
                center_y=Y_TOP,
            )
        )
        self.sprites.append(
            arcade.Sprite(
                "images/player_F/female_idle.png",
                scale=2,
                center_x=X_RIGHT,
                center_y=Y_TOP,
            )
        )
        self.sprites.append(
            arcade.Sprite(
                "images/zombie/zombie_idle.png",
                scale=2,
                center_x=X_LEFT,
                center_y=Y_BOTTOM,
            )
        )
        self.sprites.append(
            arcade.Sprite(
                "images/soldier/soldier_idle.png",
                scale=2,
                center_x=X_RIGHT,
                center_y=Y_BOTTOM,
            )
        )

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_RED)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()

        sprite_x = []
        sprite_y = []

        for x in self.sprites:
            x.draw()
            # Loading into sprite_x and sprite_y the sprite's coordinate
            sprite_x.append(x.center_x - 50)
            sprite_y.append(x.bottom - 100)

        # Text written under every character sprite
        arcade.draw_text("Male", sprite_x[0], sprite_y[0], arcade.csscolor.WHITE, 64)
        arcade.draw_text("Female", sprite_x[1], sprite_y[1], arcade.csscolor.WHITE, 64)
        arcade.draw_text("Zombie", sprite_x[2], sprite_y[2], arcade.csscolor.WHITE, 64)
        arcade.draw_text("Soldier", sprite_x[3], sprite_y[3], arcade.csscolor.WHITE, 64)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        global PLAYER_SPRITE  # To modify global variable player_sprite
        i = 0
        for sprite in self.sprites:
            # if check_box(sprite, _x, _y):
            if sprite.collides_with_point((_x,_y)):
                arcade.play_sound(self.start_sound)
                PLAYER_SPRITE = i  # Selected the index of the character defined near PLAYER_SPRITE definition
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            # Sliding to the next sprite in list
            i += 1


class GameView(arcade.View):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.background_list = None
        self.death_list = None
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Keep track of the score
        self.picked_coins_x = []
        self.picked_coins_y = []
        self.coins = 0
        self.lifes = 3

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.physics_engine = None

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin2.wav", False)
        self.jump_sound = arcade.load_sound("sounds/jump1.wav", False)
        self.game_over = arcade.load_sound("sounds/gameover3.wav", False)

        # Load the background music for game view
        self.backgroud_sound = arcade.load_sound("musics/funkyrobot.mp3", True)

    def setup(self):
        # This function permit the restart of the game

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.level = 1

        # Create the Sprite lists
        # Spatial hash speed up collision detection but slow down movement
        # The player move often so don't use Spatial Hash

        self.wall_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.death_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)

        # Keep track of the score
        self.coins = 0
        self.lifes = 3

        # Start background music
        self.media_player = self.backgroud_sound.play(volume=DEFAULT_VOLUME, loop=True)

        # Set up the player
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Name of map file to load
        map_name = "maps/chapter1.tmx"
        # Name of the layers
        platforms_layer_name = "Platforms"
        coins_layer_name = "Coins"
        death_layer_name = "Death"
        background_layer_namer = "Background"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(
            map_object=my_map,
            layer_name=platforms_layer_name,
            scaling=TILE_SCALING,
            use_spatial_hash=True,
        )

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(
            my_map, coins_layer_name, TILE_SCALING
        )
        self.death_list = arcade.tilemap.process_layer(
            my_map, death_layer_name, TILE_SCALING
        )
        self.background_list = arcade.process_layer(
            my_map, background_layer_namer, TILE_SCALING
        )

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, GRAVITY
        )
        # After all base setup try load save.dat
        try:
            save = load()
            self.player_sprite.set_position(float(save[0]), float(save[1]))
            self.level = int(save[2])
            self.lifes = int(save[3])
            self.coins = int(save[4])
            # Removed comma from x coordinate list
            coins_to_remove_x = save[5].split(",")
            # Removed first square bracket
            coins_to_remove_x[0] = coins_to_remove_x[0].split("[")[1]
            # Removed last square bracket
            coins_to_remove_x[-1] = coins_to_remove_x[-1].split("]")[0]
            # Removed comma from y coordinate list
            coins_to_remove_y = save[6].split(",")
            # Removed first square bracket
            coins_to_remove_y[0] = coins_to_remove_y[0].split("[")[1]
            # Removed last square bracket
            coins_to_remove_y[-1] = coins_to_remove_y[-1].split("]")[0]
            leng = len(coins_to_remove_x)
            for c in self.coin_list:
                for i in range(leng):
                    if c.center_x == float(coins_to_remove_x[i]):
                        if c.center_y == float(coins_to_remove_y[i]):
                            c.remove_from_sprite_lists()
                            coins_to_remove_y.pop(i)
                            coins_to_remove_x.pop(i)
                            leng = len(coins_to_remove_x)
                            break

        except FileNotFoundError:
            pass


    def on_hide_view(self):
        # When the view is changed do this
        self.media_player.pause()

    def on_draw(self):
        # Render the game
        self.backgroud_sound.set_volume(DEFAULT_VOLUME, self.media_player)
        self.media_player.play()
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

        arcade.start_render()
        self.window.set_mouse_visible(False)

        # Code to draw the screen goes here
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.background_list.draw()
        self.death_list.draw()

        # Draw coins on the screen, scrolling it with the viewport
        coins_text = f"Coins: {self.coins}"
        arcade.draw_text(
            coins_text,
            self.view_left + 10,
            self.view_bottom + SCREEN_HEIGHT - 50,
            arcade.csscolor.WHITE,
            36,
        )
        # Draw lifes left, scrolling it with the viewport
        lifes_text = f"Lifes: {self.lifes}"
        arcade.draw_text(
            lifes_text,
            self.view_left + 10,
            self.view_bottom + SCREEN_HEIGHT - 100,
            arcade.csscolor.WHITE,
            36,
        )

    def process_keychange(self):

        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound, DEFAULT_VOLUME)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        # Called when a key is pressed

        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            # To avoid movement bug set all previous keys to False
            self.up_pressed = False
            self.down_pressed = False
            self.left_pressed = False
            self.right_pressed = False
            # Load Pause Menu
            esc_view = PauseView(self)
            esc_view.setup()
            save_list = []
            save_list.append(self.player_sprite.center_x)
            save_list.append(self.player_sprite.center_y)
            save_list.append(self.level)
            save_list.append(self.lifes)
            save_list.append(self.coins)
            save_list.append(self.picked_coins_x)
            save_list.append(self.picked_coins_y)
            save(save_list)
            self.window.show_view(esc_view)

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        # Called when a key is released

        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False

        self.process_keychange()
    def boundary_check(self):
        changed = False
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            return True
        return False

    def on_update(self, delta_time):

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.coin_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if (
                wall.boundary_right
                and wall.right > wall.boundary_right
                and wall.change_x > 0
            ):
                wall.change_x *= -1
            if (
                wall.boundary_left
                and wall.left < wall.boundary_left
                and wall.change_x < 0
            ):
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if (
                wall.boundary_bottom
                and wall.bottom < wall.boundary_bottom
                and wall.change_y < 0
            ):
                wall.change_y *= -1

        # See if hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        # Loop through each coin we hit (if any), remove it and play a sound
        for coin in coin_hit_list:
            self.picked_coins_x.append(coin.center_x)
            self.picked_coins_y.append(coin.center_y)
            coin.remove_from_sprite_lists()
            self.coins += 1
            arcade.play_sound(self.collect_coin_sound, DEFAULT_VOLUME)
            if self.coins >= 100:
                self.coins -= 100
                self.lifes += 1

        # Starting setting changed to false to avoid UnboundLocalError at 770
        changed = False

        if (
            arcade.check_for_collision_with_list(self.player_sprite, self.death_list)
            or self.player_sprite.center_y < -100
        ):
            self.lifes -= 1
            if self.lifes == 0:
                # TO BE DONE: Implement death view
                pass
            else:
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed = True
                arcade.play_sound(self.game_over, DEFAULT_VOLUME)
        # Track if we need to change the viewport
        if self.boundary_check() or changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(
                self.view_left,
                SCREEN_WIDTH + self.view_left,
                self.view_bottom,
                SCREEN_HEIGHT + self.view_bottom,
            )
        

def main():
    os.chdir(
        os.path.dirname(os.path.realpath(__file__))
    )  # Change working directory to this file's directory
    
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    star_view = StartingView()
    star_view.setup()
    window.show_view(star_view)
    arcade.run()


if __name__ == "__main__":
    main()
