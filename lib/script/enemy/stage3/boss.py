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
    ctx.textures = common.EnemyTextures.BOSS_C_NORMAL
    ctx.interval = 1
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
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
    ctx.debris = (
        (debris.DebrisB, pygame.Vector2(-67, 19), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(67, 19), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-51, 19), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(51, 19), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-23, 19), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(23, 19), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-8, 18), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(8, 18), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-28, 37), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(28, 37), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(-17, 36), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(17, 36), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(0, 37), .125, 2, 1, 5, 3),
        (debris.DebrisA, pygame.Vector2(0, 16), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(0, 2), .125, 2, 1, 5, 4),
        (debris.DebrisA, pygame.Vector2(0, -22), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(0, -35), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -44), .125, 2, 1, 5, 2),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 96, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(5)
    common.setBossHPRange(ctx, 10000, 90758)
    common.setPhaseName(0)
    common.setCountdown(40 * 60 + 120, 40 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    while True:
        yield common.charge(ctx.position + pygame.Vector2(0, 4))
        for k in (1, -1):
            for i in range(30):
                if i % 5 == 0:
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
                        (135, 1),
                        (150, 1),
                    )),
                )
                yield 2
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
                    (360, -.25),
                    (480, -.25),
                )),
            )
            yield 30
        common.moveRandom(ctx, 192, 128, 120, 64, 60, lib.utils.easeOutCubicInterpolation)
        yield 60

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    for f, s in (
        (45, .5),
        (75, .25),
        (105, 0),
    ):
        if ctx.frameCounter == f:
            ctx.speedRadius = s
    if ctx.frameCounter == 120:
        ctx.textures = (common.BulletTextures[BF.TYPE_ROUND_MEDIUM | BF.COLOR_MAGENTA],)
        ctx.rotate()
        ctx.angle = common.calcDirectionAiming(ctx, 0, 0)
        ctx.speedRadius = 2
        ctx.updateCustom = None

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 121670)
    common.setPhaseName(7)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint) / (50 * 60 + 120) * .9),
    )
    ctx.hitpoint = 10000
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(50 * 60 + 120, 50 * 60)
    common.move(ctx, 192, 128, 120, lib.utils.easeInOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60
    while True:
        for i in range(36):
            SFX.ENEMY_SHOOT_A.play()
            for b in (-1, 1):
                if i % 2 == 0:
                    common.shoot(
                        ctx,
                        bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_ORANGE,
                        x=29 * b, y=-2,
                        speed=1,
                        angle=-25 * i * b,
                        update=phase0b0 if i % (6, 4, 3)[lib.globals.difficultyType] == 0 else None,
                    )
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                    x=29 * b, y=-2,
                    speed=2,
                    angle=15 * i * b,
                    ways=(1, 3, 5)[lib.globals.difficultyType],
                    fanSize=(1, 3, 5)[lib.globals.difficultyType],
                )
            if i % 18 == 0:
                common.moveRandom(ctx, 192, 96, 64, 32, 75, lib.utils.easeInOutCubicInterpolation)
            yield 5

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 24)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 96434)
    common.setPhaseName(0)
    ctx.invincibleRemain = 60
    common.setCountdown(40 * 60 + 60, 40 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120
    while True:
        for k in (1, -1):
            for i in range(20):
                if i % 3 == 0:
                    SFX.ENEMY_SHOOT_D.play()
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | (BF.COLOR_LIGHT_ORANGE if k == 1 else BF.COLOR_LIGHT_RED),
                    x=0, y=4,
                    speed=2.5,
                    angle=k * (60 + 15 * i),
                    ways=(3, 5, 7)[lib.globals.difficultyType],
                    fanSize=(28, 56, 84)[lib.globals.difficultyType],
                )
                if i % 10 == 0:
                    SFX.ENEMY_SHOOT_C.play()
                    common.shootAimingMultiWay(
                        ctx,
                        bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_GRAY,
                        x=0, y=-4,
                        speed=1.5,
                        angle=0,
                        ways=(13, 17, 21)[lib.globals.difficultyType],
                    )
                yield 3
        common.moveRandom(ctx, 192, 128, 120, 64, 60, lib.utils.easeOutCubicInterpolation)

def phase1b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 45:
        ctx.angle += 1
    elif ctx.frameCounter < 90:
        ctx.angle -= 8
    elif ctx.frameCounter < 120:
        ctx.angle -= 3
    elif ctx.frameCounter < 135:
        ctx.angle -= 1
    else:
        ctx.updateCustom = None
    if ctx.frameCounter % 4 == 0:
        ctx.rotate()

