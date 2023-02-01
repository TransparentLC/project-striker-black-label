import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, dropItem = ctx.args
    common.presetEnemyA(ctx)
    ctx.hitpoint = 14400
    ctx.pointItemNum = 12
    ctx.invincibleRemain = 75
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0

def mainb0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter % 40 == 0:
        for b in common.shootMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_TINY | BF.COLOR_ORANGE,
            x=0, y=0,
            speed=.5,
            angle=ctx.angle + 180,
            ways=2,
            fanSize=120,
        ):
            b.update()

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, dropItem = ctx.args
    common.moveRelative(ctx, 0, 120, 75, lib.utils.easeOutCubicInterpolation)
    yield 75
    for _ in range(6):
        SFX.ENEMY_SHOOT_B.play()
        common.shootAimingMultiWay(
            ctx,
            bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIGHT_ORANGE,
            x=0, y=0,
            speed=1.75,
            angle=0,
            ways=(3, 5, 7)[lib.globals.difficultyType],
            update=mainb0,
        )
        yield 120
    common.moveRelative(ctx, 0, -120, 75, lib.utils.easeOutCubicInterpolation)
    yield 75
    common.moveRelative(ctx, 0, -200, 1, lib.utils.easeOutCubicInterpolation)
    yield 1

def death(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, dropItem = ctx.args
    if dropItem:
        common.extendHyper(ctx)

functions = (
    setup,
    main,
)