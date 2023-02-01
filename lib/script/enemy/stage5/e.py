import math

import lib.bullet.enemy_bullet
import lib.globals
import lib.script.enemy.common as common
import lib.sprite.enemy
import lib.utils

from lib.script.enemy.common import BulletFlags as BF
from lib.sound import SFX

def setup(ctx: lib.sprite.enemy.Enemy):
    spawnX, spawnY = ctx.args
    common.presetEnemyA(ctx)
    ctx.hitpoint = 32000
    ctx.pointItemNum = 20
    ctx.position.update(spawnX, spawnY)
    ctx.angle = 0
    ctx.invincibleRemain = 180

def main(ctx: lib.sprite.enemy.Enemy):
    common.moveRelative(ctx, 0, 150, 60, lib.utils.easeOutCubicInterpolation)
    yield 60
    yield common.charge(ctx.position)
    for i in range(144):
        SFX.ENEMY_SHOOT_A.play()
        a = i * 11
        b = a / 180 * math.pi
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_RED,
            x=math.sin(b) * 30, y=-math.cos(b) * 30,
            speed=1.5,
            angle=-a - 90,
            ways=6 if lib.globals.groupPlayer.sprite.hyperRemain else (2, 3, 4)[lib.globals.difficultyType],
            fanSize=150,
            radius=30,
        )
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_RED,
            x=math.sin(b) * 30, y=-math.cos(b) * 30,
            speed=2.5,
            angle=-a - 90,
            ways=7 if lib.globals.groupPlayer.sprite.hyperRemain else (3, 4, 5)[lib.globals.difficultyType],
            fanSize=150,
            radius=30,
        )
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_ORANGE,
            x=math.sin(b + math.pi) * 30, y=-math.cos(b + math.pi) * 30,
            speed=1.5,
            angle=-a + 90,
            ways=6 if lib.globals.groupPlayer.sprite.hyperRemain else (2, 3, 4)[lib.globals.difficultyType],
            fanSize=150,
            radius=30,
        )
        common.shootComplex(
            ctx,
            bullet=BF.TYPE_SHELL_SMALL | BF.COLOR_LIGHT_ORANGE,
            x=math.sin(b + math.pi) * 30, y=-math.cos(b + math.pi) * 30,
            speed=2.5,
            angle=-a + 90,
            ways=7 if lib.globals.groupPlayer.sprite.hyperRemain else (3, 4, 5)[lib.globals.difficultyType],
            fanSize=150,
            radius=30,
        )
        yield 5
    yield 30
    ctx.invincibleRemain = 360
    common.extendHyper(ctx)
    common.moveRelative(ctx, 0, -300, 180, lib.utils.easeOutCubicInterpolation)

def death(ctx: lib.sprite.enemy.Enemy):
    if lib.globals.difficultyType == 2:
        common.extendLife(ctx)
    else:
        common.extendHyper(ctx)
        common.extendHyper(ctx)

functions = (
    setup,
    main,
)