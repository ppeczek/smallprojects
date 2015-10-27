import pygame

import constants
import platforms
import enemies
import random

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None

    # Flag is level is underwater (changes gravity
    # and animation)
    underwater = False

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    # Text displayed in level
    text = None

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        screen.fill(constants.WHITE)

        # Draw the background
        # If there is the background shift it less than sprites
        # to give a feeling of depth.
        if self.background:
            screen.blit(self.background,(self.world_shift // 3, 0))

        # Draw the text if there is any
        if self.text:
            center_x = (constants.SCREEN_WIDTH // 2) - (self.text.get_width() // 2)
            center_y = (constants.SCREEN_HEIGHT // 2) - (self.text.get_height() // 2)
            screen.blit(self.text, [center_x, center_y])

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

# Create platforms and enemies for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("underwater.jpg").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -900
        self.underwater = True

        # Array with type of platform, and x, y location of the platform.
        level = [[platforms.UNDERWATER_STONE, 400, 472],
                 [platforms.UNDERWATER_STONE, 370, 100],
                 [platforms.UNDERWATER_STONE, 570, 250],
                 [platforms.UNDERWATER_STONE, 810, 340],
                 [platforms.UNDERWATER_STONE, 810, 120],
                 [platforms.UNDERWATER_STONE, 1050, 480],
                 [platforms.UNDERWATER_STONE, 1350, 200],
                 [platforms.UNDERWATER_STONE, 1350, 328],
                 [platforms.UNDERWATER_STONE, 1478, 200],
                 [platforms.UNDERWATER_STONE, 1478, 328],
                 [platforms.UNDERWATER_STONE, 1060, 0]]

        for i in range(5):
            level.append([platforms.UNDERWATER_STONE, 2000, i * 128])
            level.append([platforms.UNDERWATER_STONE, 2128, i * 128])
        for i in range(3):
            level.append([platforms.UNDERWATER_STONE, 1734, i * 128])

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add main enemy
        sprite = enemies.Enemy(enemies.MAIN_ENEMY)
        sprite.rect.x = 10
        sprite.boundary_left = 0
        sprite.boundary_right = -1000
        sprite.change_x = 1
        sprite.rect.y = 10
        sprite.boundary_top = 0
        sprite.boundary_bottom = 550
        sprite.change_y = 1
        sprite.player = self.player
        sprite.level = self
        sprite.main_enemy = True
        self.enemy_list.add(sprite)

        # Add regular enemies
        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 400
        sprite.boundary_left = 350
        sprite.boundary_right = 450
        sprite.change_x = -1
        sprite.rect.y = 372
        sprite.boundary_top = 230
        sprite.boundary_bottom = 450
        sprite.change_y = 1
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 735
        sprite.rect.y = 372
        sprite.boundary_left = 734
        sprite.boundary_right = 796
        sprite.boundary_top = 50
        sprite.boundary_bottom = 550
        sprite.change_y = 2
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 1000
        sprite.rect.y = 400
        sprite.boundary_left = 940
        sprite.boundary_right = 1060
        sprite.change_x = -2
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 1600
        sprite.rect.y = 60
        sprite.boundary_left = 1200
        sprite.boundary_right = 1650
        sprite.change_x = -2
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 1300
        sprite.rect.y = 520
        sprite.boundary_left = 1200
        sprite.boundary_right = 1650
        sprite.change_x = -2
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.FISH)
        sprite.rect.x = 1650
        sprite.rect.y = 100
        sprite.boundary_left = 1649
        sprite.boundary_right = 1711
        sprite.boundary_top = 60
        sprite.boundary_bottom = 550
        sprite.change_y = 2
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

# Create platforms and enemies for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("Land.jpg").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -3000

        # Array with type of platform, and x, y location of the platform.
        level = [[platforms.GRASS_LEFT, 500, 550],
                  [platforms.GRASS_MIDDLE, 570, 550],
                  [platforms.GRASS_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 820, 400],
                  [platforms.GRASS_MIDDLE, 890, 400],
                  [platforms.GRASS_RIGHT, 960, 400],
                  [platforms.GRASS_LEFT, 1060, 500],
                  [platforms.GRASS_MIDDLE, 1130, 500],
                  [platforms.GRASS_RIGHT, 1200, 500],
                  [platforms.GRASS_LEFT, 1170, 280],
                  [platforms.GRASS_MIDDLE, 1240, 280],
                  [platforms.GRASS_RIGHT, 1310, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add moving platforms
        block = platforms.MovingPlatform(platforms.GRASS_MIDDLE)
        block.rect.x = 1700
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 470
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.GRASS_MIDDLE)
        block.rect.x = 2000
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 450
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.GRASS_MIDDLE)
        block.rect.x = 2300
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 450
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add main enemy
        sprite = enemies.Enemy(enemies.MAIN_ENEMY)
        sprite.rect.x = 10
        sprite.boundary_left = 0
        sprite.boundary_right = -1000
        sprite.change_x = 1.5
        sprite.rect.y = 10
        sprite.boundary_top = 0
        sprite.boundary_bottom = 550
        sprite.change_y = 1.5
        sprite.player = self.player
        sprite.level = self
        sprite.main_enemy = True
        self.enemy_list.add(sprite)

        # Add regular enemies
        sprite = enemies.Enemy(enemies.BUG)
        sprite.rect.x = 1500
        sprite.boundary_left = 1350
        sprite.boundary_right = 1600
        sprite.boundary_top = 0
        sprite.boundary_bottom = 600
        sprite.change_x = -1
        sprite.rect.y = 566
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BUG)
        sprite.rect.x = 1700
        sprite.boundary_left = 1550
        sprite.boundary_right = 1800
        sprite.boundary_top = 0
        sprite.boundary_bottom = 600
        sprite.change_x = -2
        sprite.rect.y = 566
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BUG)
        sprite.rect.x = 2100
        sprite.boundary_left = 1950
        sprite.boundary_right = 2200
        sprite.boundary_top = 0
        sprite.boundary_bottom = 600
        sprite.change_x = -1
        sprite.rect.y = 566
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BUG)
        sprite.rect.x = 1500
        sprite.boundary_left = 1350
        sprite.boundary_right = 1600
        sprite.boundary_top = 0
        sprite.boundary_bottom = 600
        sprite.change_x = -1
        sprite.rect.y = 566
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BEE)
        sprite.rect.x = 1600
        sprite.boundary_left = 1550
        sprite.boundary_right = 1750
        sprite.boundary_top = 50
        sprite.boundary_bottom = 450
        sprite.change_y = -2
        sprite.rect.y = 100
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BEE)
        sprite.rect.x = 1900
        sprite.boundary_left = 1850
        sprite.boundary_right = 1950
        sprite.boundary_top = 50
        sprite.boundary_bottom = 450
        sprite.change_y = -2
        sprite.rect.y = 400
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BEE)
        sprite.rect.x = 2140
        sprite.boundary_left = 2100
        sprite.boundary_right = 2250
        sprite.boundary_top = 100
        sprite.boundary_bottom = 400
        sprite.change_y = -1
        sprite.rect.y = 110
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

        sprite = enemies.Enemy(enemies.BEE)
        sprite.rect.x = 2570
        sprite.boundary_left = 2550
        sprite.boundary_right = 2650
        sprite.boundary_top = 50
        sprite.boundary_bottom = 500
        sprite.change_y = -2
        sprite.rect.y = 110
        sprite.player = self.player
        sprite.level = self
        self.enemy_list.add(sprite)

# Game over screen
class GameOver(Level):
    """ Definition for Game - over. """

    def __init__(self, player):
        """ Create level Game - over. """

        # Call the parent constructor
        Level.__init__(self, player)

        font = pygame.font.SysFont("serif", 25)
        self.text = font.render("Game Over, click to restart", True, constants.BLACK)

# Game won screen
class GameWon(Level):
    """ Definition for Game won. """

    def __init__(self, player):
        """ Create level Game won. """

        # Call the parent constructor
        Level.__init__(self, player)

        font = pygame.font.SysFont("serif", 25)
        self.text = font.render("Game Won!", True, constants.BLACK)