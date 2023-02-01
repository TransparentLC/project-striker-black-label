import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    common.presetEnemyE(ctx)
    ctx.hitpoint = 640
    ctx.pointItemNum = 3
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 180 + (60 if mirror else -60)
    ctx.invincibleRemain = 75
    common.setSpeed(ctx, 2)

def main(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY, mirror, shoot = ctx.args
    yield common.randomInt(40, 80)
    common.setSpeed(ctx, 1)
    yield 15
    common.setSpeed(ctx, 0)
    for _ in range(10):
        ctx.angle += 12 if mirror else -12
        yield 3
    for _ in range(3):
        if shoot:
            SFX.ENEMY_SHOOT_B.play()
            common.shootComplex(
                ctx,
                bullet=BF.TYPE_ROUND_MEDIUM | BF.COLOR_LIGHT_CYAN,
                x=0, y=0,
                speed=6, angle=0,
                ways=(1, 3, 5)[lib.globals.difficultyType],
                fanSize=(1, 80, 140)[lib.globals.difficultyType],
                speedAddition=.75, layers=(1, 1, 2)[lib.globals.difficultyType],
                aiming=True,
                update=common.bulletChangeSpeed((
                    (15, -5),
                )),
            )
        yield 30
    for _ in range(5):
        ctx.angle += -6 if mirror else 6
        common.setSpeed(ctx, 2)
        yield 3

functions = (
    setup,
    main,
)