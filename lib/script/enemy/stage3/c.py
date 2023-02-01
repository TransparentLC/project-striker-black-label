import lib.bullet.enemy_bullet
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
    ctx.pointItemNum = 6
    ctx.invincibleRemain = 150
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.moveRelative(ctx, 0, 120, 75, lib.utils.easeOutCubicInterpolation)
    yield 75
    for _ in range(20):
        SFX.ENEMY_SHOOT_B.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_ORANGE,
            x=0, y=0,
            speed=1,
            angle=0,
            ways=(7, 9, 11)[lib.globals.difficultyType],
            fanSize=120,
            update=common.bulletChangeSpeed((
                (15, 1.25),
                (30, 1.5),
                (45, 1.75),
            ))
        )
        yield 30
    common.moveRelative(ctx, 0, -120, 75, lib.utils.easeOutCubicInterpolation)
    yield 75
    common.moveRelative(ctx, 0, -200, 1, lib.utils.easeOutCubicInterpolation)
    yield 1

functions = (
    setup,
    main,
)