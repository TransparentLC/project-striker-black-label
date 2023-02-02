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
    ctx.textures = common.EnemyTextures.BOSS_E_NORMAL
    ctx.interval = 1
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-227, -32), 12),
        lib.sprite.Hitbox(pygame.Vector2(-213, -29), 14),
        lib.sprite.Hitbox(pygame.Vector2(-195, -27), 16),
        lib.sprite.Hitbox(pygame.Vector2(-176, -25), 18),
        lib.sprite.Hitbox(pygame.Vector2(-155, -24), 20),
        lib.sprite.Hitbox(pygame.Vector2(-133, -22), 21),
        lib.sprite.Hitbox(pygame.Vector2(-113, -21), 22),
        lib.sprite.Hitbox(pygame.Vector2(-90, -21), 22),
        lib.sprite.Hitbox(pygame.Vector2(-65, -20), 23),
        lib.sprite.Hitbox(pygame.Vector2(-39, -19), 25),
        lib.sprite.Hitbox(pygame.Vector2(-15, -18), 26),
        lib.sprite.Hitbox(pygame.Vector2(-168, -49), 8),
        lib.sprite.Hitbox(pygame.Vector2(-120, -49), 8),
        lib.sprite.Hitbox(pygame.Vector2(-72, -48), 8),
        lib.sprite.Hitbox(pygame.Vector2(-52, 84), 8),
        lib.sprite.Hitbox(pygame.Vector2(-43, 83), 8),
        lib.sprite.Hitbox(pygame.Vector2(-32, 82), 10),
        lib.sprite.Hitbox(pygame.Vector2(-21, 81), 11),
        lib.sprite.Hitbox(pygame.Vector2(-10, 79), 12),
        lib.sprite.Hitbox(pygame.Vector2(227, -32), 12),
        lib.sprite.Hitbox(pygame.Vector2(213, -29), 14),
        lib.sprite.Hitbox(pygame.Vector2(195, -27), 16),
        lib.sprite.Hitbox(pygame.Vector2(176, -25), 18),
        lib.sprite.Hitbox(pygame.Vector2(155, -24), 20),
        lib.sprite.Hitbox(pygame.Vector2(133, -22), 21),
        lib.sprite.Hitbox(pygame.Vector2(113, -21), 22),
        lib.sprite.Hitbox(pygame.Vector2(90, -21), 22),
        lib.sprite.Hitbox(pygame.Vector2(65, -20), 23),
        lib.sprite.Hitbox(pygame.Vector2(39, -19), 25),
        lib.sprite.Hitbox(pygame.Vector2(15, -18), 26),
        lib.sprite.Hitbox(pygame.Vector2(168, -49), 8),
        lib.sprite.Hitbox(pygame.Vector2(120, -49), 8),
        lib.sprite.Hitbox(pygame.Vector2(72, -48), 8),
        lib.sprite.Hitbox(pygame.Vector2(52, 84), 8),
        lib.sprite.Hitbox(pygame.Vector2(43, 83), 8),
        lib.sprite.Hitbox(pygame.Vector2(32, 82), 10),
        lib.sprite.Hitbox(pygame.Vector2(21, 81), 11),
        lib.sprite.Hitbox(pygame.Vector2(10, 79), 12),
        lib.sprite.Hitbox(pygame.Vector2(0, 86), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, 65), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, 53), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, 39), 10),
        lib.sprite.Hitbox(pygame.Vector2(0, 25), 11),
        lib.sprite.Hitbox(pygame.Vector2(0, 12), 13),
        lib.sprite.Hitbox(pygame.Vector2(0, -46), 19),
        lib.sprite.Hitbox(pygame.Vector2(-10, -62), 10),
        lib.sprite.Hitbox(pygame.Vector2(10, -62), 10),
        lib.sprite.Hitbox(pygame.Vector2(0, -72), 16),
        lib.sprite.Hitbox(pygame.Vector2(0, -88), 10),
    )
    ctx.debris = (
        (debris.DebrisA, pygame.Vector2(-227, -32), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-213, -29), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(-195, -27), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-176, -25), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-155, -24), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(-133, -22), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-113, -21), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(-90, -21), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-65, -20), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-39, -19), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-15, -18), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-168, -49), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-120, -49), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-72, -48), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(-52, 84), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-43, 83), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-32, 82), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-21, 81), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-10, 79), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(227, -32), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(213, -29), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(195, -27), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(176, -25), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(155, -24), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(133, -22), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(113, -21), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(90, -21), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(65, -20), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(39, -19), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(15, -18), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(168, -49), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(120, -49), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(72, -48), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(52, 84), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(43, 83), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(32, 82), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(21, 81), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(10, 79), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 86), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 65), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 53), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, 39), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, 25), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 12), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -46), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-10, -62), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(10, -62), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, -72), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -88), .125, 2, 1, 5, 2),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -80)
    common.move(ctx, 192, 128, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(6)
    common.setBossHPRange(ctx, 10000, 89576)
    common.setPhaseName(0)
    ctx.hitpoint = 89576
    common.setCountdown(40 * 60 + 120, 40 * 60)
    yield 120

def general0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    k = (12, 9, 6)[lib.globals.difficultyType]
    if ctx.frameCounter % k == k - 1:
        SFX.ENEMY_SHOOT_A.play()
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
            x=0, y=0,
            speed=1.5,
            angle=ctx.angle + 45,
            ways=4,
        ):
            b.update()

