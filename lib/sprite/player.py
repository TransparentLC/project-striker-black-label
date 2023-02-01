import typing
import pygame
import random

from . import Sprite
from . import Hitbox
from . import explosion

import lib.constants
import lib.globals
import lib.sound
import lib.utils
import lib.textures
import lib.bullet.player_bullet

playerBoundary = pygame.Rect(13, 8, 384 - 2 * 13, 448 - 2 * 8)
playerInitialPosition = pygame.Vector2(192, 400)

class Player(Sprite):
    def __init__(
        self,
        texturesIdle: typing.Sequence[pygame.Surface],
        texturesTurnL0: typing.Sequence[pygame.Surface],
        texturesTurnL1: typing.Sequence[pygame.Surface],
        texturesTurnR0: typing.Sequence[pygame.Surface],
        texturesTurnR1: typing.Sequence[pygame.Surface],
        explosionClass: explosion.Explosion,
        speedNormal: float,
        speedSlow: float,
        hitbox: Hitbox,
    ) -> None:
        super().__init__(lib.globals.groupPlayer)
        self.speed = pygame.Vector2(0, 0)
        self.boundary = playerBoundary
        self.position = pygame.Vector2(playerInitialPosition)
        self.hitbox = (hitbox,)
        self.texturesIdle = texturesIdle
        self.texturesTurnL0 = texturesTurnL0
        self.texturesTurnL1 = texturesTurnL1
        self.texturesTurnR0 = texturesTurnR0
        self.texturesTurnR1 = texturesTurnR1
        self.explosionClass = explosionClass
        self.speedNormal = speedNormal
        self.speedSlow = speedSlow
        self.options = tuple()
        self.interval = 5
        self.turnCounter = 0
        self.invincibleRemain = 0
        self.hyperRemain = 0
        self.shootWait = 0
        self.deathWait = 0

    @property
    def textures(self) -> tuple[pygame.Surface]:
        if self.turnCounter == 0:
            return self.texturesIdle
        elif self.turnCounter < -10:
            return self.texturesTurnL1
        elif self.turnCounter < 0:
            return self.texturesTurnL0
        elif self.turnCounter > 10:
            return self.texturesTurnR1
        elif self.turnCounter > 0:
            return self.texturesTurnR0

    def shoot(self) -> None:
        pass

    def update(self) -> None:
        self.speed.update(0, 0)

        if self.deathWait:
            self.deathWait -= 1
            if not self.deathWait:
                if lib.globals.lifeNum:
                    lib.globals.lifeNum -= 1
                    lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
                    self.invincibleRemain = 150
                    self.position.update(playerInitialPosition)
                    lib.globals.clearBulletCenter = pygame.Vector2(playerInitialPosition)
                    lib.globals.clearBulletRadius = 0
                    lib.globals.clearBulletBonus = False
                else:
                    if lib.globals.replayRecording and lib.globals.continueEnabled:
                        lib.sound.SFX.COUNTDOWN.play()
                    lib.globals.continueRemain = 659
                    self.deathWait = 1

        if self.invincibleRemain:
            self.invincibleRemain -= 1

        if self.hyperRemain:
            self.hyperRemain -= 1
            lib.globals.phaseBonus = 0
            if not self.hyperRemain:
                lib.sound.SFX.HYPER_END.play()
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            if self.hyperRemain:
                self.hyperRemain = 0
                self.invincibleRemain = 0
                lib.sound.SFX.HYPER_END.play()
            elif lib.globals.hyperNum and not self.deathWait:
                lib.globals.hyperNum -= 1
                lib.globals.hyperUsedCount += 1
                self.hyperRemain = lib.constants.HYPER_TIME
                self.invincibleRemain = lib.constants.HYPER_INVINCIBLE_TIME
                for item in lib.globals.groupItem:
                    item.magnetNear = True
                lib.sound.SFX.HYPER_ACTIVATE.play()

        if not self.deathWait:
            speed = self.speedSlow if lib.globals.keys[pygame.K_LSHIFT] else self.speedNormal
            if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keys[pygame.K_RIGHT]:
                self.speed -= pygame.Vector2(speed, 0)
                self.turnCounter = max(-10 if lib.globals.keys[pygame.K_LSHIFT] else -20, min(self.turnCounter, 0) - 1)
            elif lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keys[pygame.K_LEFT]:
                self.speed += pygame.Vector2(speed, 0)
                self.turnCounter = min(10 if lib.globals.keys[pygame.K_LSHIFT] else 20, max(self.turnCounter, 0) + 1)
            else:
                if self.turnCounter > 0:
                    self.turnCounter -= 1
                elif self.turnCounter < 0:
                    self.turnCounter += 1
            if lib.globals.keys[pygame.K_UP] and not lib.globals.keys[pygame.K_DOWN]:
                self.speed -= pygame.Vector2(0, speed)
            elif lib.globals.keys[pygame.K_DOWN] and not lib.globals.keys[pygame.K_UP]:
                self.speed += pygame.Vector2(0, speed)
            if self.speed.x and self.speed.y:
                self.speed /= 2 ** .5

            if self.shootWait:
                self.shootWait -= 1
            if lib.globals.keys[pygame.K_z] and not self.shootWait:
                self.shoot()

        super().update()

        if self.invincibleRemain & 4:
            self.image.set_alpha(128)

        if self.deathWait:
            self.image.set_alpha(0)

        self.rect.centerx = self.position.x = lib.utils.clamp(self.position.x, self.boundary.left, self.boundary.right)
        self.rect.centery = self.position.y = lib.utils.clamp(self.position.y, self.boundary.top, self.boundary.bottom)

    def explode(self):
        if self.deathWait:
            return
        lib.sound.SFX.EXPLODE_PLAYER.play()
        self.explosionClass(self.position)
        self.deathWait = 120
        self.hyperRemain = 0
        lib.globals.phaseBonus = 0
        lib.globals.missedCount += 1

