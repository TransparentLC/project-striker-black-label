import typing
import pygame
import random

import lib.sprite
import lib.sprite.player
import lib.sound
import lib.globals
import lib.textures
import lib.utils
import lib.bullet.player_bullet

texturesAIdle = tuple(lib.textures.PLAYER[f'player-a-option-idle-{i}'] for i in range(2))
texturesATurnL0 = tuple(lib.textures.PLAYER[f'player-a-option-turn-l-0-{i}'] for i in range(2))
texturesATurnL1 = tuple(lib.textures.PLAYER[f'player-a-option-turn-l-1-{i}'] for i in range(2))
texturesATurnR0 = tuple(lib.textures.PLAYER[f'player-a-option-turn-r-0-{i}'] for i in range(2))
texturesATurnR1 = tuple(lib.textures.PLAYER[f'player-a-option-turn-r-1-{i}'] for i in range(2))
texturesBIdle = tuple(lib.textures.PLAYER[f'player-b-option-idle-{i}'] for i in range(2))
texturesBTurnL0 = tuple(lib.textures.PLAYER[f'player-b-option-turn-l-0-{i}'] for i in range(2))
texturesBTurnL1 = tuple(lib.textures.PLAYER[f'player-b-option-turn-l-1-{i}'] for i in range(2))
texturesBTurnR0 = tuple(lib.textures.PLAYER[f'player-b-option-turn-r-0-{i}'] for i in range(2))
texturesBTurnR1 = tuple(lib.textures.PLAYER[f'player-b-option-turn-r-1-{i}'] for i in range(2))

class PlayerOption(lib.sprite.Sprite):
    texturesIdle: typing.Sequence[pygame.Surface]
    texturesTurnL0: typing.Sequence[pygame.Surface]
    texturesTurnL1: typing.Sequence[pygame.Surface]
    texturesTurnR0: typing.Sequence[pygame.Surface]
    texturesTurnR1: typing.Sequence[pygame.Surface]

    offsetNormal: pygame.Vector2
    offsetSlow: pygame.Vector2
    angleNormal: float
    angleSlow: float
    shiftCounter: int
    shiftCounterLimit: int

    def __init__(
        self,
        shiftCounterLimit: int,
        offsetNormal: pygame.Vector2,
        offsetSlow: pygame.Vector2,
        angleNormal: float,
        angleSlow: float,
    ) -> None:
        super().__init__(lib.globals.groupPlayerOption)
        self.shiftCounter = 0
        self.speed = pygame.Vector2()
        self.interval = 5
        self.shiftCounterLimit = shiftCounterLimit
        self.offsetNormal = offsetNormal
        self.offsetSlow = offsetSlow
        self.angleNormal = angleNormal
        self.angleSlow = angleSlow
        self.shootWait = 0

    @property
    def textures(self) -> typing.Sequence[pygame.Surface]:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if s.deathWait or s.textures == s.texturesIdle:
            return self.texturesIdle
        elif s.textures == s.texturesTurnL0:
            return self.texturesTurnL0
        elif s.textures == s.texturesTurnL1:
            return self.texturesTurnL1
        elif s.textures == s.texturesTurnR0:
            return self.texturesTurnR0
        elif s.textures == s.texturesTurnR1:
            return self.texturesTurnR1

    @property
    def angle(self) -> float:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        return s.angle + lib.utils.linearInterpolation(
            self.shiftCounter / self.shiftCounterLimit,
            self.angleNormal,
            self.angleSlow
        )

    @property
    def position(self) -> float:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        return s.position + lib.utils.linearInterpolation(
            self.shiftCounter / self.shiftCounterLimit,
            self.offsetNormal,
            self.offsetSlow
        ).rotate(-s.angle)

    @position.setter
    def position(self, value) -> None:
        # Computed property, shouldn't be assigned.
        pass

    @property
    def slow(self) -> bool:
        return lib.globals.keys[pygame.K_LSHIFT]

    def shoot(self) -> None:
        pass

    def shootHyper(self) -> None:
        pass

    def update(self) -> None:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.deathWait:
            if lib.globals.keys[pygame.K_LSHIFT]:
                self.shiftCounter = lib.utils.clamp(self.shiftCounter + 1, 0, self.shiftCounterLimit)
            else:
                self.shiftCounter = lib.utils.clamp(self.shiftCounter - 1, 0, self.shiftCounterLimit)

        if self.shootWait:
            self.shootWait -= 1
        if lib.globals.keys[pygame.K_z] and not self.shootWait and not s.deathWait:
            if lib.globals.groupPlayer.sprite.hyperRemain:
                self.shootHyper()
            else:
                self.shoot()
            random.choice((
                lib.sound.SFX.PLAYER_SHOOT_A,
                lib.sound.SFX.PLAYER_SHOOT_B,
            )).play()

        super().update()

