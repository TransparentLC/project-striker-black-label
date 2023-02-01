import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    common.presetEnemyD(ctx)
    ctx.hitpoint = 960
    ctx.pointItemNum = 1
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    common.setSpeed(ctx, 0)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    common.moveRelative(ctx, 0, 100, 60, lib.utils.easeOutCubicInterpolation)
    yield 60
    k = 0
    ctx.pointItemNum = 4
    while k < 50:
        if k % 5 == 0:
            SFX.ENEMY_SHOOT_D.play()
        common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_MAGENTA,
            x=0, y=0,
            speed=4,
            angle=k // (2, 2, 3)[lib.globals.difficultyType] * 13 * (-1 if mirror else 1),
            ways=(3, 4, 6)[lib.globals.difficultyType],
        )
        k += 1
        yield 5
    a = common.randomInt(0, 1)
    for _ in range(common.randomInt(1, 5)):
        ctx.angle += 7 * (1 if a else -1)
        yield 3
    common.setSpeed(ctx, 2)

functions = (
    setup,
    main,
)