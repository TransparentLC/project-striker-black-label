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
    ctx.textures = common.EnemyTextures.BOSS_B_NORMAL
    ctx.interval = 1
    ctx.explosion = explosion.ExplosionPlaneLarge
    ctx.explodeSfx = SFX.EXPLODE_ENEMY_D
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
    ctx.debris = (
        (debris.DebrisB, pygame.Vector2(-16, 39), .125, 2, 1, 5, 2),
        (debris.DebrisB, pygame.Vector2(16, 39), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-34, 40), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(34, 40), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, 28), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(0, -16), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(0, -36), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(-26, -16), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(-56, -16), .125, 2, 1, 5, 2),
        (debris.DebrisA, pygame.Vector2(26, -16), .125, 2, 1, 5, 3),
        (debris.DebrisB, pygame.Vector2(56, -16), .125, 2, 1, 5, 2),
    )
    ctx.invincibleRemain = 150
    ctx.position.update(192, -64)
    common.move(ctx, 192, 96, 120, lib.utils.easeOutCubicInterpolation)
    common.setBoss(ctx)
    common.setBossRemain(4)
    common.setBossHPRange(ctx, 10000, 62756)
    common.setPhaseName(0)
    common.setCountdown(30 * 60 + 120, 30 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60

def general0(ctx: lib.sprite.enemy.Enemy):
    while True:
        for i in range(4):
            for j in range(8):
                if j % 2 == 0:
                    SFX.ENEMY_SHOOT_D.play()
                for k in (-1, 1):
                    common.shootComplex(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | (BF.COLOR_CYAN if i % 2 == 0 else BF.COLOR_LIGHT_BLUE),
                        x=k * 38, y=-15,
                        speed=2.5,
                        angle=180 + k * 20 + (j - 3) * (1 if i % 2 == 0 else -1) * (2, 2, 3)[lib.globals.difficultyType],
                        ways=(10, 14, 20)[lib.globals.difficultyType],
                        fanSize=(205, 235, 270)[lib.globals.difficultyType],
                        radius=8,
                    )
                yield 7
            yield 20
        common.moveRandom(ctx, 192, 96, 120, 48, 60, lib.utils.easeInOutCubicInterpolation)
        yield 60

def phase0b0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.position.x < 0 or ctx.position.x > 384 or ctx.position.y < 0 or ctx.position.y > 448:
        bf = (
            (BF.COLOR_LIGHT_RED, BF.COLOR_RED),
            (BF.COLOR_LIGHT_MAGENTA, BF.COLOR_MAGENTA),
            (BF.COLOR_LIGHT_CYAN, BF.COLOR_CYAN),
            (BF.COLOR_LIGHT_ORANGE, BF.COLOR_ORANGE),
        )[common.randomInt(0, 3)]
        SFX.ENEMY_SHOOT_C.play()
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_MEDIUM | bf[0],
            x=0, y=0,
            speed=.75,
            angle=ctx.angle,
            ways=(4, 6, 8)[lib.globals.difficultyType],
        ):
            b.update()
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | bf[1],
            x=0, y=0,
            speed=1.25,
            angle=ctx.angle + (45, 30, 22.5)[lib.globals.difficultyType],
            ways=(4, 6, 8)[lib.globals.difficultyType],
        ):
            b.update()
        ctx.explode()

def phase0(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(3)
    common.setBossHPRange(ctx, 10000, 110358)
    common.setPhaseName(3)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint) / (45 * 60 + 120) * .9),
    )
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(45 * 60 + 120, 45 * 60)
    common.move(ctx, 192, 128, 120, lib.utils.easeInOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60
    a = -1
    while True:
        for i in range(7):
            SFX.ENEMY_SHOOT_B.play()
            common.shoot(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_ORANGE,
                x=0, y=-4,
                speed=3,
                angle=180 + (i - 3) * a * 25 + common.randomFloat(-10, 10),
                update=phase0b0,
            )
            yield 10
        yield 120
        common.moveRandom(ctx, 192, 96, 96, 48, 60, lib.utils.easeInOutCubicInterpolation)
        yield 60
        a = -a

def general1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 24)
    common.moveClear(ctx)
    common.setBossRemain(2)
    common.setBossHPRange(ctx, 10000, 68152)
    common.setPhaseName(0)
    ctx.invincibleRemain = 60
    common.setCountdown(30 * 60 + 60, 30 * 60)
    common.move(ctx, 192, 96, 60, lib.utils.easeOutCubicInterpolation)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 120
    m = 0
    n = 0
    while True:
        SFX.ENEMY_SHOOT_D.play()
        for x, y, a in (
            (-8, 23, 270),
            (-38, -15, 180),
            (38, -15, 90),
            (8, 23, 0),
        ):
            common.shootMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | (BF.COLOR_CYAN if n % 2 == 0 else BF.COLOR_LIGHT_CYAN),
                x=x, y=y,
                speed=3,
                angle=a + m,
                ways=(1, 3, 5)[lib.globals.difficultyType],
                fanSize=(0, 15, 25)[lib.globals.difficultyType],
            )
        m += 11
        n += 1
        yield 8

