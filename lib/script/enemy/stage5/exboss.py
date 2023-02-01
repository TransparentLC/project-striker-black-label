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
    ctx.textures = common.EnemyTextures.ENEMY_F
    ctx.interval = 5
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-29, -5), 2),
        lib.sprite.Hitbox(pygame.Vector2(-25, -5), 2),
        lib.sprite.Hitbox(pygame.Vector2(-21, -5), 3),
        lib.sprite.Hitbox(pygame.Vector2(-17, -5), 3),
        lib.sprite.Hitbox(pygame.Vector2(-12, -5), 4),
        lib.sprite.Hitbox(pygame.Vector2(-7, -5), 5),
        lib.sprite.Hitbox(pygame.Vector2(-3, -4), 4),
        lib.sprite.Hitbox(pygame.Vector2(-9, 15), 2),
        lib.sprite.Hitbox(pygame.Vector2(-6, 15), 2),
        lib.sprite.Hitbox(pygame.Vector2(-3, 14), 2),
        lib.sprite.Hitbox(pygame.Vector2(29, -5), 2),
        lib.sprite.Hitbox(pygame.Vector2(25, -5), 2),
        lib.sprite.Hitbox(pygame.Vector2(21, -5), 3),
        lib.sprite.Hitbox(pygame.Vector2(17, -5), 3),
        lib.sprite.Hitbox(pygame.Vector2(12, -5), 4),
        lib.sprite.Hitbox(pygame.Vector2(7, -5), 5),
        lib.sprite.Hitbox(pygame.Vector2(3, -4), 4),
        lib.sprite.Hitbox(pygame.Vector2(9, 15), 2),
        lib.sprite.Hitbox(pygame.Vector2(6, 15), 2),
        lib.sprite.Hitbox(pygame.Vector2(3, 14), 2),
        lib.sprite.Hitbox(pygame.Vector2(0, 16), 2),
        lib.sprite.Hitbox(pygame.Vector2(0, 13), 3),
        lib.sprite.Hitbox(pygame.Vector2(0, 9), 2),
        lib.sprite.Hitbox(pygame.Vector2(0, 5), 3),
        lib.sprite.Hitbox(pygame.Vector2(0, 1), 2),
        lib.sprite.Hitbox(pygame.Vector2(0, -9), 3),
        lib.sprite.Hitbox(pygame.Vector2(0, -14), 2),
        lib.sprite.Hitbox(pygame.Vector2(0, -18), 3),
    )
    ctx.debris = (
        (debris.DebrisA, pygame.Vector2(-29, -5), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(-25, -5), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(-21, -5), .125, 2, 1, 2),
        (debris.DebrisB, pygame.Vector2(-17, -5), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(-12, -5), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(-7, -5), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(-3, -4), .125, 2, 1, 2),
        (debris.DebrisB, pygame.Vector2(-9, 15), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(-6, 15), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(-3, 14), .125, 2, 1, 2),
        (debris.DebrisB, pygame.Vector2(29, -5), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(25, -5), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(21, -5), .125, 2, 1, 2),
        (debris.DebrisA, pygame.Vector2(17, -5), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(12, -5), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(7, -5), .125, 2, 1, 2),
        (debris.DebrisA, pygame.Vector2(3, -4), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(9, 15), .125, 2, 1, 2),
        (debris.DebrisA, pygame.Vector2(6, 15), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(3, 14), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(0, 16), .125, 2, 1, 2),
        (debris.DebrisB, pygame.Vector2(0, 13), .125, 2, 1, 2),
        (debris.DebrisA, pygame.Vector2(0, 9), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(0, 5), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(0, 1), .125, 2, 1, 2),
        (debris.DebrisB, pygame.Vector2(0, -9), .125, 2, 1, 1),
        (debris.DebrisB, pygame.Vector2(0, -14), .125, 2, 1, 1),
        (debris.DebrisA, pygame.Vector2(0, -18), .125, 2, 1, 2),
    )
    ctx.invincibleRemain = 480
    ctx.position.update(192, 144)
    common.moveRandom(ctx, 192, 36, 64, 24, 60, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(17)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    yield 60
    common.moveRandom(ctx, 192, 96, 64, 64, 180, lib.utils.easeInOutCubicInterpolation)
    common.moveRandom(ctx, 192, 96, 64, 64, 180, lib.utils.easeInOutCubicInterpolation)
    yield 420

# def general(ctx: lib.sprite.enemy.Enemy):
#     # ctx.hitpoint = 9999; return
#     common.setCountdown()
#     common.bonusBullet(ctx)
#     common.bonusPhase()
#     common.dropPointItem(ctx, 30)
#     common.moveClear(ctx)
#     common.setBossRemain(18)
#     common.setBossHPRange(ctx, 10000, 76666)
#     common.setPhaseName(0)
#     ctx.hitpoint = 76666
#     ctx.invincibleRemain = 180
#     ctx.blockHyper = False
#     common.setCountdown(35 * 60 + 180, 35 * 60)
#     common.moveRandom(ctx, 192, 108, 200, 72, 120, lib.utils.easeInOutCubicInterpolation)
#     yield 180

#     while True:
#         yield 60

# def phase(ctx: lib.sprite.enemy.Enemy):
#     # ctx.hitpoint = 9999; return
#     common.setCountdown()
#     common.clearBullet(ctx)
#     common.moveClear(ctx)
#     common.setBossRemain(16)
#     common.setBossHPRange(ctx, 10000, 143333)
#     common.setPhaseName(18)
#     common.setPhaseBonus(
#         (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
#         round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
#     )
#     ctx.hitpoint = 143333
#     ctx.invincibleRemain = 120
#     ctx.blockHyper = True
#     common.setCountdown(60 * 60 + 120, 60 * 60)
#     yield 120

#     while True:
#         yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    # common.bonusBullet(ctx)
    # common.bonusPhase()
    # common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(17)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 60
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 60, 35 * 60)
    yield 60

    while True:
        common.moveRandom(ctx, 192, 108, 200, 72, 240, lib.utils.easeOutCubicInterpolation)
        for _ in range(8):
            SFX.ENEMY_SHOOT_B.play()
            for s in (1.5, 3):
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_CYAN,
                    x=0, y=0,
                    speed=s, angle=0,
                    ways=21,
                )
            yield 15
            SFX.ENEMY_SHOOT_B.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_GRAY,
                x=0, y=0,
                speed=2, angle=0,
                ways=8,
            )
            yield 15
        for _ in range(3):
            for s in (1.5, 2):
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_CYAN,
                    x=0, y=0,
                    speed=s, angle=0,
                    ways=21,
                )
            a = common.calcDirectionAiming(ctx, 0, 0)
            for i in range(15):
                if i % 3 == 0:
                    SFX.ENEMY_SHOOT_D.play()
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GRAY,
                    x=0, y=0,
                    speed=4, angle=a,
                    ways=3, fanSize=45,
                )
                yield 3
            common.moveRandom(ctx, 192, 108, 100, 32, 30, lib.utils.easeOutCubicInterpolation)
            yield 30

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter <= 60:
        ctx.speedRadius = lib.utils.linearInterpolation(ctx.frameCounter / 60, 0, getattr(ctx, 'initialSpeed'))
    else:
        ctx.updateCustom = None

