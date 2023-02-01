import lib.globals

from . import common
from lib.sound import playBgm, BGM
from lib.sprite.enemy import Enemy

import lib.script.enemy.stage4.a
import lib.script.enemy.stage4.b
import lib.script.enemy.stage4.c
import lib.script.enemy.stage4.d
import lib.script.enemy.stage4.e
import lib.script.enemy.stage4.midboss
import lib.script.enemy.stage4.boss

import lib.script.stage.stage5

def stageFunction():
    common.setBackground(3)
    playBgm(BGM.STAGE4)
    lib.globals.backgroundScrollSpeed = 1.5
    lib.globals.backgroundMaskChangeSpeed = -5
    yield 60
    lib.globals.backgroundMaskChangeSpeed = 0
    yield 120

    chapter = 0

    if chapter <= 0:
        for _ in range(16):
            Enemy(lib.script.enemy.stage4.a, (42, 458, False))
            Enemy(lib.script.enemy.stage4.a, (342, 458, True))
            yield 10
        yield 180

    if chapter <= 2:
        Enemy(lib.script.enemy.stage4.b, (192, -20))
        yield 300
        Enemy(lib.script.enemy.stage4.b, (152, -20))
        Enemy(lib.script.enemy.stage4.b, (232, -20))
        yield 300
        Enemy(lib.script.enemy.stage4.b, (112, -20))
        Enemy(lib.script.enemy.stage4.b, (272, -20))
        yield 300
        Enemy(lib.script.enemy.stage4.b, (72, -20))
        Enemy(lib.script.enemy.stage4.b, (312, -20))
        yield 300
        Enemy(lib.script.enemy.stage4.b, (32, -20))
        Enemy(lib.script.enemy.stage4.b, (352, -20))
        yield 300
    yield 180

    if chapter <= 3:
        Enemy(lib.script.enemy.stage4.c, (192, -30, False))
        yield 960

    if chapter <= 4:
        for _ in range(12):
            Enemy(lib.script.enemy.stage4.a, (42, 458, False))
            Enemy(lib.script.enemy.stage4.a, (342, 458, True))
            yield 10
        yield 225
        for _ in range(12):
            Enemy(lib.script.enemy.stage4.a, (42, 458, False))
            Enemy(lib.script.enemy.stage4.a, (342, 458, True))
            yield 10
        yield 225

    if chapter <= 5:
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage4.midboss)
        yield 240
        while common.bossExists():
            yield 60
        lib.globals.backgroundScrollSpeed = 1.5
        yield 120

    if chapter <= 6:
        for i in range(6):
            Enemy(lib.script.enemy.stage4.d, (192 + 30 * (6 - i), -10 - 10 * (6 - i)))
            Enemy(lib.script.enemy.stage4.d, (192 - 30 * (6 - i), -10 - 10 * (6 - i)))
            yield 20
        yield 120
        for i in range(6):
            Enemy(lib.script.enemy.stage4.d, (192 + 30 * (i + 1), -10 - 10 * (i + 1)))
            Enemy(lib.script.enemy.stage4.d, (192 - 30 * (i + 1), -10 - 10 * (i + 1)))
            yield 20
        yield 120
        if lib.globals.groupPlayer.sprite.position.x < 192:
            for i in range(10):
                Enemy(lib.script.enemy.stage4.e, (12 + 40 * i, -10))
                yield 20
            yield 180
            for i in range(10):
                Enemy(lib.script.enemy.stage4.e, (372 - 40 * i, -10))
                yield 20
        else:
            for i in range(10):
                Enemy(lib.script.enemy.stage4.e, (372 - 40 * i, -10))
                yield 20
            yield 180
            for i in range(10):
                Enemy(lib.script.enemy.stage4.e, (12 + 40 * i, -10))
                yield 20
        yield 180

    if chapter <= 7:
        Enemy(lib.script.enemy.stage4.c, (192, -30, True))
        yield 960

    if chapter <= 8:
        for _ in range(12):
            Enemy(lib.script.enemy.stage4.a, (42, 458, False))
            Enemy(lib.script.enemy.stage4.a, (342, 458, True))
            yield 10
        yield 225

    if chapter <= 9:
        Enemy(lib.script.enemy.stage4.b, (192, -20))
        yield 120
        Enemy(lib.script.enemy.stage4.b, (192 - 155, -20))
        Enemy(lib.script.enemy.stage4.b, (192 + 155, -20))
        yield 240
        Enemy(lib.script.enemy.stage4.b, (192 - 155, -20))
        Enemy(lib.script.enemy.stage4.b, (192 + 155, -20))
        yield 120
        Enemy(lib.script.enemy.stage4.b, (192, -20))
        yield 540

    if chapter <= 10:
        yield common.bossWarning()
        playBgm(BGM.BOSS1)
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage4.boss)
        yield 240
        while common.bossExists():
            yield 60
    yield 360

    lib.globals.backgroundMaskChangeSpeed = 5
    yield 60
    lib.globals.stageFunctionWait = 0
    lib.globals.stageFunction = lib.script.stage.stage5.stageFunction()