def general0b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    k = (12, 9, 6)[lib.globals.difficultyType]
    if ctx.frameCounter % k == k - 1:
        SFX.ENEMY_SHOOT_A.play()
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE,
            x=0, y=0,
            speed=1.5,
            angle=ctx.angle + 45,
            ways=4,
        ):
            b.update()

def general0(ctx: lib.sprite.enemy.Enemy):
    k = 0
    while True:
        SFX.ENEMY_SHOOT_C.play()
        common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_LARGE | (BF.COLOR_LIGHT_RED if k % 2 else BF.COLOR_LIGHT_BLUE),
            x=0, y=-32,
            speed=5,
            angle=0,
            ways=4,
            update=general0b0 if k % 2 else general0b1,
        )
        yield 30
        k += 1
        common.moveRandom(ctx, 192, 128, 256, 64, 60, lib.utils.easeInOutCubicInterpolation)
        yield 60

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 90:
        ctx.speedRadius = lib.utils.easeInCubicInterpolation(ctx.frameCounter / 90, 1, 6)

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(5)
    common.setBossHPRange(ctx, 10000, 170421)
    common.setPhaseName(14)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint) / (70 * 60 + 120) * .9),
    )
    ctx.hitpoint = 170421
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(70 * 60 + 120, 70 * 60)
    yield 120

    k = 0
    while True:
        if k % (20, 20, 40)[lib.globals.difficultyType] == 0:
            common.moveRandom(ctx, 192, 96, 150, 100, 900, lib.utils.easeInOutCubicInterpolation)
        if k % (10, 10, 20)[lib.globals.difficultyType] == 0:
            SFX.ENEMY_SHOOT_C.play()
            c = common.randomFloat(0, 360)
            for a in range(0, 360, 20):
                a += c
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_ORANGE,
                    x=0, y=-32,
                    speed=4,
                    angle=a,
                )
                for i in range(3):
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_ORANGE,
                        x=0 + (20 + 20 * i) * math.sin((a + 10) / 180 * math.pi), y=-32 + (20 + 20 * i) * math.cos((a + 10) / 180 * math.pi),
                        speed=4,
                        angle=a,
                    )
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_ORANGE,
                        x=0 + (20 + 20 * i) * math.sin((a - 10) / 180 * math.pi), y=-32 + (20 + 20 * i) * math.cos((a - 10) / 180 * math.pi),
                        speed=4,
                        angle=a,
                    )
                for i in range(5):
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_MAGENTA,
                        x=0 + 15 * math.sin((a + i / 5 * 360) / 180 * math.pi), y=-32 - 15 * math.cos((a + i / 5 * 360) / 180 * math.pi),
                        speed=4,
                        angle=a,
                    )
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_LIME,
                        x=0 + 15 * math.sin((a + i / 5 * 360 + 36) / 180 * math.pi), y=-32 - 15 * math.cos((a + i / 5 * 360 + 36) / 180 * math.pi),
                        speed=4,
                        angle=a,
                    )

        SFX.ENEMY_SHOOT_B.play()
        for _ in range((2, 3, 3)[lib.globals.difficultyType]):
            x = common.randomInt(-192, 192)
            y = common.randomInt(-32, -8)
            a = 180 + x / 384 * 45 + common.randomFloat(-10, 10)
            common.shoot(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_RED,
                x=x, y=y,
                speed=0,
                angle=a,
                update=phase0b0,
            )
            for i in range(3):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED,
                    x=x + (20 + 20 * i) * math.sin((a + 10) / 180 * math.pi), y=y + (20 + 20 * i) * math.cos((a + 10) / 180 * math.pi),
                    speed=0,
                    angle=a,
                    update=phase0b0,
                )
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED,
                    x=x + (20 + 20 * i) * math.sin((a - 10) / 180 * math.pi), y=y + (20 + 20 * i) * math.cos((a - 10) / 180 * math.pi),
                    speed=0,
                    angle=a,
                    update=phase0b0,
                )
            for i in range(5):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_BLUE,
                    x=x + 15 * math.sin((a + i / 5 * 360) / 180 * math.pi), y=y - 15 * math.cos((a + i / 5 * 360) / 180 * math.pi),
                    speed=0,
                    angle=a,
                    update=phase0b0,
                )
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
                    x=x + 15 * math.sin((a + i / 5 * 360 + 36) / 180 * math.pi), y=y - 15 * math.cos((a + i / 5 * 360 + 36) / 180 * math.pi),
                    speed=0,
                    angle=a,
                    update=phase0b0,
                )
        k += 1
        yield (30, 30, 15)[lib.globals.difficultyType]