def phase0(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(16)
    common.setBossHPRange(ctx, 10000, 143333)
    common.setPhaseName(18)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 143333
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 108, 120, lib.utils.easeOutCubicInterpolation)
    yield 120

    while True:
        common.moveRandom(ctx, 192, 108, 200, 72, 240, lib.utils.easeOutCubicInterpolation)
        for i in range(80):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_A.play()
            for _ in range(5):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_MEDIUM | (
                        BF.COLOR_RED,
                        BF.COLOR_GREEN,
                        BF.COLOR_LIGHT_BLUE,
                        BF.COLOR_LIGHT_ORANGE,
                    )[common.randomInt(0, 3)],
                    x=0, y=0,
                    speed=common.randomFloat(1, 3),
                    angle=common.randomFloat(0, 360),
                )
            yield 3
        yield 30
        for b in lib.globals.groupEnemyBullet:
            b: lib.bullet.enemy_bullet.EnemyBullet
            b.textures = (common.BulletTextures[BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GRAY],)
            b.rotate()
            b.freeze = True
        yield 30
        common.moveRandom(ctx, 192, 108, 300, 72, 150, lib.utils.easeOutCubicInterpolation)
        for _ in range(6):
            SFX.ENEMY_SHOOT_B.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=3, angle=0,
                ways=8, fanSize=150,
                speedAddition=.5, layers=3,
                aiming=True,
            )
            yield 15
        yield 60
        for b in lib.globals.groupEnemyBullet:
            b: lib.bullet.enemy_bullet.EnemyBullet
            if b.freeze:
                setattr(b, 'initialSpeed', common.randomFloat(.5, 1.25))
                b.angle = common.randomFloat(0, 360)
                b.updateCustom = phase0b0
                b.frameCounter = 0
        common.unfreezeBullet()
        yield 270

