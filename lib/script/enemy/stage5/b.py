import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyB(ctx)
    ctx.hitpoint = 6400
    ctx.pointItemNum = 7
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    common.setSpeed(ctx, 0)

def updateFn(ctx: lib.bullet.enemy_bullet.EnemyBullet):
    if ctx.frameCounter < 30:
        ctx.speedRadius -= .05
        common.setSpeed(ctx, ctx.speedRadius)
    elif 60 < ctx.frameCounter and ctx.frameCounter < 90:
        ctx.speedRadius += .2
        common.setSpeed(ctx, ctx.speedRadius)
    if ctx.frameCounter < 60:
        a = common.calcDirectionAiming(ctx, 0, 0)
        if a > ctx.angle + 180:
            a -= 360
        elif a < ctx.angle - 180:
            a += 360
        ctx.angle = lib.utils.clamp(a, ctx.angle - 3, ctx.angle + 3)
        ctx.rotate()

def main(ctx: lib.sprite.enemy.Enemy):
    common.moveRelative(ctx, 0, 200, 60, lib.utils.easeOutCubicInterpolation)
    yield 60
    for _ in range(3):
        for _ in range(2):
            SFX.ENEMY_SHOOT_C.play()
            for i in range((1, 2, 3)[lib.globals.difficultyType]):
                common.shootAimingMultiWay(
                    ctx,
                    bullet=BF.TYPE_ROUND_LARGE | BF.COLOR_LIME,
                    x=0, y=0,
                    speed=3 + .3 * i,
                    angle=0,
                    ways=(11, 15, 19)[lib.globals.difficultyType],
                )
            yield 30
        SFX.ENEMY_SHOOT_B.play()
        for _ in range((2, 4, 6)[lib.globals.difficultyType]):
            common.shoot(
                ctx,
                bullet=BF.TYPE_SHELL_LARGE | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=common.randomFloat(2, 2.5),
                angle=common.randomFloat(-30, 30),
                update=updateFn,
            )
            yield (12, 6, 4)[lib.globals.difficultyType]
        yield 30

    a = common.randomInt(0, 1)
    for _ in range(common.randomInt(1, 5)):
        ctx.angle += 7 * (1 if a else -1)
        yield 3
    common.setSpeed(ctx, 2)

functions = (
    setup,
    main,
)