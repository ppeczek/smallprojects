"""
Simple platformer main file
"""

import pygame

import constants
import levels

from player import Player

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer training")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # Load active sprites and set level for player
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    # Player starting position
    player.rect.x = 320
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP and player.level.underwater:
                    player.swim_up()
                elif event.key == pygame.K_UP and not player.level.underwater:
                    player.jump()
                if event.key == pygame.K_DOWN:
                    player.swim_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop_x()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop_x()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop_y()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop_y()

            # If player is dead and mouse is clicked - start game again
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.dead:
                    main()

        # Check if player crossed gameplay boundaries (down, up, left)
        if player.rect.y >= 510:
            player.rect.y = 510
        if player.rect.y <= 0:
            player.rect.y = 0
        if player.rect.x <= 0:
            player.rect.x = 0

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500 and current_level.world_shift > -2400:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side and there is world to shift, shift the world right (+x)
        if player.rect.x <= 120 and current_level.world_shift <= 0:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit and player.rect.y == 0:
            player.rect.x = 120
            player.rect.y = 480
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # If the player wins - go to game won
        if current_level_no == 1 and current_position < -1850:
            current_level = levels.GameWon(player)
            active_sprite_list.remove(player)

        # If the player dies - go to game over
        if player.dead:
            current_level = levels.GameOver(player)
            active_sprite_list.remove(player)

        # Draw level and sprites
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Update the screen .
        pygame.display.flip()

    # Exit
    pygame.quit()

if __name__ == "__main__":
    main()
