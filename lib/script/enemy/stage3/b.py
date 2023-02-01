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
    ctx.hitpoint = 540
    ctx.pointItemNum = 2
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 180
    common.setSpeed(ctx, .5)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    k = 0
    while True:
        if k > 12 and k < 72:
            ctx.angle += 1 if mirror else -1
            common.setSpeed(ctx, .5)
        elif k == 72:
            common.setSpeed(ctx, 1)
        if k < 48 and k % 12 == 6:
            SFX.ENEMY_SHOOT_B.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
                x=0, y=0,
                speed=1,
                ways=(5, 7, 9)[lib.globals.difficultyType],
                fanSize=120,
                angle=0,
            )
        k += 1
        yield 5

functions = (
    setup,
    main,
)