def phase1b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 45:
        ctx.angle -= 1
    elif ctx.frameCounter < 90:
        ctx.angle += 8
    elif ctx.frameCounter < 120:
        ctx.angle += 3
    elif ctx.frameCounter < 135:
        ctx.angle += 1
    else:
        ctx.updateCustom = None
    if ctx.frameCounter % 4 == 0:
        ctx.rotate()

def phase1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 120671)
    common.setPhaseName(8)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint) / (50 * 60 + 90) * .9),
    )
    ctx.invincibleRemain = 90 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(50 * 60 + 90, 50 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 30
    m = 1
    while True:
        a = common.calcDirectionAiming(ctx, 0, -4)
        for f, b in (
            (phase1b0, (-15, -0, -4)[lib.globals.difficultyType]),
            (phase1b1, (15, 0, 4)[lib.globals.difficultyType]),
        ):
            for i in range(12):
                if i % 2 == 0:
                    SFX.ENEMY_SHOOT_E.play()
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                    x=0, y=-4,
                    speed=3,
                    angle=a + b,
                    ways=(8, 12, 16)[lib.globals.difficultyType],
                    fanSize=0,
                    update=f,
                )
                yield 5
        for i in range(24):
            SFX.ENEMY_SHOOT_A.play()
            for k in (0, 180):
                for j in range((3, 4, 5)[lib.globals.difficultyType]):
                    common.shootMultiWay(
                        ctx,
                        bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_ORANGE,
                        x=0, y=-4,
                        speed=3 + j * .025,
                        angle=a + (k + 25 * i + j) * m,
                        ways=3,
                    )
            yield 5
        common.moveRandom(ctx, 192, 96, 150, 96, 60, lib.utils.easeOutCubicInterpolation)
        m = -m
        yield 60

def general2(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_C_BREAK
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 30)
    common.moveClear(ctx)
    common.setBossRemain(1)
    common.setBossHPRange(ctx, 10000, 91031)
    common.setPhaseName(0)
    ctx.invincibleRemain = 60
    common.setCountdown(40 * 60 + 60, 40 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120
    while True:
        for k in (1, -1):
            for i in range(15):
                SFX.ENEMY_SHOOT_D.play()
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | (BF.COLOR_LIGHT_ORANGE if k == 1 else BF.COLOR_LIGHT_RED),
                    x=0, y=4,
                    speed=3,
                    angle=k * (60 + 20 * i),
                    ways=(7, 9, 11)[lib.globals.difficultyType],
                    fanSize=(84, 120, 160)[lib.globals.difficultyType],
                )
                if i % 3 == 0:
                    SFX.ENEMY_SHOOT_C.play()
                    common.shootAimingMultiWay(
                        ctx,
                        bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_GRAY,
                        x=0, y=-4,
                        speed=1.5,
                        angle=0,
                        ways=(13, 17, 21)[lib.globals.difficultyType],
                    )
                yield 12
        common.moveRandom(ctx, 192, 128, 64, 32, 80, lib.utils.easeOutCubicInterpolation)

def phase2b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if 40 < ctx.frameCounter and ctx.frameCounter < 50:
        ctx.speedRadius -= .3
    elif ctx.frameCounter == 60:
        ctx.speedRadius = .75
        ctx.angle += 15
        ctx.rotate()
        ctx.updateCustom = None

def phase2b1(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if 40 < ctx.frameCounter and ctx.frameCounter < 50:
        ctx.speedRadius -= .3
    elif ctx.frameCounter == 60:
        ctx.speedRadius = .75
        ctx.angle -= 15
        ctx.rotate()
        ctx.updateCustom = None

def phase2(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 0, 131570)
    common.setPhaseName(9)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 3) * lib.globals.maxGetPoint) / (55 * 60 + 60) * .9),
    )
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(55 * 60 + 60, 55 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60
    k = 0
    while True:
        if k % 2 == 0:
            SFX.ENEMY_SHOOT_D.play()
        for x, y, a, b in (
            (-24, -43, 0, 1),
            (-24, 5, 135, 1),
            (24, -43, 0, -1),
            (24, 5, 135, -1),
        ):
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | (BF.COLOR_LIGHT_ORANGE if k % 2 == 0 else BF.COLOR_LIGHT_RED),
                x=x, y=y,
                speed=4,
                angle=b * (k * 11 + a),
                ways=(1, 2, 4)[lib.globals.difficultyType],
                update=(phase2b0 if k % 2 == 0 else phase2b1),
            )
        if k % 36 == 0:
            common.moveRandom(ctx, 192, 96, 150, 96, 120, lib.utils.easeOutCubicInterpolation)
        k += 1
        yield 5

def death(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 34)

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
    general2,
    phase2,
)