def phase1(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.setBossRemain(0)
    common.setBossHPRange(ctx, 10000, 101653)
    common.setPhaseName(4)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint) / (45 * 60 + 90) * .9),
    )
    ctx.invincibleRemain = 90 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(45 * 60 + 90, 45 * 60)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 30
    k = 1
    while True:
        for i in range(45):
            SFX.ENEMY_SHOOT_A.play()
            for a in range(0, 360, (120, 90, 60)[lib.globals.difficultyType]):
                common.shootComplex(
                    ctx,
                    bullet=BF.TYPE_SHELL_DUAL | (BF.COLOR_GREEN if i % 2 == 0 else BF.COLOR_LIME),
                    x=0, y=-4,
                    speed=2.5,
                    angle=a + i * 21 * k,
                    ways=(2, 3, 3)[lib.globals.difficultyType],
                    fanSize=30,
                    radius=-((i / 45) ** 2) * 60 + 60,
                )
            yield 5
        k = -k
        yield 30
        common.moveRandom(ctx, 192, 96, 150, 96, 60, lib.utils.easeOutCubicInterpolation)
        yield 60

def phase2(ctx: lib.sprite.enemy.Enemy):
    ctx.textures = common.EnemyTextures.BOSS_B_BREAK
    common.setCountdown()
    common.clearBullet(ctx)
    common.moveClear(ctx)
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 26)
    common.setPhaseName(0)
    common.setBossRemain(0)
    ctx.invincibleRemain = 120 + lib.globals.groupPlayer.sprite.hyperRemain
    common.setCountdown(45 * 60 + 120, 45 * 60)
    common.setBossHPRange(ctx, 0, 118274)
    for i in range(60):
        ctx.hitpoint = round(lib.utils.linearInterpolation((i + 1) / 60, max(lib.globals.bossHitpointRangeMin, 1), lib.globals.bossHitpointRangeMax))
        yield 1
    yield 60
    common.setPhaseName(5)
    common.setPhaseBonus(
        (20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint,
        round(((20 + (2, 3, 4)[lib.globals.difficultyType] * 2) * lib.globals.maxGetPoint) / (45 * 60 + 120) * .9),
    )
    while True:
        common.moveRandom(ctx, 192, 96, 96, 96, 60, lib.utils.easeOutCubicInterpolation)
        yield 60
        for i in range(4):
            for j in range(6):
                SFX.ENEMY_SHOOT_D.play()
                for k in (-1, 1):
                    common.shootComplex(
                        ctx,
                        bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIME,
                        x=k * 38, y=-15,
                        speed=2,
                        angle=180 + k * 20 + (j - 3) * (1 if i % 2 == 0 else -1) * 2,
                        ways=(6, 10, 14)[lib.globals.difficultyType],
                        fanSize=(160, 210, 270)[lib.globals.difficultyType],
                        radius=8,
                    )
                if i >= 2 and j % 2 == 0:
                    SFX.ENEMY_SHOOT_C.play()
                    if j == 2:
                        common.shootAimingMultiWay(
                            ctx,
                            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_MAGENTA,
                            x=0, y=-4,
                            speed=3,
                            angle=0,
                            ways=(4, 6, 10)[lib.globals.difficultyType],
                            fanSize=(67.5, 87.5, 108)[lib.globals.difficultyType],
                        )
                    else:
                        common.shootAimingMultiWay(
                            ctx,
                            bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_MAGENTA,
                            x=0, y=-4,
                            speed=3,
                            angle=0,
                            ways=(5, 7, 11)[lib.globals.difficultyType],
                            fanSize=(90, 105, 120)[lib.globals.difficultyType],
                        )
                yield 10
            yield 20

def death(ctx: lib.sprite.enemy.Enemy):
    common.setCountdown()
    common.bonusBullet(ctx)
    common.bonusPhase()
    common.dropPointItem(ctx, 28)

functions = (
    setup,
    general0,
    phase0,
    general1,
    phase1,
    phase2,
)