def general1(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(15)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.moveRandom(ctx, 192, 96, 160, 96, 120, lib.utils.easeOutCubicInterpolation)
    yield 180

    while True:
        for i in range(15):
            SFX.ENEMY_SHOOT_B.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=2.7, angle=270 - 12 * i,
                ways=8, fanSize=120,
            )
            yield 10
        for i in range(10):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=1.2, angle=90 + 18 * i,
                ways=5, fanSize=10,
                speedAddition=.2, layers=3,
            )
            yield 5
        for i in range(15):
            SFX.ENEMY_SHOOT_B.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=2.7, angle=90 + 12 * i,
                ways=8, fanSize=120,
            )
            yield 10
        for i in range(10):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=1.2, angle=270 - 18 * i,
                ways=5, fanSize=10,
                speedAddition=.2, layers=3,
            )
            yield 5
        common.moveRandom(ctx, 192, 96, 160, 96, 45, lib.utils.easeOutCubicInterpolation)
        yield 45

def phase1(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(14)
    common.setBossHPRange(ctx, 10000, 109999)
    common.setPhaseName(19)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 109999
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 128, 90, lib.utils.easeInOutCubicInterpolation)
    yield 120

    k = bool(common.randomInt(0, 1))
    while True:
        common.move(ctx, 192 + (150 if k else -150), 128, 65, lib.utils.easeOutCubicInterpolation)
        for _ in range(8):
            SFX.ENEMY_SHOOT_A.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=1, angle=0, aiming=True,
                ways=21,
                speedAddition=.4, layers=3,
            )
            yield 8
        common.move(ctx, 192 - (150 if k else -150), 96, 5, lib.utils.easeInOutCubicInterpolation)
        yield 5
        for _ in range(3):
            SFX.ENEMY_SHOOT_C.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=1, angle=0, aiming=True,
                ways=7, fanSize=120,
                speedAddition=.5, layers=4,
            )
            yield 20
        k = not k
        yield 60
        common.move(ctx, 192, 128, 180, lib.utils.linearInterpolation)
        yield 240

def general2(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(13)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.extendHyper(ctx)
    common.moveRandom(ctx, 192, 108, 200, 72, 120, lib.utils.easeInOutCubicInterpolation)
    yield 180

    a = common.randomInt(0, 360)
    k = 0
    while True:
        if k % 70 == 0:
            common.moveRandom(ctx, 192, 108, 200, 72, 180, lib.utils.easeInOutCubicInterpolation)
        SFX.ENEMY_SHOOT_A.play()
        for i in range(5):
            c = (
                BF.COLOR_LIGHT_RED,
                BF.COLOR_LIGHT_MAGENTA,
                BF.COLOR_LIGHT_BLUE,
                BF.COLOR_LIGHT_GREEN,
                BF.COLOR_LIGHT_ORANGE,
            )[i]
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | c,
                x=0, y=0,
                speed=.8, angle=a + 72 * i + k * 7,
                ways=1,
                deflection=-90, radius=50,
            )
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | c,
                x=0, y=0,
                speed=1.2, angle=a + 72 * i + k * 7,
                ways=1,
                deflection=-90 + abs(((k % 70) - 35) / 35 * 60) - 30, radius=50,
            )
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | c,
                x=0, y=0,
                speed=2, angle=a + 72 * i + k * 7,
                ways=1,
                deflection=-90 + abs(((k % 70) - 35) / 35 * 120) - 60, radius=50,
            )
        k += 1
        yield 8

