import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, shoot = ctx.args
    common.presetEnemyE(ctx)
    ctx.hitpoint = 500
    ctx.pointItemNum = 1
    ctx.position.update(spawnX, spawnY)
    ctx.angle = common.randomFloat(170, 190)
    common.setSpeed(ctx, 2.5)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, shoot = ctx.args
    for _ in range(2):
        yield common.randomInt(20, 40)
        if lib.globals.difficultyType and shoot:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_MAGENTA,
                x=0, y=0,
                speed=2, angle=0,
                ways=(0, 1, 3)[lib.globals.difficultyType],
                fanSize=60,
            )
    for _ in range(10):
        ctx.angle += -4 if ctx.angle < 180 else 4
        common.setSpeed(ctx, 2.5)
        yield 3
    if lib.globals.difficultyType and shoot:
        SFX.ENEMY_SHOOT_A.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_SMALL | BF.COLOR_LIGHT_MAGENTA,
            x=0, y=0,
            speed=2, angle=0,
            ways=(0, 1, 3)[lib.globals.difficultyType],
            fanSize=60,
        )

functions = (
    setup,
    main,
)