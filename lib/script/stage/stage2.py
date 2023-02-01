import lib.globals

from . import common
from lib.sound import playBgm, BGM
from lib.sprite.enemy import Enemy

import lib.script.enemy.stage2.a
import lib.script.enemy.stage2.b
import lib.script.enemy.stage2.c
import lib.script.enemy.stage2.d
import lib.script.enemy.stage2.midboss
import lib.script.enemy.stage2.boss

import lib.script.stage.stage3

def stageFunction():
    common.setBackground(1)
    playBgm(BGM.STAGE2)
    lib.globals.backgroundScrollSpeed = 1.5
    lib.globals.backgroundMaskChangeSpeed = -5
    yield 60
    lib.globals.backgroundMaskChangeSpeed = 0
    yield 180

    chapter = 0

    if chapter <= 0:
        for _ in range(6):
            for i in range(2):
                Enemy(lib.script.enemy.stage2.a, (394, common.randomInt(48, 144), False, i % 2))
            yield 45
        Enemy(lib.script.enemy.stage2.b, (72, -20, False))
        yield 300
        for _ in range(6):
            for i in range(2):
                Enemy(lib.script.enemy.stage2.a, (-10, common.randomInt(48, 144), True, i % 2))
            yield 45
        Enemy(lib.script.enemy.stage2.b, (312, -20, True))
        yield 450

    if chapter <= 1:
        for i in range(4):
            for _ in range(2):
                Enemy(lib.script.enemy.stage2.c, (192 + common.randomInt(50, 150) * (1 if i % 2 else -1), common.randomInt(-80, -20)))
            yield 90
        yield 240
        for i in range(4):
            for _ in range(3):
                Enemy(lib.script.enemy.stage2.c, (192 + common.randomInt(50, 150) * (1 if i % 2 else -1), common.randomInt(-80, -20)))
            yield 90
        yield 300

    if chapter <= 2:
        for _ in range(3):
            for i in range(2):
                Enemy(lib.script.enemy.stage2.a, (394, common.randomInt(24, 84), False, i % 2))
                Enemy(lib.script.enemy.stage2.a, (-10, common.randomInt(24, 84), True, i % 2))
            yield 60
        yield 120

    if chapter <= 3:
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage2.midboss)
        yield 240
        while common.bossExists():
            yield 60
        lib.globals.backgroundScrollSpeed = 1.5
        yield 60

    if chapter <= 4:
        for i in range(2):
            Enemy(lib.script.enemy.stage2.c, (192 + 60 * (1 if i % 2 else -1), -20))
        yield 150
        for i in range(2):
            Enemy(lib.script.enemy.stage2.c, (192 + 90 * (1 if i % 2 else -1), -50))
        yield 150
        for i in range(2):
            Enemy(lib.script.enemy.stage2.b, (192 + 120 * (1 if i % 2 else -1), -30, i % 2 == 1))
        yield 360
        Enemy(lib.script.enemy.stage2.d, (192, -30))
        yield 480

    if chapter <= 5:
        for i in range(6):
            Enemy(lib.script.enemy.stage2.a, (394, common.randomInt(24, 96), False, i % 2))
            Enemy(lib.script.enemy.stage2.a, (-10, common.randomInt(24, 96), True, i % 2))
            yield 30
        yield 120
        Enemy(lib.script.enemy.stage2.d, (192, -30))
        yield 480

    if chapter <= 6:
        yield common.bossWarning()
        playBgm(BGM.BOSS1)
        lib.globals.backgroundScrollSpeed = .8
        Enemy(lib.script.enemy.stage2.boss)
        yield 240
        while common.bossExists():
            yield 60
    yield 360

    lib.globals.backgroundMaskChangeSpeed = 5
    yield 60
    lib.globals.stageFunctionWait = 0
    lib.globals.stageFunction = lib.script.stage.stage3.stageFunction()