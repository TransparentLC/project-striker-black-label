from re import X
import pygame

import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite
import lib.sprite.enemy
import lib.sprite.explosion as explosion
import lib.sprite.debris as debris
from lib.stg_overlay import update
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_A_NORMAL
    ctx.interval = 1
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-19, -17), 11),
        lib.sprite.Hitbox(pygame.Vector2(-31, -18), 10),
        lib.sprite.Hitbox(pygame.Vector2(-42, -18), 9),
        lib.sprite.Hitbox(pygame.Vector2(-54, -18), 8),
        lib.sprite.Hitbox(pygame.Vector2(-63, -18), 7),
        lib.sprite.Hitbox(pygame.Vector2(-73, -18), 6),
        lib.sprite.Hitbox(pygame.Vector2(-41, -33), 5),
        lib.sprite.Hitbox(pygame.Vector2(-41, -28), 5),
        lib.sprite.Hitbox(pygame.Vector2(-21, -37), 5),
        lib.sprite.Hitbox(pygame.Vector2(-21, -30), 5),
        lib.sprite.Hitbox(pygame.Vector2(-9, 38), 8),
        lib.sprite.Hitbox(pygame.Vector2(-19, 38), 7),
        lib.sprite.Hitbox(pygame.Vector2(-29, 38), 6),
        lib.sprite.Hitbox(pygame.Vector2(-37, 39), 5),
        lib.sprite.Hitbox(pygame.Vector2(19, -17), 11),
        lib.sprite.Hitbox(pygame.Vector2(31, -18), 10),
        lib.sprite.Hitbox(pygame.Vector2(42, -18), 9),
        lib.sprite.Hitbox(pygame.Vector2(54, -18), 8),
        lib.sprite.Hitbox(pygame.Vector2(63, -18), 7),
        lib.sprite.Hitbox(pygame.Vector2(73, -18), 6),
        lib.sprite.Hitbox(pygame.Vector2(41, -33), 5),
        lib.sprite.Hitbox(pygame.Vector2(41, -28), 5),
        lib.sprite.Hitbox(pygame.Vector2(21, -37), 5),
        lib.sprite.Hitbox(pygame.Vector2(21, -30), 5),
        lib.sprite.Hitbox(pygame.Vector2(9, 38), 8),
        lib.sprite.Hitbox(pygame.Vector2(19, 38), 7),
        lib.sprite.Hitbox(pygame.Vector2(29, 38), 6),
        lib.sprite.Hitbox(pygame.Vector2(37, 39), 5),
        lib.sprite.Hitbox(pygame.Vector2(0, -48), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, -38), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, -30), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, -14), 16),
        lib.sprite.Hitbox(pygame.Vector2(0, 6), 11),
        lib.sprite.Hitbox(pygame.Vector2(0, 20), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, 29), 5),
        lib.sprite.Hitbox(pygame.Vector2(0, 41), 7),
    )
    ctx.debris = (
        (debris.DebrisB, pygame.Vector2(-12, 51), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(12, 51), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 30), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(0, 12), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -6), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, -38), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(-40, -30), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-74, -28), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(40, -30), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(74, -28), .125, 2, 1, 5, 2),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 128, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 60468)
    common.setPhaseName(0)
    ctx.hitpoint = 60468
    common.setCountdown(25 * 60 + 120, 25 * 60)
    yield 120

def general0(ctx: lib.sprite.enemy.Enemy):
    x = -1
    while True:
        x = -x
        for i in range(24):
            if i % 8 == 0:
                SFX.ENEMY_SHOOT_D.play()
            for j in range((3, 4, 5)[lib.globals.difficultyType]):
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_RED,
                    x=0, y=-5,
                    speed=7 + j * .2,
                    angle=(i * 15 + j * 5) * x,
                    ways=(1, 2, 3)[lib.globals.difficultyType],
                    fanSize=60,
                    update=common.bulletChangeSpeed((
                        (5, -6),
                    )),
                )
            yield 2
        common.moveRandom(ctx, 192, 128, 300, 96, 120, lib.utils.easeInOutCubicInterpolation)
        yield 120

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 120:
        ctx.angle += 60
        ctx.speedRadius /= 2
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_DUAL | BF.COLOR_GRAY],)
        ctx.rotate()
        ctx.updateCustom = None

