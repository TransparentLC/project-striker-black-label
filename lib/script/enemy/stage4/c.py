import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    common.presetEnemyA(ctx)
    ctx.hitpoint = 10800
    ctx.pointItemNum = 16
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    ctx.invincibleRemain = 300

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args

    common.moveRelative(ctx, 0, 100, 60, lib.utils.easeOutCubicInterpolation)
    yield 90
    m = 1 if mirror else -1
    k = 0
    while True:
        SFX.ENEMY_SHOOT_D.play()
        for i in range(5):
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_GRAY,
                x=0, y=0,
                speed=3,
                angle=k * 37 * m + i * 72,
                ways=(2, 3, 4)[lib.globals.difficultyType],
                fanSize=50,
                radius=48,
                deflection=90 * m,
            )
        for i in range(3):
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=2,
                angle=k * -23 * m + i * 120,
                ways=(2, 4, 6)[lib.globals.difficultyType],
                fanSize=80,
                radius=24,
                deflection=-90 * m,
            )
        k += 1
        if k % 24 == 0:
            m = -m
        if ctx.frameCounter > 800:
            break
        yield 10
    yield 30
    common.moveRelative(ctx, 0, -200, 120, lib.utils.easeOutCubicInterpolation)

def death(ctx: lib.sprite.enemy.Enemy):
    common.extendHyper(ctx)

functions = (
    setup,
    main,
)