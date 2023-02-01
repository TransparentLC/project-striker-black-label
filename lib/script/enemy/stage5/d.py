import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, distance, colorIndex = ctx.args
    common.presetEnemyC(ctx)
    ctx.hitpoint = 825
    ctx.pointItemNum = (2, 3, 5)[lib.globals.difficultyType]
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    ctx.invincibleRemain = 90
    common.setSpeed(ctx, 0)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, distance, colorIndex = ctx.args

    common.moveRelative(ctx, 0, distance, 90, lib.utils.easeOutCubicInterpolation)
    yield 90
    a = common.calcDirectionAiming(ctx, 0, 0)
    for i in range(7):
        SFX.ENEMY_SHOOT_A.play()
        common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | (
                BF.COLOR_LIGHT_RED,
                BF.COLOR_LIGHT_GREEN,
                BF.COLOR_LIGHT_BLUE,
                BF.COLOR_LIGHT_ORANGE,
            )[colorIndex],
            x=0, y=0,
            speed=2,
            angle=a,
            ways=2 if i else 1,
            fanSize=(9, 9, 14)[lib.globals.difficultyType] * i,
        )
        yield (30, 15, 15)[lib.globals.difficultyType]
    a = common.randomInt(0, 1)
    for _ in range(common.randomInt(13, 19)):
        ctx.angle += 9 * (1 if a else -1)
        common.setSpeed(ctx, 1)
        yield 3
    common.setSpeed(ctx, 2)

functions = (
    setup,
    main,
)