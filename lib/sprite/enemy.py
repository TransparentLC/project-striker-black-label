import collections
import importlib
import random
import os
import pygame
import typing

import lib.globals
import lib.sprite
import lib.sprite.debris
import lib.sprite.explosion
import lib.sprite.player
import lib.sprite.item
import lib.utils

r = lib.globals.stgSurface.get_rect()
enemyBoundary = pygame.Rect(-30, -80, r.width + 60, r.height + 110)

class Enemy(lib.sprite.Sprite):
    hitpoint: int
    hitpointBreak: int
    invincibleRemain: int
    explosion: typing.Callable[[pygame.Vector2], lib.sprite.explosion.Explosion]
    debris: list[
        tuple[
            typing.Callable[[pygame.Vector2, float, float], lib.sprite.debris.Debris],
            pygame.Vector2,
            float, float, float, float,
        ]
    ]
    args: typing.Sequence
    explodeSfx: pygame.mixer.Sound

    def __init__(self, scriptModule, scriptArgs = ()) -> None:
        super().__init__(lib.globals.groupEnemy)
        self.interval = 5
        self.hitpoint = 1
        self.hitpointBreak = None
        self.position = pygame.Vector2()
        self.speed = pygame.Vector2()
        self.boundary = enemyBoundary
        self.explosion = None
        self.hitbox = []
        self.debris = []
        self.invincibleRemain = 0
        if os.environ.get('STRIKER_DEBUG_DISABLE_ENEMY_CACHE'):
            importlib.reload(scriptModule)
        self.args = scriptArgs
        self.function: typing.Generator[int, None, None] = None
        self.functionWait = 0
        self.functionsQueue = collections.deque(scriptModule.functions)
        try:
            self.functionDeath = scriptModule.death
        except AttributeError:
            self.functionDeath = None
        self.movementTask: tuple[
            pygame.Vector2,
            int,
            typing.Callable[
                [float, pygame.Vector2, pygame.Vector2],
                pygame.Vector2
            ]
        ] = None
        self.movementCounter = 0
        self.movementFrom: pygame.Vector2 = None
        self.movementQueue: typing.Deque[tuple[
            pygame.Vector2, int,
            typing.Callable[[float, pygame.Vector2, pygame.Vector2], pygame.Vector2],
        ]] = collections.deque()
        self.explodeSfx = None
        self.pointItemNum = 0
        self.blockHyper = False
        self.blockHoming = False

    def update(self) -> None:
        if self.invincibleRemain:
            self.invincibleRemain -= 1
        if self.hitpoint <= 0:
            if self.explosion:
                self.explosion(self.position)
            for d in self.debris:
                d[0](
                    self.position + d[1].rotate(-self.angle),
                    lib.utils.linearInterpolation(random.random(), d[2], d[3]),
                    lib.utils.linearInterpolation(random.random(), d[4], d[5]),
                )
            if self.functionDeath:
                self.functionDeath(self)
            if self.explodeSfx:
                self.explodeSfx.play()

            minwh = min(self.rect.width, self.rect.height)
            for _ in range(self.pointItemNum):
                pos = pygame.Vector2(lib.globals.stgRandom.random() * minwh, 0)
                pos.rotate_ip(lib.globals.stgRandom.random() * 360)
                pos += self.position
                lib.sprite.item.Point(pos)
            self.kill()
            return
        if self.outOfBoundary:
            self.kill()

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.invincibleRemain:
            for h in self.hitboxAbsolute:
                for g in s.hitboxAbsolute:
                    if (h.offset - g.offset).length() < h.size + g.size:
                        s.explode()

        if self.hitpointBreak and self.hitpoint < self.hitpointBreak:
            self.hitpointBreak = None
            self.function = None
            self.functionWait = 0
        if self.functionWait:
            self.functionWait -= 1
        else:
            if not self.function and len(self.functionsQueue):
                self.function = self.functionsQueue.popleft()(self)
            if self.function:
                try:
                    self.functionWait = next(self.function) - 1
                except StopIteration:
                    self.function = None

        if not self.movementTask and self.movementQueue:
            self.movementCounter = 0
            self.movementFrom = pygame.Vector2(self.position)
            self.movementTask = self.movementQueue.popleft()
        if self.movementTask:
            self.movementCounter += 1
            self.position.update(
                self.movementTask[2](
                    self.movementCounter / self.movementTask[1],
                    self.movementFrom,
                    self.movementTask[0],
                )
            )
            if self.movementCounter >= self.movementTask[1]:
                self.movementTask = None

        super().update()