def general1b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    k = (10, 7, 5)[lib.globals.difficultyType]
    if ctx.frameCounter % k == k - 1:
        SFX.ENEMY_SHOOT_A.play()
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
            x=common.randomFloat(-50, 50), y=0,
            speed=common.randomFloat(2.5, 3.5),
            angle=ctx.angle,
            ways=2,
            update=general1b1,
        ):
            b.update()

def general1b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.y < -5 or ctx.position.y > 453:
        common.shoot(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_MAGENTA,
            x=0, y=0,
            speed=ctx.speedRadius / 3,
            angle=ctx.angle + 180,
        ).update()
        ctx.explode()

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 28 * 3)
    common.moveClear(ctx)
    common.setBossRemain(4)
    common.setBossHPRange(ctx, 10000, 136920)
    common.setPhaseName(0)
    ctx.hitpoint = 136920
    ctx.invincibleRemain = 60
    common.setCountdown(40 * 60 + 60, 40 * 60)
    common.move(ctx, 192, 128, 90, lib.utils.easeInOutCubicInterpolation)
    yield 240

    while True:
        SFX.ENEMY_SHOOT_C.play()
        common.shoot(
            ctx,
            bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_MAGENTA,
            x=0, y=-32,
            speed=5,
            angle=-90,
            update=general1b0,
        )
        common.shoot(
            ctx,
            bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_MAGENTA,
            x=0, y=-32,
            speed=5,
            angle=90,
            update=general1b0,
        )
        yield 30
        common.moveRandom(ctx, 192, 128, 144, 128, 120, lib.utils.easeInOutCubicInterpolation)
        yield 120

def phase1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 168659)
    common.setPhaseName(15)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint) / (60 * 60 + 120) * .9),
    )
    ctx.hitpoint = 168659
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(60 * 60 + 120, 60 * 60)
    common.move(ctx, 192, 224, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120

    yield common.charge(ctx.position - pygame.Vector2(0, 32))
    common.move(ctx, 192, 24, 240, lib.utils.easeInOutCubicInterpolation)
    for k in range(24):
        if k % 2 == 0:
            SFX.ENEMY_SHOOT_E.play()
        for i in (72, 120, 168):
            for _ in range((2, 3, 4)[lib.globals.difficultyType]):
                for j in (-1, 1):
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_TINY | BF.COLOR_RED,
                        x=i * j, y=-52,
                        speed=common.randomFloat(1, 2) - ((k - 12) ** 2 - 144) / 48,
                        angle=180 + common.randomFloat(-10, 10),
                    )
        yield 10
    a = 0
    b = 0
    while True:
        if b % 12 == 11:
            SFX.ENEMY_SHOOT_B.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_RED,
                x=(-168, -120, -72, 72, 120, 168)[common.randomInt(0, 5)], y=-52,
                speed=2, angle=0,
                ways=3, fanSize=30,
                speedAddition=.25, layers=5,
                aiming=True,
            )
        SFX.ENEMY_SHOOT_A.play()
        for i in range(0, 360, (15, 12, 9)[lib.globals.difficultyType]):
            i += a
            x = -180 * math.sin(i / 180 * math.pi)
            y = -64 * math.cos(i / 180 * math.pi)
            for k in (-135, 135):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_ORANGE,
                    x=x, y=y - 32,
                    speed=2,
                    angle=-math.atan2(y * (180 ** 2), x * (64 ** 2)) / math.pi * 180 - 90 + k,
                )
        a += (13, 17, 23)[lib.globals.difficultyType]
        b += 1
        yield 10

