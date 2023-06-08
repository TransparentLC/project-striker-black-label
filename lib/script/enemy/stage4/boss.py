import math
import pygame

import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite
import lib.sprite.enemy
import lib.sprite.explosion as explosion
import lib.sprite.debris as debris
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_D_NORMAL
    ctx.interval = 1
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-15, -17), 11),
        lib.sprite.Hitbox(pygame.Vector2(-25, -36), 5),
        lib.sprite.Hitbox(pygame.Vector2(-25, -29), 5),
        lib.sprite.Hitbox(pygame.Vector2(-29, -18), 10),
        lib.sprite.Hitbox(pygame.Vector2(-40, -18), 9),
        lib.sprite.Hitbox(pygame.Vector2(-52, -18), 8),
        lib.sprite.Hitbox(pygame.Vector2(-63, -18), 7),
        lib.sprite.Hitbox(pygame.Vector2(-73, -18), 6),
        lib.sprite.Hitbox(pygame.Vector2(-35, 38), 5),
        lib.sprite.Hitbox(pygame.Vector2(-27, 38), 6),
        lib.sprite.Hitbox(pygame.Vector2(-19, 37), 7),
        lib.sprite.Hitbox(pygame.Vector2(-10, 37), 8),
        lib.sprite.Hitbox(pygame.Vector2(15, -17), 11),
        lib.sprite.Hitbox(pygame.Vector2(25, -36), 5),
        lib.sprite.Hitbox(pygame.Vector2(25, -29), 5),
        lib.sprite.Hitbox(pygame.Vector2(29, -18), 10),
        lib.sprite.Hitbox(pygame.Vector2(40, -18), 9),
        lib.sprite.Hitbox(pygame.Vector2(52, -18), 8),
        lib.sprite.Hitbox(pygame.Vector2(63, -18), 7),
        lib.sprite.Hitbox(pygame.Vector2(73, -18), 6),
        lib.sprite.Hitbox(pygame.Vector2(35, 38), 5),
        lib.sprite.Hitbox(pygame.Vector2(27, 38), 6),
        lib.sprite.Hitbox(pygame.Vector2(19, 37), 7),
        lib.sprite.Hitbox(pygame.Vector2(10, 37), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, -46), 5),
        lib.sprite.Hitbox(pygame.Vector2(0, -40), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, -29), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, -14), 12),
        lib.sprite.Hitbox(pygame.Vector2(0, 0), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, 10), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, 20), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, 30), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, 42), 6),
    )
    ctx.debris = (
        (debris.DebrisB, pygame.Vector2(-17, 17), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(17, 17), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-31, -18), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(31, -18), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-46, -18), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(46, -18), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-58, -19), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(58, -19), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-73, -18), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(73, -18), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-13, 37), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(13, 37), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-26, 37), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(26, 37), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(0, 37), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(0, 19), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, 4), .125, 2, 1, 5, 4),
        (debris.DebrisA, pygame.Vector2(0, -9), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(0, -26), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -41), .125, 2, 1, 5, 2),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 96, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(5)
    common.setBossHPRange(ctx, 10000, 87573)
    common.setPhaseName(0)
    common.setCountdown(35 * 60 + 120, 35 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    k = 1
    while True:
        for i in range(20):
            SFX.ENEMY_SHOOT_B.play()
            v = pygame.Vector2(0, (i + 1) * 10).rotate(i * -20 * k)
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | (BF.COLOR_LIGHT_CYAN if k == 1 else BF.COLOR_LIME),
                x=v.x, y=-25 + v.y,
                speed=1.75,
                angle=0,
                ways=(9, 13, 17)[lib.globals.difficultyType],
            )
            yield 5
        k = -k
        common.moveRandom(ctx, 192, 96, 192, 64, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 116562)
    common.setPhaseName(11)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint) / (55 * 60) * .9),
    )
    ctx.hitpoint = 116562
    common.setCountdown(55 * 60, 55 * 60)
    k = bool(common.randomInt(0, 1))
    while True:
        common.moveRandom(ctx, 192 + (80 if k else -80), 128, 128, 64, 120, lib.utils.easeInOutCubicInterpolation)
        yield 120
        for i in range(0, 448, (12, 8, 4)[lib.globals.difficultyType]):
            SFX.ENEMY_SHOOT_A.play()
            common.shoot(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE,
                x=0,
                y=-ctx.position.y + i,
                speed=0,
                angle=common.randomInt(0, 360),
                update=common.bulletChangeSpeed((
                    (120, .5),
                    (150, .5),
                )),
            )
            if i % (24, 16, 8)[lib.globals.difficultyType] == 0:
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GRAY,
                    x=25 * math.sin(math.pi / 112 * i),
                    y=-ctx.position.y + i,
                    speed=0,
                    angle=180 + 360 / 224 * i,
                    update=common.bulletChangeSpeed((
                        (120, .5),
                        (150, .5),
                    )),
                )
            yield (4, 3, 2)[lib.globals.difficultyType]
        k = not k

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 28)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 98671)
    common.setPhaseName(0)
    ctx.invincibleRemain = 60
    common.setCountdown(40 * 60 + 60, 40 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120

    m = (2, 1.5, 1.5)[lib.globals.difficultyType]
    while True:
        k = common.randomInt(0, 360)
        for _ in range(8):
            for i in range(16):
                if i % 8 < 5:
                    if i % 2 == 0:
                        SFX.ENEMY_SHOOT_D.play()
                    common.shootMultiWay(
                        ctx,
                        bullet=BF.TYPE_SHELL_SMALL | (BF.COLOR_LIGHT_CYAN if m > 0 else BF.COLOR_LIME),
                        x=0, y=-25,
                        speed=3.5 + (i % 8) * .25,
                        angle=k,
                        ways=(6, 10, 14)[lib.globals.difficultyType],
                    )
                    k += m
                    yield 3
        m = -m
        common.moveRandom(ctx, 192, 96, 96, 64, 150, lib.utils.easeOutCubicInterpolation)

def phase1b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 55 or ctx.frameCounter == 60:
        ctx.speedRadius -= 1
    elif ctx.frameCounter == 65:
        ctx.speedRadius -= .5
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN],)
        ctx.hitbox = (lib.sprite.Hitbox(pygame.Vector2(0, 0), common.BulletSizes[BF.TYPE_SHELL_SMALL]),)
        ctx.rotate()
        ctx.updateCustom = None

