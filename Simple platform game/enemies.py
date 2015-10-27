"""
Module for managing enemies.
"""
import pygame
import player

from spritesheet_load import SpriteSheet

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

FISH       = (201, 0, 60, 45)
MAIN_ENEMY = (528, 147, 51, 73)
BUG        = (141, 248, 58, 34)
BEE        = (315, 353, 56, 48)

class Enemy(pygame.sprite.Sprite):
    """ Enemies """
    change_x = 0
    change_y = 0

    # Enemies movement boundaries
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None

    def __init__(self, sprite_sheet_data):
        """ Enemy constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("enemies.png")
        # Grab the image for this enemy
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        # Get rect for collisions
        self.rect = self.image.get_rect()

        # Flag main enemy
        self.main_enemy = False

    def update(self):
        """ Move the regular enemies and main enemy.
            If the player is in the way, enemy will kill player.
            Assumes that enemies can hit only player
            Main enemy moves towards player """

        # Movement of regular enemies
        if not self.main_enemy:
            # Move left/right/up/down
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # Check the boundaries and see if we need to reverse
            # direction and flip the image.
            if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
                self.change_y = -self.change_y

            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
                self.change_x = -self.change_x
                self.image = pygame.transform.flip(self.image, True, False)

        # Movement for main enemy
        else:
            if self.player.rect.y > self.rect.y:
                self.rect.y += self.change_y
            if self.player.rect.y < self.rect.y:
                self.rect.y -= self.change_y
            if self.player.rect.x > self.rect.x:
                self.rect.x += self.change_x
            if self.player.rect.x < self.rect.x:
                self.rect.x -= self.change_x

        # See if we hit the player and kill him if so
        hit = pygame.sprite.collide_rect(self, self.player)

        if hit:
            self.player.dead = True