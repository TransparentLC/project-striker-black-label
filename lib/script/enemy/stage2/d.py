import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyA(ctx)
    ctx.hitpoint = 10800
    ctx.pointItemNum = 12
    ctx.position.update(spawnX, spawnY)
    ctx.invincibleRemain = 120
    common.moveRelative(ctx, 0, 100, 60, lib.utils.easeOutCubicInterpolation)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    a = 12 if common.randomInt(0, 1) else -12
    for i in range(96):
        if i % 3 == 0:
            SFX.ENEMY_SHOOT_D.play()
        for j in (-1, 1):
            common.shoot(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
                x=0, y=0,
                speed=4,
                angle=i * j * (15, 11, 7)[lib.globals.difficultyType],
            )
            if i % 3 == 0:
                common.shootMultiWay(
                    ctx,
                    bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
                    x=0, y=0,
                    speed=3,
                    angle=(i + 6) * j * (15, 11, 7)[lib.globals.difficultyType],
                    ways=(2, 3, 4)[lib.globals.difficultyType],
                    fanSize=40,
                )
        yield 4
    for _ in range(10):
        ctx.angle += a
        common.setSpeed(ctx, .5)
        yield 3
    common.setSpeed(ctx, 1.5)

functions = (
    setup,
    main,
)