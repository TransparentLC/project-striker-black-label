import dataclasses
import functools
import pygame
import typing

import lib.bullet.enemy_bullet
import lib.constants
import lib.globals
import lib.sound
import lib.sprite
import lib.sprite.enemy
import lib.sprite.debris
import lib.sprite.explosion
import lib.sprite.item
import lib.stg_overlay
import lib.textures
import lib.utils

@dataclasses.dataclass
class EnemyTextures:
    ENEMY_A = tuple(lib.textures.ENEMY[f'enemy-a-{i}'] for i in range(2))
    ENEMY_B = tuple(lib.textures.ENEMY[f'enemy-b-{i}'] for i in range(2))
    ENEMY_C = tuple(lib.textures.ENEMY[f'enemy-c-{i}'] for i in range(2))
    ENEMY_D = tuple(lib.textures.ENEMY[f'enemy-d-{i}'] for i in range(2))
    ENEMY_E = tuple(lib.textures.ENEMY[f'enemy-e-{i}'] for i in range(2))
    ENEMY_F = tuple(lib.textures.ENEMY[f'enemy-f-{i}'] for i in range(2))
    BOSS_A_NORMAL = tuple(lib.textures.ENEMY[f'boss-a-normal-{i}'] for i in range(8))
    BOSS_A_BREAK = tuple(lib.textures.ENEMY[f'boss-a-break-{i}'] for i in range(8))
    BOSS_B_NORMAL = tuple(lib.textures.ENEMY[f'boss-b-normal-{i}'] for i in range(8))
    BOSS_B_BREAK = tuple(lib.textures.ENEMY[f'boss-b-break-{i}'] for i in range(8))
    BOSS_C_NORMAL = tuple(lib.textures.ENEMY[f'boss-c-normal-{i}'] for i in range(8))
    BOSS_C_BREAK = tuple(lib.textures.ENEMY[f'boss-c-break-{i}'] for i in range(8))
    BOSS_D_NORMAL = tuple(lib.textures.ENEMY[f'boss-d-normal-{i}'] for i in range(8))
    BOSS_D_BREAK = tuple(lib.textures.ENEMY[f'boss-d-break-{i}'] for i in range(8))
    BOSS_E_NORMAL = tuple(lib.textures.ENEMY[f'boss-e-normal-{i}'] for i in range(8))
    BOSS_E_BREAK = tuple(lib.textures.ENEMY[f'boss-e-break-{i}'] for i in range(8))

@dataclasses.dataclass
class BulletFlags:
    TYPE_ROUND_TINY = 0x10
    TYPE_ROUND_SMALL = 0x10
    TYPE_ROUND_MEDIUM = 0x20
    TYPE_ROUND_LARGE = 0x30
    TYPE_SHELL_SMALL = 0x40
    TYPE_SHELL_LARGE = 0x50
    TYPE_SHELL_DUAL = 0x60
    COLOR_GRAY = 0x00
    COLOR_RED = 0x01
    COLOR_MAGENTA = 0x02
    COLOR_BLUE = 0x03
    COLOR_CYAN = 0x04
    COLOR_GREEN = 0x05
    COLOR_LIME = 0x06
    COLOR_ORANGE = 0x07
    COLOR_LIGHT_GRAY = 0x08
    COLOR_LIGHT_RED = 0x09
    COLOR_LIGHT_MAGENTA = 0x0A
    COLOR_LIGHT_BLUE = 0x0B
    COLOR_LIGHT_CYAN = 0x0C
    COLOR_LIGHT_GREEN = 0x0D
    COLOR_LIGHT_LIME = 0x0E
    COLOR_LIGHT_ORANGE = 0x0F

