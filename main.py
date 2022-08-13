# Space Invaders Game

import os
import pygame
import random
import time

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Images Load
RED_SPACE_SHIP = pygame.image.load("assests/pixel_ship_red_small.png")
GREEN_SPACE_SHIP=pygame.image.load("assests/pixel_ship_green_small.png")
BLUE_SPACE_SHIP=pygame.image.load("assests/pixel_ship_blue_small.png")

# Player Ship
YELLOW_SPACE_SHIP=pygame.image.load("assests/testpic.png").convert_alpha()

YELLOW_SPACE_SHIP=pygame.transform.scale(YELLOW_SPACE_SHIP, (100, 100))
#YELLOW_SPACE_SHIP.set_colorkey(0, 0, 0)

# Lasers
RED_LASER=pygame.image.load(os.path.join("assests", "pixel_laser_red.png"))
GREEN_LASER=pygame.image.load(os.path.join("assests", "pixel_laser_green.png"))
BLUE_LASER=pygame.image.load(os.path.join("assests", "pixel_laser_blue.png"))
YELLOW_LASER=pygame.image.load(
    os.path.join("assests", "pixel_laser_yellow.png"))

# Background
BG=pygame.image.load(os.path.join("assests", "background-black.png"))


class Ship:
    def __init__(self, x, y, health = 100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    # pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, 50, 50))


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img=YELLOW_SPACE_SHIP
        self.laser_img=YELLOW_LASER
        # Pixel Perfect Collision
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health


def main():
    run=True
    FPS=70
    level=1
    lives=6
    player_velo=5
    main_font=pygame.font.SysFont("cominsans", 50)
    player=Player(300, 650)
    clock=pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # Draw text
        lives_label=main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        level_label=main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        player.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        # Exit Funtion
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        # Player Movement
        keys=pygame.key.get_pressed()
        if (
            keys[pygame.K_a] and player.x - player_velo > 0
        ):  # left
            player.x -= player_velo
        if (
            keys[pygame.K_d] and player.x + player_velo + 50 < WIDTH
        ):  # right
            player.x += player_velo
        if keys[pygame.K_w] and player.y - player_velo > 0:  # up
            player.y -= player_velo
        if (
            keys[pygame.K_s] and player.y + player_velo + 50 < HEIGHT
        ):  # down
            player.y += player_velo


main()
