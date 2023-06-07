import pygame
import random

import lib.globals
import lib.sprite
import lib.textures
import lib.utils

class Explosion(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(lib.globals.groupParticle)
        self.position = position
        self.speed = pygame.Vector2()
        self.interval = 5

    def update(self) -> None:
        super().update()

        if self.frameCounter > len(self.textures) * self.interval:
            self.kill()

class ExplosionBullet(Explosion):
    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2 = pygame.Vector2(0, 0), large: bool = False) -> None:
        super().__init__(position + pygame.Vector2(random.randint(-3, 3), random.randint(-3, 3)))
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-bullet-{i}-2x' if large else f'explode-bullet-{i}'] for i in range(3))
        self.interval = 5
        self.speed = speed

class ExplosionPlaneSmallA(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-plane-a-{i}'] for i in range(8))

class ExplosionPlaneSmallB(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-plane-b-{i}'] for i in range(8))

class ExplosionPlaneMediumA(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-plane-c-{i}'] for i in range(8))

class ExplosionPlaneMediumB(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-plane-d-{i}'] for i in range(8))

class ExplosionPlaneLarge(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.EXPLOSION[f'explode-plane-e-{i}'] for i in range(8))

class ExplosionPlayerA(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.PLAYER[f'explode-player-a-{i}'] for i in range(15))

class ExplosionPlayerB(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(lib.textures.PLAYER[f'explode-player-b-{i}'] for i in range(15))

class Charge(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(lib.globals.groupParticle)
        self.delay = (random.randint(0, 80), random.randint(5, 10), random.randint(10, 30), random.randint(5, 10))
        self.delayCounter = tuple(sum(self.delay[:i+1]) for i in range(len(self.delay)))
        self.speed = pygame.Vector2(0, random.random() * 2 + 2).rotate(random.randint(0, 360))
        self.position = position - self.speed * sum(self.delay[:3])
        self.textures = (
            lib.textures.EXPLOSION[random.choice((
                'charge-a',
                'charge-b',
                'charge-c',
                'charge-d',
                'charge-e',
                'charge-f',
            ))].copy(),
        )
        self.textures[0].set_alpha(0)

    def update(self) -> None:
        super().update()

        if self.frameCounter < self.delayCounter[0]:
            self.textures[0].set_alpha(0)
        elif self.frameCounter < self.delayCounter[1]:
            self.textures[0].set_alpha(round(255 * (self.frameCounter - self.delay[0]) / self.delay[1]))
        elif self.frameCounter < self.delayCounter[2]:
            pass
        elif self.frameCounter < self.delayCounter[3]:
            self.textures[0].set_alpha(round(255 * (1 - (self.frameCounter - self.delayCounter[2]) / self.delay[3])))
            self.speed.update(0, 0)
        else:
            self.kill()