BulletTexturesMerged = pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet.webp')).convert_alpha()
BulletTextures = (
    # ROUND_TINY
    *(BulletTexturesMerged.subsurface((0 + (i & 7) * 7, 0 + (i >> 3) * 7, 7, 7)) for i in range(16)),
    # ROUND_SMALL
    *(BulletTexturesMerged.subsurface((0 + (i & 7) * 9, 14 + (i >> 3) * 9, 9, 9)) for i in range(16)),
    # ROUND_MEDIUM
    *(BulletTexturesMerged.subsurface((0 + (i & 7) * 14, 32 + (i >> 3) * 14, 14, 14)) for i in range(16)),
    # ROUND_LARGE
    *(BulletTexturesMerged.subsurface((0 + (i & 7) * 18, 60 + (i >> 3) * 18, 18, 18)) for i in range(16)),
    # SHELL_SMALL
    *(BulletTexturesMerged.subsurface((88 + (i & 7) * 6, 96 + (i >> 3) * 13, 6, 13)) for i in range(16)),
    # SHELL_LARGE
    *(BulletTexturesMerged.subsurface((72 + (i & 7) * 8, 0 + (i >> 3) * 15, 8, 15)) for i in range(16)),
    # SHELL_DUAL
    *(BulletTexturesMerged.subsurface((0 + (i & 7) * 11, 96 + (i >> 3) * 18, 11, 18)) for i in range(16)),
)

BulletSizes = (
    *(2 for i in range(16)),
    *(3 for i in range(16)),
    *(5 for i in range(16)),
    *(7 for i in range(16)),
    *(2 for i in range(16)),
    *(3 for i in range(16)),
    *(4 for i in range(16)),
)

def randomInt(minValue: int, maxValue: int):
    return lib.globals.stgRandom.randint(minValue, maxValue)

def randomFloat(minValue: float, maxValue: float):
    return minValue + (maxValue - minValue) * lib.globals.stgRandom.random()

def calcOffset(context: 'lib.sprite.enemy.Enemy', x: float, y: float):
    return context.position + pygame.Vector2(x, y).rotate(-context.angle)

def calcDirection(a: pygame.Vector2, b: pygame.Vector2):
    return -(b - a).as_polar()[1] - 90

def calcDirectionAiming(context: 'lib.sprite.enemy.Enemy', x: float, y: float):
    return calcDirection(context.position + pygame.Vector2(x, y), lib.globals.groupPlayer.sprite.position)

def setPosition(context: 'lib.sprite.enemy.Enemy', x: float, y: float):
    context.position.update(x, y)

def setPositionRelative(context: 'lib.sprite.enemy.Enemy', x: float, y: float):
    context.position += pygame.Vector2(x, y)

def setSpeed(context: 'lib.sprite.enemy.Enemy', speed: float):
    context.speed.update(pygame.Vector2(0, -speed).rotate(-context.angle))

def setBoss(context: 'lib.sprite.enemy.Enemy'):
    lib.globals.groupBoss.sprite = context

def setBossRemain(remain: int):
    lib.globals.bossRemain = remain

def setBossHPRange(context: 'lib.sprite.enemy.Enemy', hpMin: int, hpMax: int):
    context.hitpointBreak = hpMin
    lib.globals.bossHitpointRangeMin = hpMin
    lib.globals.bossHitpointRangeMax = hpMax

def setPhaseName(index: int):
    lib.globals.phaseIndex = index
    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_NAME_REMAIN] = 120 if index else 0
    if index:
        lib.sound.SFX.PHASE_START.play()

def setPhaseBonus(bonus: int, drop: int):
    lib.globals.phaseBonus = bonus
    lib.globals.phaseBonusDrop = drop

def setCountdown(countdown: int|None = None, countdownMax: int = 0):
    lib.globals.timeCountdown = countdown
    lib.globals.timeCountdownMax = countdownMax

def move(
    context: 'lib.sprite.enemy.Enemy',
    x: float, y: float,
    time: int,
    interpolation: typing.Callable[[float, pygame.Vector2, pygame.Vector2], pygame.Vector2],
):
    context.speed.update(0, 0)
    context.movementQueue.append((
        pygame.Vector2(x, y),
        time,
        interpolation,
    ))

