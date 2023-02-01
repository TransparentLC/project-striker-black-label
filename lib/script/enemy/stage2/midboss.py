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
    ctx.textures = common.EnemyTextures.BOSS_B_NORMAL
    ctx.interval = 1
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-10, -15), 12),
        lib.sprite.Hitbox(pygame.Vector2(-22, -16), 11),
        lib.sprite.Hitbox(pygame.Vector2(-34, -16), 10),
        lib.sprite.Hitbox(pygame.Vector2(-44, -16), 9),
        lib.sprite.Hitbox(pygame.Vector2(-54, -16), 8),
        lib.sprite.Hitbox(pygame.Vector2(-65, -16), 7),
        lib.sprite.Hitbox(pygame.Vector2(-73, -16), 6),
        lib.sprite.Hitbox(pygame.Vector2(-7, 39), 8),
        lib.sprite.Hitbox(pygame.Vector2(-15, 39), 7),
        lib.sprite.Hitbox(pygame.Vector2(-22, 39), 6),
        lib.sprite.Hitbox(pygame.Vector2(-28, 39), 6),
        lib.sprite.Hitbox(pygame.Vector2(-36, 40), 5),
        lib.sprite.Hitbox(pygame.Vector2(-25, -34), 5),
        lib.sprite.Hitbox(pygame.Vector2(-25, -28), 5),
        lib.sprite.Hitbox(pygame.Vector2(10, -15), 12),
        lib.sprite.Hitbox(pygame.Vector2(22, -16), 11),
        lib.sprite.Hitbox(pygame.Vector2(34, -16), 10),
        lib.sprite.Hitbox(pygame.Vector2(44, -16), 9),
        lib.sprite.Hitbox(pygame.Vector2(54, -16), 8),
        lib.sprite.Hitbox(pygame.Vector2(65, -16), 7),
        lib.sprite.Hitbox(pygame.Vector2(73, -16), 6),
        lib.sprite.Hitbox(pygame.Vector2(7, 39), 8),
        lib.sprite.Hitbox(pygame.Vector2(15, 39), 7),
        lib.sprite.Hitbox(pygame.Vector2(22, 39), 6),
        lib.sprite.Hitbox(pygame.Vector2(28, 39), 6),
        lib.sprite.Hitbox(pygame.Vector2(36, 40), 5),
        lib.sprite.Hitbox(pygame.Vector2(25, -34), 5),
        lib.sprite.Hitbox(pygame.Vector2(25, -28), 5),
        lib.sprite.Hitbox(pygame.Vector2(0, -25), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, -34), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, -42), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, -2), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, 8), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, 17), 10),
        lib.sprite.Hitbox(pygame.Vector2(0, 29), 5),
        lib.sprite.Hitbox(pygame.Vector2(0, 47), 5),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 128, 60, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 67853)
    ctx.hitpoint = 67853
    common.setCountdown(30 * 60 + 90, 30 * 60)
    yield 30
    common.clearBullet(ctx)
    yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    while True:
        for i in range((3, 6, 9)[lib.globals.difficultyType]):
            if i % 3 == 0:
                SFX.ENEMY_SHOOT_D.play()
            for x, y in (
                (-38, -7),
                (38, -7),
            ):
                a = common.calcDirectionAiming(ctx, x, y)
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN,
                    x=x, y=y,
                    speed=1 + i * .25,
                    angle=a + common.randomFloat(-2, 2),
                    ways=(3, 5, 7)[lib.globals.difficultyType],
                    fanSize=(100, 150, 160)[lib.globals.difficultyType],
                )
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
                    x=x, y=y,
                    speed=1 + i * .25,
                    angle=a + common.randomFloat(-2, 2),
                    ways=(4, 6, 8)[lib.globals.difficultyType],
                    fanSize=(110, 160, 170)[lib.globals.difficultyType],
                )
            yield 5
        common.moveRandom(ctx, 192, 128, 100, 80, 75, lib.utils.easeInOutCubicInterpolation)
        yield 90

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.dropPointItem(ctx, 14)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 61470)
    ctx.hitpoint = 61470
    ctx.invincibleRemain = 210
    common.setCountdown(30 * 60 + 210, 30 * 60)
    common.move(ctx, 192, 128, 150, lib.utils.easeOutCubicInterpolation)
    yield 180
    a = 0
    while True:
        SFX.ENEMY_SHOOT_C.play()
        common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIME,
            x=0, y=-4,
            speed=2,
            angle=a,
            ways=(19, 24, 29)[lib.globals.difficultyType],
        )
        a += (27, 23, 19)[lib.globals.difficultyType]
        yield (20, 15, 10)[lib.globals.difficultyType]

def escape(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.dropPointItem(ctx, 20)
    common.extendHyper(ctx)
    common.moveRelative(ctx, 0, -210, 60, lib.utils.easeInCubicInterpolation)
    common.moveRelative(ctx, 0, -200, 1, lib.utils.easeInCubicInterpolation)
    ctx.invincibleRemain = 120
    yield 60

functions = (
    setup,
    general0,
    general1,
    escape,
)