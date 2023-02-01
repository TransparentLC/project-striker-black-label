import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    common.presetEnemyE(ctx)
    ctx.hitpoint = 500
    ctx.pointItemNum = 2
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 180 + (5 if mirror else -5)
    common.setSpeed(ctx, 2)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    yield 45
    for i in range(20):
        ctx.angle += -5 if mirror else 5
        common.setSpeed(ctx, 2)
        if i % 5 == 0 and lib.globals.difficultyType and shoot:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=0, y=0,
                speed=2, angle=0,
                ways=(0, 1, 3)[lib.globals.difficultyType],
                fanSize=60,
            )
        yield 3
    yield 60
    for i in range(20):
        ctx.angle -= -4 if mirror else 4
        common.setSpeed(ctx, 2)
        if i % 5 == 0 and lib.globals.difficultyType and shoot:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_ORANGE,
                x=0, y=0,
                speed=2, angle=0,
                ways=(0, 1, 3)[lib.globals.difficultyType],
                fanSize=60,
            )
        yield 3

functions = (
    setup,
    main,
)