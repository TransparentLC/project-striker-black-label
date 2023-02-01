import lib.globals

from . import common
from lib.sound import playBgm, BGM
from lib.sprite.enemy import Enemy

import lib.script.enemy.stage5.a
import lib.script.enemy.stage5.b
import lib.script.enemy.stage5.c
import lib.script.enemy.stage5.d
import lib.script.enemy.stage5.e
import lib.script.enemy.stage5.boss
import lib.script.enemy.stage5.exboss

def stageFunction():
    common.setBackground(4)
    playBgm(BGM.STAGE5)
    lib.globals.backgroundScrollSpeed = 1.5
    lib.globals.backgroundMaskChangeSpeed = -5
    yield 60
    lib.globals.backgroundMaskChangeSpeed = 0
    yield 120

    chapter = 0

    if chapter <= 0:
        for i in range(8):
            Enemy(lib.script.enemy.stage5.a, (52 + 40 * i, -60 + abs(i - 3.5) * 15, True))
            yield 10
        yield 360
        for i in range(8):
            Enemy(lib.script.enemy.stage5.a, (332 - 40 * i, -60 + abs(i - 3.5) * 15, False))
            yield 10
        yield 360

    if chapter <= 1:
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(32, 92), common.randomInt(-80, -10)))
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(92, 152), common.randomInt(-80, -10)))
        yield 120
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(132, 192), common.randomInt(-80, -10)))
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(192, 252), common.randomInt(-80, -10)))
        yield 120
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(232, 292), common.randomInt(-80, -10)))
        Enemy(lib.script.enemy.stage5.b, (common.randomInt(292, 352), common.randomInt(-80, -10)))
        yield 480
        Enemy(lib.script.enemy.stage5.c, (common.randomInt(92 - 40, 92 + 40), common.randomInt(-50, -10)))
        Enemy(lib.script.enemy.stage5.c, (common.randomInt(292 - 40, 292 + 40), common.randomInt(-50, -10)))
        yield 540

    if chapter <= 2:
        for _ in range(2):
            for i in range(2):
                Enemy(lib.script.enemy.stage5.a, (52 + 90 * i, -50 - 10 * i, False))
                yield 10
            yield 60
            for i in range(2):
                Enemy(lib.script.enemy.stage5.a, (332 - 90 * i, -50 - 10 * i, True))
                yield 10
            yield 60
            for i in range(2):
                Enemy(lib.script.enemy.stage5.a, (52 + 90 * i, -30 + 10 * i, False))
                yield 10
            yield 60
            for i in range(2):
                Enemy(lib.script.enemy.stage5.a, (332 - 90 * i, -30 + 10 * i, True))
                yield 10
            yield 60
        yield 180

    if chapter <= 3:
        for _ in range(2):
            for i in range(4):
                if i % 2 == 0:
                    for j in range(-1, 2):
                        Enemy(lib.script.enemy.stage5.d, (192 + 90 * j, -50, 220 - i * 40, i))
                else:
                    for j in range(-2, 2):
                        j += .5
                        Enemy(lib.script.enemy.stage5.d, (192 + 90 * j, -50, 220 - i * 40, i))
                yield 60
            yield 60
            for i in range(3, -1, -1):
                if i % 2 == 0:
                    for j in range(-1, 2):
                        Enemy(lib.script.enemy.stage5.d, (192 + 90 * j, -50, 220 - i * 40, i))
                else:
                    for j in range(-2, 2):
                        j += .5
                        Enemy(lib.script.enemy.stage5.d, (192 + 90 * j, -50, 220 - i * 40, i))
                yield 60
            yield 60
        yield 240

    if chapter <= 4:
        Enemy(lib.script.enemy.stage5.e, (192, -20))
        yield 960

    if chapter <= 5:
        yield common.bossWarning()
        playBgm(BGM.BOSS2)
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage5.boss)
        yield 240
        while common.bossExists():
            yield 10
        if lib.globals.difficultyType == 2 and not lib.globals.continueCount:
            Enemy(lib.script.enemy.stage5.exboss)
            playBgm(BGM.BOSS3)
            yield 180
            common.bossWarning()
            for _ in range(30):
                lib.globals.backgroundScrollSpeed += .15
                yield 10
            while common.bossExists():
                yield 10
        yield 240
        yield common.setCleared()
        common.showResult()
