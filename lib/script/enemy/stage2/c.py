import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyC(ctx)
    ctx.hitpoint = 1280
    ctx.pointItemNum = 5
    ctx.position.update(spawnX, spawnY)
    ctx.invincibleRemain = 120
    common.moveRelative(ctx, 0, 150, 90, lib.utils.easeOutCubicInterpolation)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    for i in range(3):
        yield 120
        SFX.ENEMY_SHOOT_C.play()
        common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_GREEN,
            x=0, y=0,
            speed=2, angle=180,
            ways=common.randomInt(
                (4, 6, 8)[lib.globals.difficultyType],
                (5, 7, 9)[lib.globals.difficultyType],
            ),
            fanSize=0,
            update=common.bulletChangeSpeed((
                (15, -1),
                (20, -.5),
                (25, -.5),
                (50, -.5),
            )),
        )
    a = common.randomInt(0, 1)
    for _ in range(10):
        ctx.angle += 3 if a else -3
        common.setSpeed(ctx, .5)
        yield 3

def death(ctx: lib.sprite.enemy.Enemy):
    common.shootMultiWay(
        ctx,
        bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_GREEN,
        x=0, y=0,
        speed=3, angle=180,
        ways=common.randomInt(
            (4, 6, 8)[lib.globals.difficultyType],
            (5, 7, 9)[lib.globals.difficultyType],
        ),
        fanSize=0,
    )
    common.shootMultiWay(
        ctx,
        bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_GREEN,
        x=0, y=0,
        speed=2, angle=180,
        ways=common.randomInt(
            (8, 14, 20)[lib.globals.difficultyType],
            (9, 15, 21)[lib.globals.difficultyType],
        ),
        fanSize=0,
        update=common.bulletChangeSpeed((
            (15, -1),
            (20, -.5),
            (25, -.5),
            (50, -.5),
        )),
    )

functions = (
    setup,
    main,
)