class PlayerA(Player):
    def __init__(self) -> None:
        super().__init__(
            tuple(lib.textures.PLAYER[f'player-a-idle-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-a-turn-l-0-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-a-turn-l-1-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-a-turn-r-0-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-a-turn-r-1-{i}'] for i in range(2)),
            explosion.ExplosionPlayerA,
            lib.constants.PLAYER_A_SPEED_NORMAL,
            lib.constants.PLAYER_A_SPEED_SLOW,
            Hitbox(pygame.Vector2(0, -3), 2),
        )

    def shoot(self) -> None:
        if self.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-hyper-bullet-c'],
                size=lib.bullet.player_bullet.bulletSize4Way * 2, speed=18, angle=self.angle, damage=259,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 3
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-a-bullet-c'],
                size=lib.bullet.player_bullet.bulletSize4Way, speed=14, angle=self.angle, damage=205,
            )
            self.shootWait = 4
        random.choice((
            lib.sound.SFX.PLAYER_SHOOT_A,
            lib.sound.SFX.PLAYER_SHOOT_B,
        )).play()

class PlayerB(Player):
    def __init__(self) -> None:
        super().__init__(
            tuple(lib.textures.PLAYER[f'player-b-idle-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-b-turn-l-0-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-b-turn-l-1-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-b-turn-r-0-{i}'] for i in range(2)),
            tuple(lib.textures.PLAYER[f'player-b-turn-r-1-{i}'] for i in range(2)),
            explosion.ExplosionPlayerB,
            lib.constants.PLAYER_B_SPEED_NORMAL,
            lib.constants.PLAYER_B_SPEED_SLOW,
            Hitbox(pygame.Vector2(0, -.5), 2),
        )

    def shoot(self) -> None:
        if self.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-hyper-bullet-c'],
                size=lib.bullet.player_bullet.bulletSize4Way * 2, speed=18, angle=self.angle, damage=289,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 3
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-b-bullet-c'],
                size=lib.bullet.player_bullet.bulletSize4Way, speed=14, angle=self.angle, damage=235,
            )
            self.shootWait = 4
        random.choice((
            lib.sound.SFX.PLAYER_SHOOT_A,
            lib.sound.SFX.PLAYER_SHOOT_B,
        )).play()