def phase2(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(12)
    common.setBossHPRange(ctx, 10000, 143333)
    common.setPhaseName(20)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 143333
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 96, 90, lib.utils.easeInOutCubicInterpolation)
    yield 120

    k = 0
    while True:
        if k % 2 == 0:
            SFX.ENEMY_SHOOT_B.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | (BF.COLOR_LIGHT_RED if k % 4 == 2 else BF.COLOR_LIGHT_BLUE),
                x=0, y=0,
                speed=1, angle=k * 4,
                ways=9,
            )
        common.shoot(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
            x=common.randomInt(-202, -197), y=common.randomInt(-96, 352),
            speed=common.randomFloat(.5, 1.2), angle=common.randomFloat(255, 265),
        )
        common.shoot(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_GREEN,
            x=common.randomInt(197, 202), y=common.randomInt(-96, 352),
            speed=common.randomFloat(.5, 1.2), angle=common.randomFloat(105, 115),
        )
        k += 1
        yield 10

def general3(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(11)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.move(ctx, 192, 108, 120, lib.utils.easeInOutCubicInterpolation)
    yield 180

    k = 0
    while True:
        if k % 10 == 7:
            common.moveRandom(ctx, 192, 108, 64, 32, 40, lib.utils.easeInOutCubicInterpolation)
        SFX.ENEMY_SHOOT_B.play()
        for i in range(4):
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=1.4 + i * .075,
                angle=-(k * 11 + i * 2),
                ways=8,
            )
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=1.8 + i * .075,
                angle=k * 11 + i * 2,
                ways=8,
            )
        k += 1
        yield 20

def phase3b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 50:
        if ctx.frameCounter % 10 == 0:
            SFX.ENEMY_SHOOT_D.play()
        if ctx.frameCounter % 5 == 0 or ctx.frameCounter % 5 == 2:
            common.shoot(
                ctx,
                bullet=(BF.TYPE_ROUND_MEDIUM | BF.COLOR_RED) if ctx.frameCounter % 5 == 2 else (BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED),
                x=0, y=0,
                speed=1, angle=ctx.angle,
                update=phase3b1,
            ).update()
            common.shoot(
                ctx,
                bullet=(BF.TYPE_ROUND_MEDIUM | BF.COLOR_BLUE) if ctx.frameCounter % 5 == 2 else (BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE),
                x=0, y=0,
                speed=1, angle=ctx.angle - 30,
                update=phase3b1,
            ).update()
            common.shoot(
                ctx,
                bullet=(BF.TYPE_ROUND_MEDIUM | BF.COLOR_BLUE) if ctx.frameCounter % 5 == 2 else (BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE),
                x=0, y=0,
                speed=1, angle=ctx.angle + 30,
                update=phase3b1,
            ).update()
    else:
        ctx.explode()

def phase3b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 90:
        ctx.speedRadius = lib.utils.linearInterpolation(ctx.frameCounter / 90, 1, 7)
    else:
        ctx.updateCustom = None

def phase3(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(10)
    common.setBossHPRange(ctx, 10000, 109999)
    common.setPhaseName(21)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 109999
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    yield 120

    k = 0
    while True:
        x = 60 * math.sin(k / 32 * 2 * math.pi)
        for i in range(10):
            common.shoot(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_CYAN,
                x=min(4 * k, 100) + x - 20 * i - ctx.position.x, y=-ctx.position.y - 5,
                speed=2, angle=180,
            )
            common.shoot(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_CYAN,
                x=384 - min(4 * k, 100) + x + 20 * i - ctx.position.x, y=-ctx.position.y - 5,
                speed=2, angle=180,
            )
        if k % 8 == 0:
            common.moveRandom(ctx, 192, 72, 160, 80, 60, lib.utils.easeOutCubicInterpolation)
        if k % 8 == 0 or k % 8 == 5:
            SFX.ENEMY_SHOOT_B.play()
            common.shootAiming(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_GRAY,
                x=common.randomFloat(10, 25) * (common.randomInt(0, 1) - .5) * 2,
                y=common.randomFloat(10, 25) * (common.randomInt(0, 1) - .5) * 2,
                speed=0, angle=0,
                update=phase3b0,
            )
        k += 1
        yield 10

def general4b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < -3 or ctx.position.x > 387:
        ctx.angle = -ctx.angle
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_RED],)
        ctx.rotate()
        ctx.updateCustom = None
    elif ctx.position.y < -3:
        ctx.angle = 180 - ctx.angle
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_RED],)
        ctx.rotate()
        ctx.updateCustom = None

