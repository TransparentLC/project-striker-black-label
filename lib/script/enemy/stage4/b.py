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
    ctx.hitpoint = 5400
    ctx.pointItemNum = 4
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    common.setSpeed(ctx, -.75)

def main(ctx: lib.sprite.enemy.Enemy):
    while True:
        if ctx.position.y < 324:
            SFX.ENEMY_SHOOT_C.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=1.25,
                angle=0,
                ways=(25, 33, 41)[lib.globals.difficultyType],
            )
        yield 90

functions = (
    setup,
    main,
)