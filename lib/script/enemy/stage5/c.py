import lib.bullet.enemy_bullet
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
    ctx.pointItemNum = 10
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0

def main(ctx: lib.sprite.enemy.Enemy):
    common.moveRelative(ctx, 0, 100, 60, lib.utils.easeOutCubicInterpolation)
    yield 90
    for _ in range(5):
        SFX.ENEMY_SHOOT_C.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_MAGENTA,
            x=0, y=0,
            speed=2.5,
            angle=0,
            ways=(11, 17, 23)[lib.globals.difficultyType],
        )
        for _ in range((5, 9, 13)[lib.globals.difficultyType]):
            common.shootAiming(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=common.randomFloat(2.75, 5.5),
                angle=common.randomFloat(-5, 5),
            )
        yield 90
    yield 30
    common.moveRelative(ctx, 0, -200, 120, lib.utils.easeOutCubicInterpolation)

functions = (
    setup,
    main,
)