
"""
GameEngine: owns the player, coins, and obstacles.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_OBSTACLES = 4
STARTING_LIVES = 3

COIN_TYPES = [
    (1, (156, 101, 54)),
    (3, (192, 192, 192)),
    (5, (255, 215, 0)),
]


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self._was_colliding = False
        self.obstacles = []

        for _ in range(NUM_OBSTACLES):
            self.obstacles.append(self._random_obstacle())

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        value, color = random.choice(COIN_TYPES)
        return Coin(x=x, y=y, radius=12, value=value, color=color)

    def _random_obstacle(self):
        width = 60
        height = 30

        while True:
            x = random.randint(20, WIDTH - width - 20)
            y = random.randint(20, HEIGHT - height - 20)
            obstacle = Obstacle(x, y, width, height)

            if obstacle.rect.colliderect(self.player.get_rect()):
                continue

            if any(obstacle.rect.colliderect(coin.get_rect()) for coin in self.coins):
                continue

            if any(obstacle.rect.colliderect(other.rect) for other in self.obstacles):
                continue

            return obstacle

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed

        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if self.game_over:
            return

        collected = check_collection(self.player, self.coins)

        for coin in collected:
            self.score += coin.value

        collected_ids = {id(coin) for coin in collected}
        self.coins = [
            coin for coin in self.coins
            if id(coin) not in collected_ids
        ]

        player_rect = self.player.get_rect()
        colliding = any(
            player_rect.colliderect(obstacle.rect)
            for obstacle in self.obstacles
        )

        if colliding and not self._was_colliding:
            self.lives = max(0, self.lives - 1)

            if self.lives == 0:
                self.game_over = True

        self._was_colliding = colliding

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface, self.player, self.coins, self.obstacles
        )
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 35))

        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER")

