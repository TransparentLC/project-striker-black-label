import lib.globals

from . import common
from lib.sound import playBgm, BGM
from lib.sprite.enemy import Enemy

import lib.script.enemy.stage1.a
import lib.script.enemy.stage1.b
import lib.script.enemy.stage1.c
import lib.script.enemy.stage1.d
import lib.script.enemy.stage1.midboss
import lib.script.enemy.stage1.boss

import lib.script.stage.stage2

def stageFunction():
    common.setBackground(0)
    playBgm(BGM.STAGE1)
    lib.globals.backgroundScrollSpeed = 1.5
    lib.globals.backgroundMaskAlpha = 0
    yield 120

    chapter = 0

    if chapter <= 0:
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (62, -20, False, i % 2))
            Enemy(lib.script.enemy.stage1.a, (82, -20, False, not i % 2))
            yield 15
        yield 120
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (322, -20, True, i % 2))
            Enemy(lib.script.enemy.stage1.a, (292, -20, True, not i % 2))
            yield 15
        yield 120
        for i in range(7):
            Enemy(lib.script.enemy.stage1.b, (52 + 15 * i, -20, False, i % 2))
            Enemy(lib.script.enemy.stage1.b, (332 - 15 * i, -20, True, i % 2))
            yield 20
        yield 120

    if chapter <= 1:
        for i in range(5):
            for _ in range(2):
                Enemy(lib.script.enemy.stage1.c, (common.randomInt(42, 342), common.randomInt(-45, -15)))
            yield 75
        yield 300

    if chapter <= 2:
        for i in range(7):
            for _ in range(4):
                Enemy(lib.script.enemy.stage1.d, (common.randomInt(22, 362), common.randomInt(-45, -15), i % 2))
            yield 30
        yield 60
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (62, -20, False, i % 2))
            Enemy(lib.script.enemy.stage1.a, (82, -20, False, not i % 2))
            yield 15
        yield 90
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (322, -20, True, i % 2))
            Enemy(lib.script.enemy.stage1.a, (292, -20, True, not i % 2))
            yield 15
        yield 90

    if chapter <= 3:
        for i in range(4):
            for _ in range(2):
                Enemy(lib.script.enemy.stage1.c, (common.randomInt(42, 342), common.randomInt(-45, -15)))
            yield 90
        yield 240
        for i in range(5):
            Enemy(lib.script.enemy.stage1.b, (52 + 15 * i, -20, False, i % 2))
            Enemy(lib.script.enemy.stage1.b, (332 - 15 * i, -20, True, i % 2))
            yield 20
        yield 150

    if chapter <= 4:
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage1.midboss)
        yield 240
        while common.bossExists():
            yield 60
        lib.globals.backgroundScrollSpeed = 1.5
        yield 60

    if chapter <= 5:
        for i in range(9):
            i -= 4
            Enemy(lib.script.enemy.stage1.b, (192 + i * 40, -20, False, not i % 2))
            yield 15
        for _ in range(2):
            yield 30
            Enemy(lib.script.enemy.stage1.c, (common.randomInt(242, 342), common.randomInt(-45, -15)))
        yield 60
        for i in range(9):
            i -= 4
            Enemy(lib.script.enemy.stage1.b, (192 - i * 40, -20, True, not i % 2))
            yield 15
        for _ in range(2):
            yield 30
            Enemy(lib.script.enemy.stage1.c, (common.randomInt(42, 142), common.randomInt(-45, -15)))
        yield 60

    if chapter <= 6:
        for i in range(7):
            for _ in range(4):
                Enemy(lib.script.enemy.stage1.d, (common.randomInt(22, 362), common.randomInt(-45, -15), i % 2))
            yield 30
        yield 60
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (62, -20, False, i % 2))
            Enemy(lib.script.enemy.stage1.a, (82, -20, False, not i % 2))
            yield 15
        yield 120
        for i in range(6):
            Enemy(lib.script.enemy.stage1.a, (322, -20, True, i % 2))
            Enemy(lib.script.enemy.stage1.a, (292, -20, True, not i % 2))
            yield 15
        yield 300

    if chapter <= 7:
        yield common.bossWarning()
        playBgm(BGM.BOSS1)
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage1.boss)
        yield 240
        while common.bossExists():
            yield 60
    yield 360

    lib.globals.backgroundMaskChangeSpeed = 5
    yield 60
    lib.globals.stageFunctionWait = 0
    lib.globals.stageFunction = lib.script.stage.stage2.stageFunction()