def general4(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(9)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.move(ctx, 192, 108, 120, lib.utils.easeInOutCubicInterpolation)
    common.extendLife(ctx)
    yield 180

    k = 0
    while True:
        if k % 10 == 7:
            common.moveRandom(ctx, 192, 108, 64, 32, 40, lib.utils.easeInOutCubicInterpolation)
        SFX.ENEMY_SHOOT_B.play()
        for i in range(8):
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_BLUE,
                x=0, y=0,
                speed=1.4 + i * .03,
                angle=k * 11 + i * .8 + 45,
                ways=4,
                update=general4b0,
            )
        k += 1
        yield 20

def phase4b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < -5:
        ctx.position.x += 394
        ctx.updateCustom = phase4b1
    elif ctx.position.x > 389:
        ctx.position.x -= 394
        ctx.updateCustom = phase4b1

def phase4b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < -5:
        ctx.position.x += 394
        ctx.updateCustom = None
    elif ctx.position.x > 389:
        ctx.position.x -= 394
        ctx.updateCustom = None

def phase4(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(8)
    common.setBossHPRange(ctx, 10000, 143333)
    common.setPhaseName(22)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 143333
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    yield 120

    k = True
    while True:
        for i in range(36):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            if i == 12:
                common.moveRandom(ctx, 192, 108, 64, 48, 30, lib.utils.easeOutCubicInterpolation)
            for _ in range(2):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | (BF.COLOR_GREEN if k else BF.COLOR_LIGHT_CYAN),
                    x=0, y=0,
                    speed=3,
                    angle=180 + (45 + i * 2.5 + common.randomFloat(-10, 10)) * (-1 if k else 1),
                    update=phase4b0,
                )
            yield 5
        k = not k

def general5(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(7)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.moveRandom(ctx, 192, 108, 64, 32, 180, lib.utils.easeOutCubicInterpolation)
    yield 180

    while True:
        a = common.calcDirectionAiming(ctx, 0, 0)
        for i in range(12):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=6, angle=a,
                ways=i + 1, fanSize=i * 2,
                update=common.bulletChangeSpeed((
                    (15, -3),
                )),
            )
            yield 4
        a = common.calcDirectionAiming(ctx, 0, 0)
        for i in range(12):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=6, angle=a,
                ways=i + 13, fanSize=(i + 12) * 12,
                update=common.bulletChangeSpeed((
                    (15, -3),
                )),
            )
            yield 4
        SFX.ENEMY_SHOOT_B.play()
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_BLUE,
            x=0, y=0,
            speed=1, angle=0,
            ways=1,
            speedAddition=.2, layers=8,
            aiming=True,
        )
        common.moveRandom(ctx, 192, 108, 64, 32, 60, lib.utils.easeOutCubicInterpolation)
        yield 60

def phase5(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(6)
    common.setBossHPRange(ctx, 10000, 143333)
    common.setPhaseName(23)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 143333
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    yield 120

    a = 0
    b = 0
    k = 0
    while True:
        if k % 60 == 0:
            common.moveRandom(ctx, 192, 108, 32, 32, 40, lib.utils.easeOutCubicInterpolation)
        if k % 2 == 0:
            SFX.ENEMY_SHOOT_D.play()
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE,
            x=0, y=0,
            speed=1.5, angle=k * 7,
            ways=8,
            radius=50,
        )
        if k % 60 == 10:
            a = common.calcDirectionAiming(ctx, 0, 0)
        if 10 <= k % 60 and k % 60 < 46:
            for b, c in (
                (10, 0),
                (14, 60),
                (18, -60),
                (22, 30),
                (26, -30),
                (30, 15),
                (34, -15),
                (38, 0),
            ):
                if b <= k % 60 and k % 60 < b + 8:
                    if ((k % 60) - b) % 4 == 0:
                        SFX.ENEMY_SHOOT_E.play()
                    common.shootMultiWay(
                        ctx,
                        bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
                        x=0, y=0,
                        speed=6, angle=a + c,
                        ways=(k % 60 - b) + 1, fanSize=(k % 60 - b) * 1.375,
                        update=common.bulletChangeSpeed((
                            (15, -3),
                        )),
                    )
        k += 1
        yield 4

