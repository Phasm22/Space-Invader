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
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, (70, 70))
RED_SPACE_SHIP = pygame.transform.rotate(RED_SPACE_SHIP, 180)

GREEN_SPACE_SHIP = pygame.image.load("assests/pixel_ship_green_small.png")
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, (70, 70))

BLUE_SPACE_SHIP = pygame.image.load("assests/pixel_ship_blue_small.png")
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP, (70, 70))


# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load("assests/testpic.png").convert_alpha()
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP, (100, 100))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assests", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assests", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assests", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assests", "pixel_laser_yellow.png"))

# Background
BG = pygame.image.load(os.path.join("assests", "background-black.png"))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER

        # Pixel Perfect Collision
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 70
    level = 0
    lives = 6
    player_velo = 5
    
    main_font = pygame.font.SysFont("cominsans", 50)
    player = Player(300, 650)
    clock = pygame.time.Clock()

    enemies = []
    wave_length = 5
    enemy_vel = 1

    def redraw_window():
        WIN.blit(BG, (0, 0))
        
        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        
        # Increment level when no emnemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5

            # Enemy Spawn
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

        # Exit Funtion
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velo > 0:  # left
            player.x -= player_velo
        if (
            keys[pygame.K_d] and player.x + player_velo + player.get_width() < WIDTH
        ):  # right
            player.x += player_velo
        if keys[pygame.K_w] and player.y - player_velo > 0:  # up
            player.y -= player_velo
        if (
            keys[pygame.K_s] and player.y + player_velo + player.get_height() < HEIGHT
        ):  # down
            player.y += player_velo

        # Enemy Movement

        for enemy in enemies:
            enemy.move(enemy_vel)


main()
