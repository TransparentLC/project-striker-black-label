import enum
import pygame
import random

import lib.bullet
import lib.constants
import lib.globals
import lib.script.enemy.common
import lib.sprite.enemy
import lib.sprite.explosion
import lib.sprite.item
import lib.sound
import lib.utils

class PlayerBulletFlags(enum.IntFlag):
    HOMING = enum.auto()
    LOCKING = enum.auto()
    BULLET_CANCELLING = enum.auto()

bulletSize1Way = 5
bulletSize2Way = 9
bulletSize4Way = 12
bulletSizeHoming = 4

class PlayerBullet(lib.bullet.Bullet):
    def __init__(self, position: pygame.Vector2, texture: pygame.Surface, size: float, speed: float, angle: float, damage: int, flags: int = 0) -> None:
        super().__init__(lib.globals.groupPlayerBullet)
        self.position = pygame.Vector2(position)
        self.textures = (texture,)
        self.size = size
        self.speedRadius = speed
        self.angle = angle
        self.damage = damage
        self.flags = flags
        self.bulletCancelRemain = 2

        if self.flags & PlayerBulletFlags.LOCKING:
            ne = self.nearestEnemy
            if ne:
                self.angle = -pygame.Vector2().angle_to(ne.position - self.position) - 90

    @property
    def nearestEnemy(self) -> 'lib.sprite.enemy.Enemy':
        r = None
        d = float('inf')
        for x in lib.globals.groupEnemy:
            if x.blockHoming:
                continue
            e = self.position.distance_squared_to(x.position)
            if e < d:
                d = e
                r = x
        return r

    def update(self) -> None:
        super().update()

        if self.flags & PlayerBulletFlags.HOMING:
            ne = self.nearestEnemy
            if ne:
                targetAngle = -(ne.position - self.position).as_polar()[1] - 90
                if targetAngle > self.angle + 180:
                    targetAngle -= 360
                elif targetAngle < self.angle - 180:
                    targetAngle += 360
                self.angle = lib.utils.clamp(
                    targetAngle,
                    self.angle - min(3, self.frameCounter * .1),
                    self.angle + min(3, self.frameCounter * .1),
                )

        for s in lib.globals.groupEnemy:
            s: lib.sprite.enemy.Enemy
            for h in s.hitboxAbsolute:
                if (h.offset - self.position).length() < h.size + self.size:
                    if self.flags & PlayerBulletFlags.BULLET_CANCELLING and s.blockHyper:
                        self.damage = 1
                        random.choice((
                            lib.sound.SFX.PLAYER_SHOOT_BLOCK_A,
                            lib.sound.SFX.PLAYER_SHOOT_BLOCK_B,
                        )).play()
                    elif s.invincibleRemain:
                        self.damage = 1
                    else:
                        s.hitpoint -= self.damage
                    return self.explode()

        if self.flags & PlayerBulletFlags.BULLET_CANCELLING:
            self.largeExplode = True
            for b in lib.globals.groupEnemyBullet:
                b: lib.bullet.enemy_bullet.EnemyBullet
                if self.position.distance_squared_to(b.position) < self.size ** 2:
                    lib.sprite.item.PointClear(pygame.Vector2(self.position))
                    lib.globals.maxGetPoint = max(
                        lib.constants.INITIAL_MAXGETPOINT,
                        lib.globals.maxGetPoint - max(4, len(lib.globals.groupEnemyBullet) >> 4)
                    )
                    self.bulletCancelRemain -= 1
                    b.explode()
                    if not self.bulletCancelRemain:
                        return self.explode()

    def explode(self) -> None:
        super().explode()
        lib.globals.score += self.damage * 7
        random.choice((
            lib.sound.SFX.PLAYER_SHOOT_HIT_A,
            lib.sound.SFX.PLAYER_SHOOT_HIT_B,
            lib.sound.SFX.PLAYER_SHOOT_HIT_C,
            lib.sound.SFX.PLAYER_SHOOT_HIT_D,
        )).play()