def general6(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(5)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.moveRandom(ctx, 192, 108, 96, 72, 120, lib.utils.easeInOutCubicInterpolation)
    common.extendHyper(ctx)
    yield 180

    k = True
    while True:
        for i in range(30):
            if i % 2 == 0:
                SFX.ENEMY_SHOOT_D.play()
            if i == 15:
                common.moveRandom(ctx, 192, 108, 96, 72, 60, lib.utils.easeInOutCubicInterpolation)
            for j in range(2):
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
                    x=0, y=0,
                    speed=2.5 + j * .1,
                    angle=(i * 7 - j * 1 - 30) * (1 if k else -1),
                    ways=11,
                )
            yield 5
        k = not k
        yield 10

def phase6b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter % 90 == 0:
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_CYAN,
            x=0, y=0,
            speed=1,
            angle=common.randomFloat(0, 360),
            ways=24,
        ):
            b.update()
    if ctx.frameCounter == 0:
        setattr(ctx, 'angle', common.calcDirectionAiming(lib.globals.groupBoss.sprite, 0, 0))
    if ctx.frameCounter % 5 == 0:
        common.shoot(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GRAY,
            x=0, y=0,
            speed=3,
            angle=getattr(ctx, 'angle'),
        ).update()
    if ctx.frameCounter > 180:
        ctx.explode()

def phase6(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(4)
    common.setBossHPRange(ctx, 10000, 143333)
    common.setPhaseName(24)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 143333
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 192, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120

    while True:
        for x, y in (
            (34, 70),
            (93, 50),
            (163, 50),
            (223, 72),
            (253, 120),
            (323, 120),
            (353, 70),
        ):
            common.shoot(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_GRAY,
                x=x - ctx.position.x, y=y - ctx.position.y,
                speed=0, angle=0,
                update=phase6b0,
            )
        for _ in range(3):
            SFX.ENEMY_SHOOT_C.play()
            yield 90

def general7(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 76666)
    common.setPhaseName(0)
    ctx.hitpoint = 76666
    ctx.invincibleRemain = 180
    ctx.blockHyper = False
    common.setCountdown(35 * 60 + 180, 35 * 60)
    common.moveRandom(ctx, 192, 108, 64, 32, 120, lib.utils.easeOutCubicInterpolation)
    yield 180

    k = 0
    while True:
        if k % 9 == 8:
            common.moveRandom(ctx, 192, 108, 64, 32, 60, lib.utils.easeOutCubicInterpolation)
        SFX.ENEMY_SHOOT_B.play()
        for i in range(7):
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_ORANGE,
                x=0, y=0,
                speed=1,
                angle=(k % 8) * 15 + (6 - i) * 11,
                ways=3,
                radius=5 + 4 * i,
            )
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_ORANGE,
                x=0, y=0,
                speed=1,
                angle=(-k % 8) * 15 - (6 - i) * 11,
                ways=3,
                radius=5 + 4 * i,
            )
        k += 1
        yield 20

def phase7b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    a = None
    if ctx.position.x < 0:
        a = 270
    elif ctx.position.x > 384:
        a = 90
    elif ctx.position.y < 0:
        a = 180
    elif ctx.position.y > 448:
        a = 0
    if a is not None:
        for _ in range(3):
            common.shoot(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=0, y=0,
                speed=common.randomFloat(1, 3),
                angle=a + common.randomFloat(-90, 90),
                update=phase7b1,
            ).update()
        ctx.explode()

def phase7b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 20:
        ctx.explode()