def moveRelative(
    context: 'lib.sprite.enemy.Enemy',
    x: float, y: float,
    time: int,
    interpolation: typing.Callable[[float, pygame.Vector2, pygame.Vector2], pygame.Vector2],
):
    context.speed.update(0, 0)
    context.movementQueue.append((
        context.position + pygame.Vector2(x, y),
        time,
        interpolation,
    ))

def moveRandom(
    context: 'lib.sprite.enemy.Enemy',
    x: float, y: float,
    width: float, height: float,
    time: int,
    interpolation: typing.Callable[[float, pygame.Vector2, pygame.Vector2], pygame.Vector2],
):
    context.speed.update(0, 0)
    context.movementQueue.append((
        pygame.Vector2(
            x + (lib.globals.stgRandom.random() - .5) * width,
            y + (lib.globals.stgRandom.random() - .5) * height,
        ),
        time,
        interpolation,
    ))

def moveClear(context: 'lib.sprite.enemy.Enemy'):
    context.movementQueue.clear()
    context.movementTask = None

def shoot(
    context: 'lib.sprite.enemy.Enemy',
    bullet: int,
    x: float, y: float,
    speed: float, angle: float,
    update: typing.Callable[[lib.bullet.enemy_bullet.EnemyBullet], None] = None,
) -> lib.bullet.enemy_bullet.EnemyBullet:
    return lib.bullet.enemy_bullet.EnemyBullet(
        context.position + pygame.Vector2(x, y).rotate(-context.angle),
        speed,
        angle,
        BulletSizes[bullet],
        BulletTextures[bullet],
        update,
    )

def shootAiming(
    context: 'lib.sprite.enemy.Enemy',
    bullet: int,
    x: float, y: float,
    speed: float, angle: float,
    update: typing.Callable[[lib.bullet.enemy_bullet.EnemyBullet], None] = None,
) -> lib.bullet.enemy_bullet.EnemyBullet:
    shootPosition = context.position + pygame.Vector2(x, y).rotate(-context.angle)
    return lib.bullet.enemy_bullet.EnemyBullet(
        shootPosition,
        speed,
        -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + angle,
        BulletSizes[bullet],
        BulletTextures[bullet],
        update,
    )

def shootMultiWay(
    context: 'lib.sprite.enemy.Enemy',
    bullet: int,
    x: float, y: float,
    speed: float, angle: float,
    ways: int, fanSize: float = 0,
    update: typing.Callable[[lib.bullet.enemy_bullet.EnemyBullet], None] = None,
) -> typing.Sequence[lib.bullet.enemy_bullet.EnemyBullet]:
    r = []
    if not fanSize:
        fanSize = (ways - 1) / ways * 360
    for i in range(ways):
        fanAngle = 0 if ways == 1 else (i - (ways - 1) / 2) / (ways - 1) * fanSize
        r.append(lib.bullet.enemy_bullet.EnemyBullet(
            context.position + pygame.Vector2(x, y).rotate(-context.angle),
            speed,
            fanAngle + angle,
            BulletSizes[bullet],
            BulletTextures[bullet],
            update,
        ))
    return r

def shootAimingMultiWay(
    context: 'lib.sprite.enemy.Enemy',
    bullet: int,
    x: float, y: float,
    speed: float, angle: float,
    ways: int, fanSize: float = 0,
    update: typing.Callable[[lib.bullet.enemy_bullet.EnemyBullet], None] = None,
) -> typing.Sequence[lib.bullet.enemy_bullet.EnemyBullet]:
    r = []
    shootPosition = context.position + pygame.Vector2(x, y).rotate(-context.angle)
    if not fanSize:
        fanSize = (ways - 1) / ways * 360
    for i in range(ways):
        fanAngle = 0 if ways == 1 else (i - (ways - 1) / 2) / (ways - 1) * fanSize
        r.append(lib.bullet.enemy_bullet.EnemyBullet(
            shootPosition,
            speed,
            -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + fanAngle + angle,
            BulletSizes[bullet],
            BulletTextures[bullet],
            update,
        ))
    return r