def general2(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 33 * 3)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 133671)
    common.setPhaseName(0)
    ctx.hitpoint = 133671
    ctx.invincibleRemain = 180
    common.setCountdown(40 * 60 + 180, 40 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    yield 180

    while True:
        for i in range(4):
            pos = (
                (-96, -24), (96, -24),
                (-48, -24), (48, -24),
                (0, -32),
                (0, 17),
            )[common.randomInt(0, 5)]
            a = common.randomFloat(0, 360)
            b = (13, 25, 37)[lib.globals.difficultyType]
            c = (
                BF.COLOR_LIGHT_RED,
                BF.COLOR_LIGHT_GREEN,
                BF.COLOR_LIGHT_BLUE,
                BF.COLOR_LIGHT_ORANGE,
            )[i]
            d = (1, -1)[common.randomInt(0, 1)]
            for j in range(b):
                if j % (3, 5, 10)[lib.globals.difficultyType] == 0:
                    SFX.ENEMY_SHOOT_D.play()
                common.shootComplex(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | c,
                    x=pos[0], y=pos[1],
                    speed=1.2,
                    speedAddition=.4,
                    angle=a + 360 / b * j * d,
                    ways=1,
                    layers=5,
                )
                yield (3, 2, 1)[lib.globals.difficultyType]
            SFX.ENEMY_SHOOT_B.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_DUAL | c,
                x=pos[0], y=pos[1],
                speed=2.5,
                angle=0,
                ways=3,
                fanSize=15,
            )
        common.moveRandom(ctx, 192, 128, 192, 64, 240, lib.utils.easeInOutCubicInterpolation)
        yield 120

def phase2b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 5:
        setattr(ctx, 'initialSpeed', ctx.speedRadius)
        setattr(ctx, 'changeSpeed', common.randomFloat(.5, 2.5))
    elif 5 <= ctx.frameCounter and ctx.frameCounter <= 35:
        ctx.speedRadius = lib.utils.linearInterpolation((ctx.frameCounter - 5) / 30, getattr(ctx, 'initialSpeed'), 0)
    elif ctx.frameCounter == 65:
        ctx.angle += common.randomFloat(-5, 5)
        ctx.updateCustom = phase2b1

def phase2b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if 65 <= ctx.frameCounter and ctx.frameCounter <= 125:
        ctx.speedRadius = lib.utils.linearInterpolation((ctx.frameCounter - 65) / 60, 0, getattr(ctx, 'changeSpeed'))
    else:
        ctx.updateCustom = None

def phase2(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 172862)
    common.setPhaseName(16)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint) / (70 * 60 + 120) * .9),
    )
    ctx.hitpoint = 172862
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(70 * 60 + 120, 70 * 60)
    common.move(ctx, 192, 96, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120

    while True:
        yield common.charge(ctx.position - pygame.Vector2(0, 32))
        SFX.ENEMY_SHOOT_C.play()
        for i, c in enumerate((
            BF.COLOR_MAGENTA,
            BF.COLOR_LIGHT_BLUE,
            BF.COLOR_LIGHT_CYAN,
            BF.COLOR_LIGHT_GREEN,
            BF.COLOR_LIGHT_ORANGE,
            BF.COLOR_ORANGE,
            BF.COLOR_LIGHT_RED,
        )):
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | c,
                x=0, y=-32,
                speed=1 + i,
                angle=0,
                ways=(35, 45, 55)[lib.globals.difficultyType],
                update=phase2b0,
            )
        common.moveRandom(ctx, 192, 96, 128, 96, 120, lib.utils.easeInOutCubicInterpolation)
        yield 120