class OptionTypeAH(PlayerOption):
    texturesIdle = texturesAIdle
    texturesTurnL0 = texturesATurnL0
    texturesTurnL1 = texturesATurnL1
    texturesTurnR0 = texturesATurnR0
    texturesTurnR1 = texturesATurnR1

    def shoot(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-b-bullet-d'],
            size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle,
            damage=117,
            flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING,
        )
        self.shootWait = 12

    def shootHyper(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-b-bullet-d'],
            size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle,
            damage=117,
            flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING,
        )
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-hyper-bullet-a'],
            size=lib.bullet.player_bullet.bulletSize1Way * 2, speed=12, angle=self.angle,
            damage=48,
            flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING,
        )
        self.shootWait = 10

class OptionTypeAW(PlayerOption):
    texturesIdle = texturesAIdle
    texturesTurnL0 = texturesATurnL0
    texturesTurnL1 = texturesATurnL1
    texturesTurnR0 = texturesATurnR0
    texturesTurnR1 = texturesATurnR1

    def __init__(
        self,
        shiftCounterLimit: int,
        offsetNormal: pygame.Vector2,
        offsetSlow: pygame.Vector2,
        angleNormal: float,
        angleSlow: float,
        hyperClockwise: bool
    ) -> None:
        super().__init__(shiftCounterLimit, offsetNormal, offsetSlow, angleNormal, angleSlow)
        self.hyperClockwise = hyperClockwise

    def shoot(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-a-bullet-b'],
            size=lib.bullet.player_bullet.bulletSize2Way * 3 // 2, speed=12, angle=self.angle,
            damage=49,
        )
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-a-bullet-a'],
            size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=11, angle=self.angle - 9,
            damage=31,
        )
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-a-bullet-a'],
            size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=11, angle=self.angle + 9,
            damage=31,
        )
        self.shootWait = 6

    def shootHyper(self) -> None:
        for i in range(0, 360, 90):
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-hyper-bullet-a'],
                size=lib.bullet.player_bullet.bulletSize1Way * 2, speed=7,
                angle=self.angle + i + (-1 if self.hyperClockwise else 1) * self.frameCounter,
                damage=77,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING,
            )
        self.shootWait = 10

# B-Deflect机体：
class OptionTypeBD(PlayerOption):
    texturesIdle = texturesBIdle
    texturesTurnL0 = texturesBTurnL0
    texturesTurnL1 = texturesBTurnL1
    texturesTurnR0 = texturesBTurnR0
    texturesTurnR1 = texturesBTurnR1

    def shoot(self) -> None:
        for i in (-7, 0, 7):
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.textures.PLAYER['player-b-bullet-a'],
                size=lib.bullet.player_bullet.bulletSize1Way, speed=11, angle=self.angle + i - lib.globals.groupPlayer.sprite.turnCounter * 2,
                damage=31,
            )
        self.shootWait = 8

    def shootHyper(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-hyper-bullet-b'],
            size=lib.bullet.player_bullet.bulletSize2Way * 2, speed=11, angle=self.angle - lib.globals.groupPlayer.sprite.turnCounter * 2.5,
            damage=114,
            flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING,
        )
        self.shootWait = 6

# B-Straight机体：
class OptionTypeBS(PlayerOption):
    texturesIdle = texturesBIdle
    texturesTurnL0 = texturesBTurnL0
    texturesTurnL1 = texturesBTurnL1
    texturesTurnR0 = texturesBTurnR0
    texturesTurnR1 = texturesBTurnR1

    def shoot(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-b-bullet-c'],
            size=lib.bullet.player_bullet.bulletSize4Way * 2 // 3, speed=12, angle=self.angle, damage=123,
        )
        self.shootWait = 5

    def shootHyper(self) -> None:
        lib.bullet.player_bullet.PlayerBullet(
            self.position,
            lib.textures.PLAYER['player-hyper-bullet-c'],
            size=lib.bullet.player_bullet.bulletSize4Way * 4 // 3, speed=12, angle=self.angle, damage=166,
            flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING,
        )
        self.shootWait = 4
