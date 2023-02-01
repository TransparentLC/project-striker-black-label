import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyD(ctx)
    ctx.hitpoint = 270
    ctx.pointItemNum = 3
    ctx.invincibleRemain = 25
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    common.setSpeed(ctx, 0)

def main(ctx: lib.sprite.enemy.Enemy):
    common.moveRelative(ctx, 0, 100, 45, lib.utils.easeOutCubicInterpolation)
    yield 45
    SFX.ENEMY_SHOOT_B.play()
    common.shootComplex(
        ctx,
        bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_CYAN,
        x=0, y=0,
        speed=1,
        angle=180,
        ways=1,
        speedAddition=(.4, .25, .2)[lib.globals.difficultyType],
        layers=(3, 5, 7)[lib.globals.difficultyType],
    )
    yield 30
    common.moveRelative(ctx, 0, -250, 120, lib.utils.easeOutCubicInterpolation)

functions = (
    setup,
    main,
)