def phase3(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 38 * 3)
    common.moveClear(ctx)
    common.move(ctx, 192, 128, 120, lib.utils.easeInOutCubicInterpolation)
    ctx.invincibleRemain = 300
    yield 120
    for _ in range(3):
        SFX.BOSS_ALERT.play()
        yield common.charge(ctx.position - pygame.Vector2(0, 32)) // 2
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 409999)
    common.setPhaseName(17)
    common.setPhaseBonus(
        (30 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 5) * lib.globals.maxGetPoint) / (120 * 60 + 120) * .9),
    )
    ctx.blockHyper = True
    ctx.hitpoint = 409999
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(120 * 60 + 120, 120 * 60)
    common.move(ctx, 192, 128, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120

    k = 0
    m = ctx.hitpoint
    a = common.randomInt(0, 360)
    b = common.randomInt(0, 360)
    c = common.randomInt(0, 360)
    while True:
        if lib.globals.timeCountdown == 1200 and ctx.hitpoint > 109999:
            ctx.hitpoint = 109999
        if ctx.hitpoint <= 109999 and 109999 < m:
            ctx.textures = common.EnemyTextures.BOSS_E_BREAK
        for i in (109999, 209999, 309999):
            if ctx.hitpoint <= i and i < m:
                SFX.PHASE_START.play()
        m = ctx.hitpoint
        if k % 20 == 19:
            SFX.ENEMY_SHOOT_C.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=0, y=-32,
                speed=3, angle=0,
                ways=(25, 29, 35)[lib.globals.difficultyType],
            )
        if k % 4 == 0 and ctx.hitpoint > 109999:
            SFX.ENEMY_SHOOT_D.play()
        elif k % 6 == 0 and ctx.hitpoint <= 109999:
            SFX.ENEMY_SHOOT_E.play()
        if k % 8 < (2, 3, 4)[lib.globals.difficultyType]:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_BLUE,
                x=0, y=-32,
                speed=1.5,
                angle=a + k * 2,
                ways=8,
            )
        if k % 12 < (2, 3, 4)[lib.globals.difficultyType] and ctx.hitpoint <= 309999:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GREEN,
                x=0, y=-32,
                speed=2.5,
                angle=b + k * -2,
                ways=10,
            )
        if k % 16 < (2, 3, 4)[lib.globals.difficultyType] and ctx.hitpoint <= 209999:
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=-32,
                speed=2,
                angle=c + k * 2,
                ways=15,
            )
        if ctx.hitpoint <= 109999:
            for _ in range(2):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_MAGENTA,
                    x=0, y=-32,
                    speed=common.randomFloat(1.5, 2),
                    angle=common.randomFloat(0, 360),
                )
        k += 1
        yield 3

def beforeDeath(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 38 * 3)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.move(ctx, 192, 128, 960, lib.utils.easeInOutCubicInterpolation)
    ctx.blockHyper = False
    ctx.invincibleRemain = 1048576

    for i, t in (
        (4, 60),
        (8, 30),
        (16, 15),
        (32, 5),
        (64, 2),
    ):
        for _ in range(i):
            (
                SFX.EXPLODE_ENEMY_A,
                SFX.EXPLODE_ENEMY_B,
                SFX.EXPLODE_ENEMY_C,
            )[common.randomInt(0, 2)].play()
            for _ in range(common.randomInt(4, 9)):
                if common.randomInt(0, 2):
                    p = ctx.position + pygame.Vector2(
                        common.randomInt(-226, 226),
                        common.randomInt(-42, 0),
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
                        common.randomInt(-13, 13),
                        common.randomInt(-96, 90),
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
                )[common.randomInt(0, 4)](p)
            yield t
    ctx.hitpoint = 0

def death(ctx: lib.sprite.enemy.Enemy):
    if lib.globals.difficultyType == 2 and not lib.globals.continueCount:
        common.extendLife(ctx)

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
    general2,
    phase2,
    phase3,
    beforeDeath,
)