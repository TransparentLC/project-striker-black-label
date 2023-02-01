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
    ctx.hitpoint = 480
    ctx.pointItemNum = 4
    ctx.invincibleRemain = 45
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    common.setSpeed(ctx, 0)

def main(ctx: lib.sprite.enemy.Enemy):
    common.moveRelative(ctx, 0, 100, 45, lib.utils.easeOutCubicInterpolation)
    yield 60
    SFX.ENEMY_SHOOT_D.play()
    common.shootComplex(
        ctx,
        bullet=BF.TYPE_SHELL_DUAL | BF.COLOR_LIME,
        x=0, y=0,
        speed=2.5,
        angle=0,
        fanSize=120,
        ways=(3, 5, 5)[lib.globals.difficultyType],
        speedAddition=1,
        layers=(3, 3, 5)[lib.globals.difficultyType],
        aiming=True,
    )
    yield 60
    common.moveRelative(ctx, 0, -250, 120, lib.utils.easeOutCubicInterpolation)

functions = (
    setup,
    main,
)