def shootComplex(
    context: 'lib.sprite.enemy.Enemy',
    bullet: int,
    x: float, y: float,
    speed: float, angle: float,
    ways: int, fanSize: float = 0,
    speedAddition: float = 0, layers: int = 1,
    deflection: float = 0, radius: float = 0,
    aiming: bool = False,
    freeze: bool = False,
    avoidRange: float = 0,
    update: typing.Callable[[lib.bullet.enemy_bullet.EnemyBullet], None] = None,
) -> typing.Sequence[lib.bullet.enemy_bullet.EnemyBullet]:
    r = []
    shootPosition = context.position + pygame.Vector2(x, y).rotate(-context.angle)
    shootAngle = angle
    if not fanSize:
        fanSize = (ways - 1) / ways * 360
    if aiming:
        shootAngle += -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90
    for i in range(ways):
        fanAngle = 0 if ways == 1 else (i - (ways - 1) / 2) / (ways - 1) * fanSize
        sp = shootPosition + pygame.Vector2(0, -radius).rotate(-shootAngle-fanAngle)
        if sp.distance_to(lib.globals.groupPlayer.sprite.position) < avoidRange:
            continue
        for j in range(layers):
            r.append(lib.bullet.enemy_bullet.EnemyBullet(
                sp,
                speed + j * speedAddition,
                shootAngle + fanAngle + deflection,
                BulletSizes[bullet],
                BulletTextures[bullet],
                update,
            ))
    for b in r:
        b.freeze = freeze
    return r

def clearBullet(context: 'lib.sprite.enemy.Enemy'):
    lib.globals.clearBulletCenter = pygame.Vector2(context.position)
    lib.globals.clearBulletRadius = 0
    lib.globals.clearBulletBonus = False

def bonusBullet(context: 'lib.sprite.enemy.Enemy'):
    lib.globals.clearBulletCenter = pygame.Vector2(context.position)
    lib.globals.clearBulletRadius = 0
    lib.globals.clearBulletBonus = True
    lib.sound.SFX.BONUS.play()

def bonusPhase():
    if not lib.globals.phaseIndex:
        return
    sf = f'{lib.globals.phaseIndex - 1}-{lib.globals.optionType}-{lib.globals.difficultyType}'
    if lib.globals.replayRecording:
        lib.globals.savedata["phase-encounter-" + sf] += 1
    lib.globals.score += lib.globals.phaseBonus
    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_BONUS_REMAIN] = 240
    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_BONUS_VALUE] = lib.globals.phaseBonus
    if lib.globals.replayRecording and lib.globals.phaseBonus:
        lib.globals.phaseBonusCount += 1
        lib.globals.savedata["phase-reward-" + sf] += 1
    lib.globals.phaseIndex = 0
    lib.globals.phaseBonus = 0

def dropPointItem(context: 'lib.sprite.enemy.Enemy', amount: int):
    minwh = min(context.rect.width, context.rect.height)
    for i in range(amount):
        pos = pygame.Vector2(lib.globals.stgRandom.random() * minwh, 0)
        pos.rotate_ip(lib.globals.stgRandom.random() * 360)
        pos += context.position
        lib.sprite.item.Point(pos)

def charge(position: pygame.Vector2, count: int = 96) -> int:
    lib.sound.SFX.CHARGE.play()
    for _ in range(count):
        lib.sprite.explosion.Charge(position)
    return 120

def freezeBullet():
    for b in lib.globals.groupEnemyBullet:
        b.freeze = True

def unfreezeBullet():
    for b in lib.globals.groupEnemyBullet:
        b.freeze = False

def extendLife(context: 'lib.sprite.enemy.Enemy'):
    lib.sprite.item.LifeExtend(context.position)

