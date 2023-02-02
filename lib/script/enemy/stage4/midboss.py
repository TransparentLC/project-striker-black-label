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
    ctx.textures = common.EnemyTextures.BOSS_D_NORMAL
    ctx.interval = 1
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
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 128, 180, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 106532)
    ctx.hitpoint = 106532
    common.setCountdown(40 * 60 + 150, 40 * 60)
    yield 180

def general0(ctx: lib.sprite.enemy.Enemy):
    k = 1
    while True:
        for i in range(20):
            SFX.ENEMY_SHOOT_B.play()
            v = pygame.Vector2(0, (i + 1) * 10).rotate(i * 20 * k)
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | (BF.COLOR_LIME if k == 1 else BF.COLOR_LIGHT_CYAN),
                x=v.x, y=-25 + v.y,
                speed=1.25,
                angle=0,
                ways=(9, 17, 25)[lib.globals.difficultyType],
            )
            yield 5
        k = -k
        common.moveRandom(ctx, 192, 96, 192, 64, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < 0 or ctx.position.x > 384 or ctx.position.y < 0 or ctx.position.y > 448:
        SFX.ENEMY_SHOOT_E.play()
        for b in common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_GRAY,
            x=0, y=0,
            speed=1,
            angle=0,
            ways=(21, 27, 33)[lib.globals.difficultyType],
        ):
            b.update()
        ctx.explode()

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setPhaseName(10)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 4) * lib.globals.maxGetPoint) / (60 * 60 + 90) * .9),
    )
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 120413)
    ctx.hitpoint = 120413
    ctx.invincibleRemain = 90 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(60 * 60 + 90, 60 * 60)
    common.moveRandom(ctx, 192, 96, 120, 32, 90, lib.utils.easeOutCubicInterpolation)
    yield 90
    while True:
        d = (
            pygame.Vector2(0, 0),
            pygame.Vector2(0, 448),
            pygame.Vector2(384, 0),
            pygame.Vector2(384, 448),
        )
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIGHT_CYAN,
            x=0, y=-25,
            speed=1,
            angle=0,
            ways=(21, 27, 33)[lib.globals.difficultyType],
        )
        for i in range(7):
            SFX.ENEMY_SHOOT_B.play()
            for v in d:
                common.shoot(
                    ctx,
                    bullet=(BF.TYPE_SHELL_SMALL if i else BF.TYPE_SHELL_LARGE) | BF.COLOR_LIGHT_CYAN,
                    x=0, y=-25,
                    speed=(ctx.position - v).length() / 90,
                    angle=common.calcDirection(ctx.position + pygame.Vector2(0, -25), v),
                    update=(None if i else phase0b0),
                )
            yield 3
        yield 90
        common.moveRandom(ctx, 192, 96, 120, 32, 90, lib.utils.easeOutCubicInterpolation)
        yield 90

def escape(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 36)
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