import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    common.presetEnemyE(ctx)
    ctx.hitpoint = 320
    ctx.pointItemNum = 1
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 10 if mirror else -10
    common.setSpeed(ctx, 5)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    k = 0
    while True:
        if 8 <= k and k <= 16:
            ctx.angle += 7 if mirror else -7
            common.setSpeed(ctx, 4)
        if 8 <= k and 16 <= k and k % 2 == 0:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_CYAN,
                x=0, y=0,
                speed=(4.5, 6, 7.5)[lib.globals.difficultyType],
                angle=0,
                ways=1,
                fanSize=60,
            )
        k += 1
        yield 5

functions = (
    setup,
    main,
)