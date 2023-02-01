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
    ctx.hitpoint = 480
    ctx.pointItemNum = 2
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 180 + (60 if mirror else -60)
    common.setSpeed(ctx, 2)

def mainb0(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter == 60:
        ctx.angle = common.calcDirectionAiming(ctx, 0, 0)
        ctx.updateCustom = common.bulletChangeSpeed((
            (90, .5),
            (105, .75),
            (120, 1),
            (135, 1.25),
            (150, 1.5),
        ))

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    k = 0
    while True:
        ctx.angle += 1.5 if mirror else -1.5
        common.setSpeed(ctx, 2)
        if (k + 1) % (7, 6, 5)[lib.globals.difficultyType] == 0:
            SFX.ENEMY_SHOOT_A.play()
            common.shootAimingMultiWay(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_ORANGE,
                x=0, y=0,
                speed=.25,
                ways=(1, 2, 3)[lib.globals.difficultyType],
                fanSize=120,
                angle=0,
                update=mainb0,
            )
        k += 1
        yield 5

functions = (
    setup,
    main,
)