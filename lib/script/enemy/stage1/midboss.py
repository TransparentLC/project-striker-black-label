import pygame

import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_A_NORMAL
    ctx.interval = 1
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
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 128, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 66934)
    common.setCountdown(25 * 60 + 120, 25 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    while True:
        for x, y in (
            (-41, -24),
            (-21, -25),
            (21, -25),
            (41, -24),
        ):
            a = common.calcDirectionAiming(ctx, x, y)
            for _ in range(3):
                SFX.ENEMY_SHOOT_B.play()
                common.shootComplex(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                    x=x, y=y,
                    speed=(2, 2.25, 2.5)[lib.globals.difficultyType], angle=a,
                    ways=(1, 3, 9)[lib.globals.difficultyType],
                    fanSize=(60, 60, 120)[lib.globals.difficultyType],
                )
                yield 10
        for _ in range((2, 3, 4)[lib.globals.difficultyType]):
            SFX.ENEMY_SHOOT_C.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_ORANGE,
                x=0, y=-5,
                speed=4, angle=0,
                ways=(15, 25, 35)[lib.globals.difficultyType],
                update=common.bulletChangeSpeed((
                    (10, -2),
                )),
            )
            if lib.globals.difficultyType == 2:
                for i in (2.5, 3):
                    common.shootAimingMultiWay(
                        ctx,
                        bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_ORANGE,
                        x=0, y=-5,
                        speed=i, angle=0,
                        ways=5,
                        fanSize=45,
                    )
            yield 20
        common.moveRandom(ctx, 192, 128, 150, 128, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.dropPointItem(ctx, 14)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 69361)
    ctx.invincibleRemain = 210
    common.setCountdown(25 * 60 + 210, 25 * 60)
    common.move(ctx, 192, 96, 150, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120
    x = -8
    while True:
        a = common.calcDirectionAiming(ctx, x, 18)
        b = (2, 4, 6)[lib.globals.difficultyType]
        for i in range((10, 18, 26)[lib.globals.difficultyType]):
            if i % 5 == 0:
                SFX.ENEMY_SHOOT_D.play()
            i -= b
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=x, y=18,
                speed=(2, 2.25, 2.5)[lib.globals.difficultyType],
                angle=a + (1 if x < 0 else -1) * (10, 8, 6)[lib.globals.difficultyType] * i + common.randomFloat(-2, 2),
                ways=1,
                speedAddition=(.25, .25, .5)[lib.globals.difficultyType],
                layers=(1, 2, 3)[lib.globals.difficultyType],
            )
            yield 3
        x = -x

def escape(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.dropPointItem(ctx, 20)
    common.moveRelative(ctx, 0, -180, 60, lib.utils.easeInCubicInterpolation)
    common.moveRelative(ctx, 0, -200, 1, lib.utils.easeInCubicInterpolation)
    ctx.invincibleRemain = 120
    yield 60

functions = (
    setup,
    general0,
    general1,
    escape,
)