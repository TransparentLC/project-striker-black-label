import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    common.presetEnemyD(ctx)
    ctx.hitpoint = 500
    ctx.pointItemNum = 2
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 180
    common.setSpeed(ctx, 2)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    for _ in range(3):
        yield 30
        if lib.globals.difficultyType:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=0, y=0,
                speed=3, angle=0,
                ways=(0, 1, 3)[lib.globals.difficultyType],
                fanSize=80,
            )
    yield 30
    for _ in range(20):
        ctx.angle -= -3 if mirror else 3
        common.setSpeed(ctx, 2)
        yield 3

functions = (
    setup,
    main,
)