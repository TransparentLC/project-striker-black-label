import os
import importlib
import pygame

import lib.constants
import lib.globals
import lib.sprite.player
import lib.sprite.option
import lib.stg_overlay
import lib.utils
import lib.scene.stg

import lib.script.stage.stage1 as stage

def init():
    lib.globals.stgRandom.seed(lib.globals.stgRandomSeed, version=2)

    if lib.globals.optionType in {0, 1}:
        lib.sprite.player.PlayerA()
    elif lib.globals.optionType in {2, 3}:
        lib.sprite.player.PlayerB()

    lib.globals.score = 0
    lib.globals.scoreDisplay = 0
    lib.globals.scoreLastFrame = 0
    lib.globals.grazeCount = 0
    lib.globals.maxGetPoint = lib.constants.INITIAL_MAXGETPOINT
    lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM
    lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
    lib.globals.timeCountdown = None
    lib.globals.timeCountdownMax = 0
    lib.globals.missedCount = 0
    lib.globals.hyperUsedCount = 0
    lib.globals.phaseIndex = 0
    lib.globals.phaseBonusCount = 0
    lib.globals.clearBulletCenter = None
    lib.globals.clearBulletRadius = 0
    lib.globals.clearBulletBonus = False
    lib.globals.continueCount = 0
    lib.globals.continueRemain = 0
    lib.globals.continueEnabled = True
    lib.globals.allCleared = False
    lib.globals.backgroundScrollOffset = 0
    lib.globals.backgroundMaskAlpha = 0
    lib.globals.backgroundMaskChangeSpeed = 0
    for i in range(len(lib.stg_overlay.overlayStatus)):
        lib.stg_overlay.overlayStatus[i] = 0
    for g in (
        lib.globals.groupPlayerOption,
        lib.globals.groupPlayerBullet,
        lib.globals.groupEnemy,
        lib.globals.groupEnemyBullet,
        lib.globals.groupBoss,
        lib.globals.groupParticle,
        lib.globals.groupItem,
    ):
        g.empty()

    if lib.globals.optionType == 0:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeAH(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
            lib.sprite.option.OptionTypeAH(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
            lib.sprite.option.OptionTypeAH(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
            lib.sprite.option.OptionTypeAH(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
        )
    elif lib.globals.optionType == 1:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeAW(8, pygame.Vector2(-25, 5), pygame.Vector2(-15, -20), 8, 10, True),
            lib.sprite.option.OptionTypeAW(8, pygame.Vector2(25, 5), pygame.Vector2(15, -20), -8, -10, False),
            lib.sprite.option.OptionTypeAW(8, pygame.Vector2(-50, 10), pygame.Vector2(-35, -5), 15, 50, False),
            lib.sprite.option.OptionTypeAW(8, pygame.Vector2(50, 10), pygame.Vector2(35, -5), -15, -50, True),
        )
    elif lib.globals.optionType == 2:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeBD(8, pygame.Vector2(-45, 5), pygame.Vector2(-30, -15), 0, 0),
            lib.sprite.option.OptionTypeBD(8, pygame.Vector2(45, 5), pygame.Vector2(30, -15), 0, 0),
            lib.sprite.option.OptionTypeBD(8, pygame.Vector2(-30, 20), pygame.Vector2(-10, -20), 0, 0),
            lib.sprite.option.OptionTypeBD(8, pygame.Vector2(30, 20), pygame.Vector2(10, -20), 0, 0),
        )
    elif lib.globals.optionType == 3:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeBS(8, pygame.Vector2(-30, -5), pygame.Vector2(-15, -15), -4, -2),
            lib.sprite.option.OptionTypeBS(8, pygame.Vector2(30, -5), pygame.Vector2(15, -15), 4, 2),
        )

    if os.environ.get('STRIKER_DEBUG_DISABLE_ENEMY_CACHE'):
        importlib.reload(stage)
    lib.globals.stageFunctionWait = 0
    lib.globals.stageFunction = stage.stageFunction()

    lib.globals.nextScene = lib.scene.stg
