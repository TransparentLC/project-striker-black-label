import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    common.presetEnemyB(ctx)
    ctx.hitpoint = 3200
    ctx.pointItemNum = 6
    ctx.position.update(spawnX, spawnY)
    ctx.invincibleRemain = 60
    common.moveRelative(ctx, 0, 100, 90, lib.utils.easeOutCubicInterpolation)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror = ctx.args
    yield 60
    for i in range(20):
        if i % 2 == 0:
            SFX.ENEMY_SHOOT_D.play()
        for i in range((1, 2, 3)[lib.globals.difficultyType]):
            common.shootAiming(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_MAGENTA,
                x=0, y=0,
                speed=common.randomFloat(6, 8),
                angle=common.randomFloat(-20, 20),
                update=common.bulletChangeSpeed((
                    (10, -5),
                ))
            )
        yield 10
    for _ in range(10):
        ctx.angle += 12 if mirror else -12
        common.setSpeed(ctx, .5)
        yield 3
    common.setSpeed(ctx, 1.5)

functions = (
    setup,
    main,
)