def phase1b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 55 or ctx.frameCounter == 60:
        ctx.speedRadius -= 1
    elif ctx.frameCounter == 65:
        ctx.speedRadius -= .5
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GRAY],)
        ctx.hitbox = (lib.sprite.Hitbox(pygame.Vector2(0, 0), common.BulletSizes[BF.TYPE_SHELL_SMALL]),)
        ctx.rotate()
        ctx.updateCustom = None

def phase1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 131698)
    common.setPhaseName(12)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 96, 120, lib.utils.easeInOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60

    k = True
    while True:
        SFX.ENEMY_SHOOT_C.play()
        if k:
            for x in (-39, 39):
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_CYAN,
                    x=x, y=-7,
                    speed=4,
                    angle=0,
                    ways=(21, 35, 49)[lib.globals.difficultyType],
                    update=phase1b0,
                )
        else:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_GRAY,
                x=0, y=-41,
                speed=4,
                angle=common.randomInt(0, 360),
                ways=(21, 35, 49)[lib.globals.difficultyType],
                update=phase1b1,
            )
        k = not k
        yield 15

def general2(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_D_BREAK
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 33)
    common.moveClear(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 102984)
    common.setPhaseName(0)
    ctx.invincibleRemain = 60
    common.setCountdown(45 * 60 + 60, 45 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120

    m = (3, 2, 2)[lib.globals.difficultyType]
    while True:
        k = common.randomInt(0, 360)
        for _ in range(2):
            for i in range(16):
                if i % 8 < 5:
                    if i % 2 == 0:
                        SFX.ENEMY_SHOOT_D.play()
                    common.shootMultiWay(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | (BF.COLOR_LIGHT_CYAN if m > 0 else BF.COLOR_LIME),
                        x=0, y=-25,
                        speed=1.5 + (i % 8) * .075,
                        angle=k,
                        ways=(6, 10, 14)[lib.globals.difficultyType],
                    )
                    k += m
                    yield 5
        m = -m
        common.moveRandom(ctx, 192, 96, 96, 64, 150, lib.utils.easeOutCubicInterpolation)

def phase2(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 0, 146876)
    common.setPhaseName(13)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint) / (70 * 60 + 120) * .9),
    )
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(70 * 60 + 120, 70 * 60)
    common.move(ctx, 192, 96, 120, lib.utils.easeInOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60
    k = (12, 18, 24)[lib.globals.difficultyType]
    while True:
        for _ in range(8):
            for i in range(4):
                if i % 2 == 0:
                    SFX.ENEMY_SHOOT_D.play()
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN,
                    x=0, y=-27,
                    speed=2,
                    angle=0,
                    ways=k + 1,
                    fanSize=k * (20, 15, 10)[lib.globals.difficultyType],
                )
                for _ in range((1, 1, 2)[lib.globals.difficultyType]):
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED,
                        x=common.randomInt(-192, 192), y=-108,
                        speed=common.randomFloat(.5, 1.75),
                        angle=180,
                    )
                yield 10
            if k < (19, 25, 37)[lib.globals.difficultyType]:
                k += 1
            else:
                k = (18, 24, 36)[lib.globals.difficultyType]
        common.moveRandom(ctx, 192, 96, 144, 48, 90, lib.utils.easeOutCubicInterpolation)

def death(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 38)

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
    general2,
    phase2,
)