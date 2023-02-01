import pygame

import lib.sprite
import lib.globals

import lib.sprite.explosion

bulletBoundary = pygame.Rect(-30, -30, 384 + 60, 448 + 60)

class Bullet(lib.sprite.Sprite):
    damage: int = 0
    size: float = 0
    speedRadius: float = 0

    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.speed = pygame.Vector2()
        self.boundary = bulletBoundary

    def update(self, *args, **kwargs) -> None:
        self.speed.from_polar((self.speedRadius, -self.angle - 90))

        super().update(*args, **kwargs)

        if self.outOfBoundary:
            self.kill()

    def explode(self) -> None:
        self.kill()
        lib.sprite.explosion.ExplosionBullet(self.position)