def extendHyper(context: 'lib.sprite.enemy.Enemy'):
    lib.sprite.item.HyperExtend(context.position)

def presetEnemyA(context: 'lib.sprite.enemy.Enemy'):
    context.textures = EnemyTextures.ENEMY_A
    context.explosion = lib.sprite.explosion.ExplosionPlaneLarge
    context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_C
    context.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(0, 12), 10),
        lib.sprite.Hitbox(pygame.Vector2(0, -10), 12),
        lib.sprite.Hitbox(pygame.Vector2(-19, -6), 8),
        lib.sprite.Hitbox(pygame.Vector2(19, -6), 8),
    )
    context.debris = (
        (lib.sprite.debris.DebrisA, pygame.Vector2(-20, -6), .125, 2, 1, 5),
        (lib.sprite.debris.DebrisA, pygame.Vector2(20, -6), .125, 2, 1, 5),
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, 12), .125, 2, 1, 5),
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, 12), .125, 2, 1, 5),
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, -10), .125, 2, 1, 5),
    )

def presetEnemyB(context: 'lib.sprite.enemy.Enemy'):
    context.textures = EnemyTextures.ENEMY_B
    context.explosion = lib.sprite.explosion.ExplosionPlaneMediumA
    context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
    context.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
        lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
        lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
    )
    context.debris = (
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, 5), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(6, -2), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
    )

def presetEnemyC(context: 'lib.sprite.enemy.Enemy'):
    context.textures = EnemyTextures.ENEMY_C
    context.explosion = lib.sprite.explosion.ExplosionPlaneMediumB
    context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
    context.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
        lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
        lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
    )
    context.debris = (
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, 5), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(6, -2), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
    )

def presetEnemyD(context: 'lib.sprite.enemy.Enemy'):
    context.textures = EnemyTextures.ENEMY_D
    context.explosion = lib.sprite.explosion.ExplosionPlaneMediumB
    context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
    context.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
        lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
        lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
    )
    context.debris = (
        (lib.sprite.debris.DebrisB, pygame.Vector2(0, 5), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(6, -2), .125, 1.75, 1, 3),
        (lib.sprite.debris.DebrisA, pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
    )

def presetEnemyE(context: 'lib.sprite.enemy.Enemy'):
    context.textures = EnemyTextures.ENEMY_E
    context.explosion = lib.sprite.explosion.ExplosionPlaneSmallA
    context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_A
    context.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(4, 0), 6),
        lib.sprite.Hitbox(pygame.Vector2(-4, 0), 6),
    )
    context.debris = (
        (lib.sprite.debris.DebrisA, pygame.Vector2(4, 0), .125, 1.75, .5, 2),
        (lib.sprite.debris.DebrisB, pygame.Vector2(-4, 0), .125, 1.75, .5, 2),
    )

@functools.cache
def bulletChangeSpeed(speedTable: tuple[tuple[int, float], ...]) -> typing.Callable[['lib.bullet.enemy_bullet.EnemyBullet'], None]:
    def update(context: 'lib.bullet.enemy_bullet.EnemyBullet'):
        for frame, speed in speedTable:
            if context.frameCounter == frame:
                context.speedRadius += speed
                return
        if context.frameCounter > speedTable[-1][0]:
            context.updateCustom = None
    return update

@functools.cache
def bulletChangeType(speedTable: tuple[tuple[int, int], ...]) -> typing.Callable[['lib.bullet.enemy_bullet.EnemyBullet'], None]:
    def update(context: 'lib.bullet.enemy_bullet.EnemyBullet'):
        for frame, bulletType in speedTable:
            if context.frameCounter == frame:
                context.textures = (BulletTextures[bulletType],)
                context.size = BulletSizes[bulletType]
                context.rotate()
                return
        if context.frameCounter > speedTable[-1][0]:
            context.updateCustom = None
    return update