def phase7b2(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    a = None
    if ctx.position.x < 0:
        a = 270
    elif ctx.position.x > 384:
        a = 90
    elif ctx.position.y < 0:
        a = 180
    elif ctx.position.y > 448:
        a = 0
    if a is not None:
        SFX.ENEMY_SHOOT_C.play()
        for _ in range(common.randomInt(2, 5)):
            common.shoot(
                ctx,
                bullet=(BF.TYPE_ROUND_TINY, BF.TYPE_ROUND_TINY, BF.TYPE_ROUND_LARGE)[common.randomInt(0, 2)] | BF.COLOR_ORANGE,
                x=0, y=0,
                speed=common.randomFloat(.25, 1),
                angle=a + common.randomFloat(-90, 90),
            ).update()
        ctx.explode()

def phase7(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 87777)
    common.setPhaseName(25)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (75 * 60 + 120) * .9),
    )
    ctx.hitpoint = 87777
    ctx.invincibleRemain = 120
    ctx.blockHyper = True
    common.setCountdown(75 * 60 + 120, 75 * 60)
    common.move(ctx, 192, 224, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120

    k = -12
    while True:
        if k % 2 == 0:
            SFX.ENEMY_SHOOT_D.play()
        if k > 0 and k % 24 == 0:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=3, angle=max(k, 0) * -1.5,
                ways=5,
                update=phase7b2,
            )
        else:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=3, angle=max(k, 0) * -1.5,
                ways=5,
                update=phase7b0,
            )
        k += 1
        yield 5

def phase8b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter >= 30:
        ctx.speedRadius -= .01
    if ctx.speedRadius <= 0:
        ctx.speedRadius = 0
        ctx.frameCounter = 0
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_GREEN],)
        ctx.size = common.BulletSizes[BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_GREEN]
        ctx.angle = (90 if ctx.position.x > 192 else -90) + common.randomFloat(-10, 10)
        ctx.rotate()
        ctx.updateCustom = phase8b1

def phase8b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter <= 60:
        ctx.speedRadius = lib.utils.linearInterpolation(
            ctx.frameCounter / 60,
            0,
            1.5,
        )
    else:
        ctx.updateCustom = None

def phase8b2(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    ctx.speedRadius -= .01
    if ctx.speedRadius <= 0:
        ctx.speedRadius = 0
        ctx.frameCounter = 0
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED],)
        ctx.size = common.BulletSizes[BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED]
        ctx.angle = common.calcDirectionAiming(ctx, 0, 0)
        ctx.rotate()
        ctx.updateCustom = phase8b3

def phase8b3(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter <= 60:
        ctx.speedRadius = lib.utils.linearInterpolation(
            ctx.frameCounter / 60,
            0,
            1.5,
        )
    else:
        ctx.updateCustom = None

def phase8b4(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter <= 60:
        ctx.speedRadius = lib.utils.linearInterpolation(
            ctx.frameCounter / 60,
            0,
            1,
        )
    else:
        ctx.updateCustom = None

def phase8(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.dropPointItem(ctx, 30)
    common.bonusPhase()
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 1009999)
    common.setPhaseName(26)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        0,
    )
    ctx.hitpoint = 1009999
    ctx.invincibleRemain = 1048576
    ctx.blockHyper = True
    common.setCountdown(75 * 60 + 180, 75 * 60)
    common.moveRandom(ctx, 192, -32, 64, 0, 180, lib.utils.easeInOutCubicInterpolation)
    common.extendLife(ctx)
    yield 180
    ctx.blockHoming = True
    hitbox = ctx.hitbox
    ctx.hitbox = []

    k = 0
    while True:
        if k % 240 == 0:
            SFX.ENEMY_SHOOT_B.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GREEN,
                x=48 - ctx.position.x, y=224 - ctx.position.y,
                speed=.25, angle=90,
                ways=2,
                speedAddition=.3, layers=8,
                update=phase8b0,
            )
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GREEN,
                x=336 - ctx.position.x, y=224 - ctx.position.y,
                speed=.25, angle=-90,
                ways=2,
                speedAddition=.3, layers=8,
                update=phase8b0,
            )
        if lib.globals.timeCountdown < 50 * 60 and k % 240 == 120:
            SFX.ENEMY_SHOOT_C.play()
            for x, y in (
                (48, 48),
                (48, 400),
                (336, 48),
                (336, 400),
            ):
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GREEN,
                    x=x - ctx.position.x, y=y - ctx.position.y,
                    speed=1, angle=0,
                    ways=5, fanSize=120,
                    update=phase8b2,
                )
        if lib.globals.timeCountdown < 25 * 60 and k % 60 == 0:
            SFX.ENEMY_SHOOT_A.play()
            a = lib.utils.linearInterpolation(lib.globals.timeCountdown / (25 * 60), 32, 144)
            for s in (1, -1):
                for y in (48, 400):
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_RED,
                        x=192 + s * a - ctx.position.x, y=y - ctx.position.y,
                        speed=0, angle=0,
                        update=phase8b4,
                    )
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_BLUE,
                        x=192 + s * a - ctx.position.x, y=y - ctx.position.y,
                        speed=0, angle=180,
                        update=phase8b4,
                    )
        if lib.globals.timeCountdown == 1:
            lib.globals.timeCountdown += 1
            ctx.hitpoint = 9999
            ctx.blockHoming = False
            ctx.hitbox = hitbox
        k += 1
        yield 1

