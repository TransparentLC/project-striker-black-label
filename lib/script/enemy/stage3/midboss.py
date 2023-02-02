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
    ctx.textures = common.EnemyTextures.BOSS_C_NORMAL
    ctx.interval = 1
    ctx.hitbox = (
        lib.sprite.Hitbox(pygame.Vector2(-8, -18), 12),
        lib.sprite.Hitbox(pygame.Vector2(-23, -19), 13),
        lib.sprite.Hitbox(pygame.Vector2(-24, -3), 7),
        lib.sprite.Hitbox(pygame.Vector2(-24, -36), 6),
        lib.sprite.Hitbox(pygame.Vector2(-24, -44), 4),
        lib.sprite.Hitbox(pygame.Vector2(-40, -19), 8),
        lib.sprite.Hitbox(pygame.Vector2(-51, -19), 8),
        lib.sprite.Hitbox(pygame.Vector2(-59, -19), 7),
        lib.sprite.Hitbox(pygame.Vector2(-67, -19), 5),
        lib.sprite.Hitbox(pygame.Vector2(-36, 37), 5),
        lib.sprite.Hitbox(pygame.Vector2(-28, 37), 6),
        lib.sprite.Hitbox(pygame.Vector2(-17, 36), 7),
        lib.sprite.Hitbox(pygame.Vector2(-6, 36), 8),
        lib.sprite.Hitbox(pygame.Vector2(8, -18), 12),
        lib.sprite.Hitbox(pygame.Vector2(23, -19), 13),
        lib.sprite.Hitbox(pygame.Vector2(24, -3), 7),
        lib.sprite.Hitbox(pygame.Vector2(24, -36), 6),
        lib.sprite.Hitbox(pygame.Vector2(24, -44), 4),
        lib.sprite.Hitbox(pygame.Vector2(40, -19), 8),
        lib.sprite.Hitbox(pygame.Vector2(51, -19), 8),
        lib.sprite.Hitbox(pygame.Vector2(59, -19), 7),
        lib.sprite.Hitbox(pygame.Vector2(67, -19), 5),
        lib.sprite.Hitbox(pygame.Vector2(36, 37), 5),
        lib.sprite.Hitbox(pygame.Vector2(28, 37), 6),
        lib.sprite.Hitbox(pygame.Vector2(17, 36), 7),
        lib.sprite.Hitbox(pygame.Vector2(6, 36), 8),
        lib.sprite.Hitbox(pygame.Vector2(0, -35), 7),
        lib.sprite.Hitbox(pygame.Vector2(0, -44), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, 2), 11),
        lib.sprite.Hitbox(pygame.Vector2(0, 16), 6),
        lib.sprite.Hitbox(pygame.Vector2(0, 25), 5),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 128, 180, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 98201)
    ctx.hitpoint = 98201
    common.setCountdown(40 * 60 + 180, 40 * 60)
    yield 180

def general0(ctx: lib.sprite.enemy.Enemy):
    k = 1
    while True:
        yield common.charge(ctx.position + pygame.Vector2(0, 4))
        for i in range(30):
            if i % 3 == 0:
                SFX.ENEMY_SHOOT_D.play()
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | (BF.COLOR_LIGHT_ORANGE if k == 1 else BF.COLOR_LIGHT_RED),
                x=0, y=4,
                speed=3,
                angle=k * (60 + 10 * i),
                ways=(3, 5, 7)[lib.globals.difficultyType],
                fanSize=(18, 36, 54)[lib.globals.difficultyType],
                update=common.bulletChangeSpeed((
                    (15, -2.5),
                    (105, .5),
                    (120, .5),
                    (135, .5),
                    (150, .5),
                )),
            )
            yield 3
        for _ in range(5):
            SFX.ENEMY_SHOOT_C.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GRAY,
                x=0, y=-4,
                speed=1.5,
                angle=0,
                ways=(25, 35, 45)[lib.globals.difficultyType],
                update=common.bulletChangeSpeed((
                    (60, -.25),
                    (120, -.25),
                )),
            )
            yield 30
        k = -k
        common.moveRandom(ctx, 192, 128, 120, 64, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setPhaseName(6)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint) / (60 * 60 + 90) * .9),
    )
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 134967)
    ctx.hitpoint = 134967
    ctx.invincibleRemain = 90 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(60 * 60 + 90, 60 * 60)
    common.moveRandom(ctx, 192, 96, 120, 32, 90, lib.utils.easeOutCubicInterpolation)
    yield 90
    while True:
        yield common.charge(ctx.position + pygame.Vector2(0, 4))
        for i in range(70):
            if i % 10 == 0:
                SFX.ENEMY_SHOOT_C.play()
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_ROUND_TINY | BF.COLOR_LIGHT_RED,
                    x=0, y=-4,
                    speed=3,
                    angle=0,
                    ways=(17, 25, 33)[lib.globals.difficultyType],
                )
            if i % 3 == 0:
                SFX.ENEMY_SHOOT_B.play()
                for x in (-29, 29):
                    for _ in range((1, 2, 4)[lib.globals.difficultyType]):
                        common.shootAiming(
                            ctx,
                            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_ORANGE,
                            x=x, y=-2,
                            speed=common.randomFloat(1, 2),
                            angle=common.randomInt(-120, 120) * (1, 1, 1.5)[lib.globals.difficultyType],
                            update=common.bulletChangeSpeed((
                                (15, 1),
                                (30, 1),
                                (45, 1),
                                (60, 1),
                            )),
                        )
            yield 3
        common.moveRandom(ctx, 192, 96, 120, 32, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def escape(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.extendLife(ctx)
    common.moveRelative(ctx, 0, -210, 60, lib.utils.easeInCubicInterpolation)
    common.moveRelative(ctx, 0, -200, 1, lib.utils.easeInCubicInterpolation)
    ctx.invincibleRemain = 120
    yield 60

functions = (
    setup,
    general0,
    phase0,
    escape,
)