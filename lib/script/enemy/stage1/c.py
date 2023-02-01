import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyC(ctx)
    ctx.hitpoint = 1200
    ctx.invincibleRemain = 120
    ctx.pointItemNum = 4
    ctx.position.update(spawnX, spawnY)
    common.moveRandom(ctx, spawnX, spawnY + 100, 60, 60, 120, lib.utils.easeOutCubicInterpolation)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    yield 120
    for _ in range(3):
        yield 60
        SFX.ENEMY_SHOOT_B.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_MAGENTA,
            x=0, y=0,
            speed=5, angle=0,
            ways=(3, 7, 11)[lib.globals.difficultyType],
            fanSize=120,
            update=common.bulletChangeSpeed((
                (10, -3.75),
            )),
        )
    a = common.randomFloat(-30, 30)
    for _ in range(6):
        ctx.angle += a / 6
        yield 5
    common.setSpeed(ctx, 2)

functions = (
    setup,
    main,
)