import lib.globals

from . import common
from lib.sound import playBgm, BGM
from lib.sprite.enemy import Enemy

import lib.script.enemy.stage3.a
import lib.script.enemy.stage3.b
import lib.script.enemy.stage3.c
import lib.script.enemy.stage3.d
import lib.script.enemy.stage3.midboss
import lib.script.enemy.stage3.boss

import lib.script.stage.stage4

def stageFunction():
    common.setBackground(2)
    playBgm(BGM.STAGE3)
    lib.globals.backgroundScrollSpeed = 1.5
    lib.globals.backgroundMaskChangeSpeed = -5
    yield 60
    lib.globals.backgroundMaskChangeSpeed = 0
    yield 180

    chapter = 0

    if chapter <= 0:
        for _ in range(7):
            Enemy(lib.script.enemy.stage3.a, (-5, common.randomInt(24, 64), True))
            Enemy(lib.script.enemy.stage3.a, (389, common.randomInt(24, 64), False))
            yield 60
        yield 180

    if chapter <= 1:
        for _ in range(8):
            Enemy(lib.script.enemy.stage3.b, (112, -10, True))
            Enemy(lib.script.enemy.stage3.b, (272, -10, False))
            yield 60
        for _ in range(4):
            Enemy(lib.script.enemy.stage3.b, (112, -10, True))
            Enemy(lib.script.enemy.stage3.b, (272, -10, False))
            Enemy(lib.script.enemy.stage3.a, (-5, common.randomInt(24, 64), True))
            Enemy(lib.script.enemy.stage3.a, (389, common.randomInt(24, 64), False))
            yield 60
        for _ in range(4):
            Enemy(lib.script.enemy.stage3.a, (-5, common.randomInt(24, 64), True))
            Enemy(lib.script.enemy.stage3.a, (389, common.randomInt(24, 64), False))
            yield 60
        yield 150

    if chapter <= 2:
        for _ in range(6):
            Enemy(lib.script.enemy.stage3.b, (52, -10, True))
            Enemy(lib.script.enemy.stage3.b, (132, -10, True))
            Enemy(lib.script.enemy.stage3.b, (252, -10, False))
            Enemy(lib.script.enemy.stage3.b, (332, -10, False))
            yield 60
        yield 540

    if chapter <= 3:
        Enemy(lib.script.enemy.stage3.c, (152, -10))
        Enemy(lib.script.enemy.stage3.c, (232, -10))
        yield 240
        Enemy(lib.script.enemy.stage3.c, (332, -10))
        yield 240
        Enemy(lib.script.enemy.stage3.c, (52, -10))
        yield 390

    if chapter <= 4:
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage3.midboss)
        yield 240
        while common.bossExists():
            yield 60
        lib.globals.backgroundScrollSpeed = 1.5
        yield 120

    if chapter <= 5:
        for _ in range(6):
            Enemy(lib.script.enemy.stage3.a, (-5, common.randomInt(24, 64), True))
            Enemy(lib.script.enemy.stage3.a, (389, common.randomInt(24, 64), False))
            yield 45
            Enemy(lib.script.enemy.stage3.b, (112, -10, True))
            Enemy(lib.script.enemy.stage3.b, (272, -10, False))
            yield 45
        for _ in range(2):
            for _ in range(3):
                Enemy(lib.script.enemy.stage3.b, (72, -10, True))
                Enemy(lib.script.enemy.stage3.b, (312, -10, False))
                yield 75
            yield 75
            Enemy(lib.script.enemy.stage3.c, (192, -10))
            yield 150

    if chapter <= 6:
        for i in range(8):
            Enemy(lib.script.enemy.stage3.b, (52, -10, True))
            Enemy(lib.script.enemy.stage3.b, ((132 if i % 2 == 0 else 252), -10, i % 2 == 0))
            Enemy(lib.script.enemy.stage3.b, (332, -10, False))
            yield 90
        yield 360

    if chapter <= 7:
        Enemy(lib.script.enemy.stage3.d, (192, -10, False))
        yield 480
        Enemy(lib.script.enemy.stage3.d, (192, -10, True))
        yield 840

    if chapter <= 8:
        yield common.bossWarning()
        playBgm(BGM.BOSS1)
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage3.boss)
        yield 240
        while common.bossExists():
            yield 60
    yield 360

    lib.globals.backgroundMaskChangeSpeed = 5
    yield 60
    lib.globals.stageFunctionWait = 0
    lib.globals.stageFunction = lib.script.stage.stage4.stageFunction()