def phase0b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 120:
        ctx.angle -= 60
        ctx.speedRadius /= 2
        ctx.textures = (common.BulletTextures[BF.TYPE_SHELL_DUAL | BF.COLOR_GRAY],)
        ctx.rotate()
        ctx.updateCustom = None

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 117361)
    common.setPhaseName(1)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 1) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 1) * lib.globals.maxGetPoint) / (40 * 60 + 120) * .9),
    )
    ctx.hitpoint = 117361
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(40 * 60 + 120, 40 * 60)
    common.move(ctx, 192, 128, 120, lib.utils.easeInOutCubicInterpolation)
    yield 120
    a = False
    while True:
        b = (120 if a else 240) + common.randomFloat(-45, 45)
        for i in range(10):
            if i == 0:
                SFX.ENEMY_SHOOT_E.play()
            if (
                (i % 4 == 0 and lib.globals.difficultyType == 0) or
                (i % 2 == 0 and lib.globals.difficultyType == 1) or
                lib.globals.difficultyType == 2
            ):
                common.shootComplex(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_ORANGE,
                    x=(-41 if a else 41), y=-24,
                    speed=.5 + (10 - i) / 20,
                    angle=b + i * (12 if a else -12),
                    ways=1,
                    speedAddition=.25 + (10 - i) / 25,
                    layers=3,
                    update=(phase0b0 if a else phase0b1),
                )
            yield 1
        yield 60
        a = not a

def general1(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_A_BREAK
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 22)
    common.moveClear(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 67254)
    common.setPhaseName(0)
    ctx.hitpoint = 67254
    ctx.invincibleRemain = 210
    common.setCountdown(25 * 60 + 210, 25 * 60)
    common.move(ctx, 192, 96, 150, lib.utils.easeOutCubicInterpolation)
    yield 180
    x = -1
    while True:
        x = -x
        for i in range(24):
            if i % 8 == 0:
                SFX.ENEMY_SHOOT_D.play()
            for j in range((3, 4, 5)[lib.globals.difficultyType]):
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_RED,
                    x=0, y=-5,
                    speed=7 + j * .2,
                    angle=(i * 15 + j * 5) * x,
                    ways=(1, 2, 3)[lib.globals.difficultyType],
                    fanSize=60,
                    update=common.bulletChangeSpeed((
                        (5, -6),
                    )),
                )
            yield 2
        for _ in range((1, 2, 3)[lib.globals.difficultyType]):
            SFX.ENEMY_SHOOT_C.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_MAGENTA,
                x=0, y=-5,
                speed=5, angle=0,
                ways=(21, 31, 41)[lib.globals.difficultyType],
                update=common.bulletChangeSpeed((
                    (10, -3.25),
                )),
            )
            yield 15
        common.moveRandom(ctx, 192, 96, 200, 64, 90, lib.utils.easeInOutCubicInterpolation)
        yield 90

def phase1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 0, 128274)
    common.setPhaseName(2)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 1) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 1) * lib.globals.maxGetPoint) / (40 * 60 + 120) * .9),
    )
    ctx.hitpoint = 128274
    ctx.invincibleRemain = 90 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(40 * 60 + 120, 40 * 60)
    yield 60
    while True:
        common.moveRandom(ctx, 192, 96, 100, 96, 60, lib.utils.easeOutCubicInterpolation)
        yield 60
        for _ in range(20):
            SFX.ENEMY_SHOOT_A.play()
            for _ in range((4, 10, 18)[lib.globals.difficultyType]):
                common.shoot(
                    ctx,
                    bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_GRAY,
                    x=0, y=-5,
                    speed=common.randomFloat(1.75, 2.25),
                    angle=common.randomFloat(0, 360),
                )
            yield 5
        yield 60
        common.freezeBullet()
        yield common.charge(ctx.position + pygame.Vector2(0, -5))
        pos = (
            [-41, -24, 0],
            [-21, -25, 0],
            [21, -25, 0],
            [41, -24, 0],
        )
        for p in pos:
            p[2] = common.calcDirectionAiming(ctx, p[0], p[1])
        for i in range(24):
            if i % 3 == 0:
                SFX.ENEMY_SHOOT_D.play()
            for x, y, a in pos:
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_GRAY,
                    x=x, y=y,
                    speed=4, angle=a + common.randomFloat(-2, 2),
                    ways=(6, 10, 6)[lib.globals.difficultyType],
                    fanSize=(150, 150, 60)[lib.globals.difficultyType],
                    update=common.bulletChangeType((
                        (40, BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED),
                    )),
                )
            yield 4
        yield 30
        common.unfreezeBullet()
        yield 60

def death(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 25)

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
)