def phase9b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < -3 or ctx.position.x > 387:
        ctx.angle = -ctx.angle
        ctx.rotate()
        ctx.updateCustom = None
    elif ctx.position.y < -3:
        ctx.angle = 180 - ctx.angle
        ctx.rotate()
        ctx.updateCustom = None

def phase9(ctx: lib.sprite.enemy.Enemy):
    # ctx.hitpoint = 9999; return
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.dropPointItem(ctx, 30)
    common.bonusPhase()
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 309999)
    common.setPhaseName(27)
    common.setPhaseBonus(
        (30 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 6) * lib.globals.maxGetPoint) / (100 * 60 + 180) * .9),
    )
    ctx.hitpoint = 309999
    ctx.invincibleRemain = 180
    ctx.blockHyper = True
    common.setCountdown(100 * 60 + 180, 100 * 60)
    common.move(ctx, 192, 72, 180, lib.utils.easeInOutCubicInterpolation)
    yield 180

    yield common.charge(ctx.position)
    while True:
        if lib.globals.timeCountdown == 1200 and ctx.hitpoint > 109999:
            ctx.hitpoint = 109999
        SFX.ENEMY_SHOOT_C.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_BLUE,
            x=common.randomFloat(-60, 60), y=common.randomFloat(-25, 25),
            speed=1, angle=0,
            ways=75,
            update=phase9b0,
        )
        if ctx.hitpoint <= 109999:
            t = 90
        elif ctx.hitpoint <= 209999:
            t = 135
        else:
            t = 180
        yield t

def beforeDeath(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.moveRandom(ctx, 192, 144, 160, 72, 400, lib.utils.easeInOutCubicInterpolation)
    ctx.blockHyper = False
    ctx.invincibleRemain = 1048576
    ctx.pointItemNum = 50

    for i, t in (
        (3, 60),
        (4, 30),
        (4, 15),
        (8, 5),
    ):
        for _ in range(i):
            (
                SFX.EXPLODE_ENEMY_A,
                SFX.EXPLODE_ENEMY_B,
                SFX.EXPLODE_ENEMY_C,
            )[common.randomInt(0, 2)].play()
            for _ in range(common.randomInt(4, 9)):
                if common.randomInt(0, 1):
                    p = ctx.position + pygame.Vector2(
                        common.randomInt(-30, 30),
                        common.randomInt(-8, -1),
                    )
                    (
                        debris.DebrisA,
                        debris.DebrisB,
                    )[common.randomInt(0, 1)](
                        p,
                        common.randomFloat(1, 2),
                        common.randomFloat(2, 5),
                    )
                else:
                    p = ctx.position + pygame.Vector2(
                        common.randomInt(-3, 3),
                        common.randomInt(-20, 16),
                    )
                    (
                        debris.DebrisA,
                        debris.DebrisB,
                    )[common.randomInt(0, 1)](
                        p,
                        common.randomFloat(1, 2),
                        common.randomFloat(2, 5),
                    )
                (
                    explosion.ExplosionPlaneSmallA,
                    explosion.ExplosionPlaneSmallB,
                    explosion.ExplosionPlaneMediumA,
                    explosion.ExplosionPlaneMediumB,
                    explosion.ExplosionPlaneLarge,
                )[common.randomInt(0, 3)](p)
            yield t
    ctx.hitpoint = 0

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
    general2,
    phase2,
    general3,
    phase3,
    general4,
    phase4,
    general5,
    phase5,
    general6,
    phase6,
    general7,
    phase7,
    phase8,
    phase9,
    beforeDeath,
)