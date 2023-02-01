import pygame

import lib.globals
import lib.replay
import lib.scene.result
import lib.scene.replay
import lib.scroll_map
import lib.sound
import lib.stg_overlay
import lib.textures

def randomInt(minValue: int, maxValue: int):
    return lib.globals.stgRandom.randint(minValue, maxValue)

def randomFloat(minValue: float, maxValue: float):
    return minValue + (maxValue - minValue) * lib.globals.stgRandom.random()

def setBackground(index: int):
    lib.globals.backgroundSurfaces.clear()
    lib.globals.backgroundSurfaces.extend(lib.textures.STAGEBACKGROUND[index][::-1])
    lib.globals.backgroundScrollOffset = 0

def bossWarning() -> int:
    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.WARNING_REMAIN] = 330
    lib.sound.SFX.BOSS_ALERT.play(loops=1)
    return 300

def bossExists() -> bool:
    return bool(lib.globals.groupBoss.sprite)

def setCleared() -> int:
    lib.globals.allCleared = True
    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.CLEAR_REMAIN] = 240
    lib.sound.SFX.EXTEND_LIFE.play()
    return 360

def showResult():
    if lib.globals.replayRecording:
        pygame.mixer.music.stop()
        lib.replay.stopRecording()
        lib.globals.nextScene = lib.scene.result
    else:
        lib.sound.playBgm(lib.sound.BGM.TITLE)
        lib.globals.nextScene = lib.scene.replay
