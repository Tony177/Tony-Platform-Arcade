# Creating the game's window
# Author : Tony177

import arcade

# Costant used to represent the window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Platform Game"

# Constants used to scale the sprites from their original size
CHARACTER_SCALING = 0.7
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Costant used to establish the player's sprite speed (pixel per frame)
PLAYER_MOVEMENT_SPEED = 3.5
GRAVITY = 1
PLAYER_JUMP_SPEED = 14

# Map Starting Point
PLAYER_START_X = 64
PLAYER_START_Y = 192

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 700
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = CHARACTER_SCALING
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture(
            "images/player_2/player_stand.png", flipped_horizontally=True)
        self.textures.append(texture)
        texture = arcade.load_texture("images/player_2/player_stand.png")
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]


class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
        self.score = 0

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.physics_engine = None
        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover1.wav")
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def setup(self):
        # This function permit the restart of the game

        # Create the Sprite lists
        # Spatial hash speed up collision detection but slow down movement
        # The player move often so don't use Spatial Hash

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.death_list = arcade.SpriteList(use_spatial_hash=True)
        self.background_list = arcade.SpriteList(use_spatial_hash=True)

        # Keep track of the score
        self.score = 0

        # Set up the player
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Name of map file to load
        map_name = "maps/chapter1.tmx"
        # Name of the layers
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'
        death_layer_name = 'Death'
        background_layer_namer = 'Background'

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(
            my_map, coins_layer_name, TILE_SCALING)
        self.death_list = arcade.tilemap.process_layer(
            my_map, death_layer_name, TILE_SCALING)
        self.background_list = arcade.process_layer(
            my_map, background_layer_namer, TILE_SCALING)
        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        # Render the game

        arcade.start_render()

        # Code to draw the screen goes here
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.background_list.draw()
        self.death_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, SCREEN_HEIGHT-50,
                         arcade.csscolor.WHITE, 36)

    def on_key_press(self, key, modifiers):
        # Called when a key is pressed

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        # Called when a key is released

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # Faces sprite texture left or right
        self.player_sprite.update()
        # Physics engine movemente logic

        self.physics_engine.update()
        # See if hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
        # Loop through each coin we hit (if any), remove it and play a sound
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)

        if (arcade.check_for_collision_with_list(self.player_sprite, self.death_list) or self.player_sprite.center_y < -100):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed = True
            arcade.play_sound(self.game_over)
        # Track if we need to change the viewport
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
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
