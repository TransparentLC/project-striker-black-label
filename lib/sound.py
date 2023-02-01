from calendar import c
import dataclasses
import pygame

import lib.globals
import lib.utils

pygame.mixer.set_num_channels(128)

@dataclasses.dataclass
class SFX:
    EXTEND_HYPER = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/extend-hyper.ogg'))
    EXTEND_LIFE = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/extend-life.ogg'))
    HYPER_ACTIVATE = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/hyper-activate.ogg'))
    HYPER_END = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/hyper-end.ogg'))
    BOSS_ALERT = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/boss-alert.ogg'))
    PHASE_START = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/phase-start.ogg'))
    CHARGE = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/charge.ogg'))
    BONUS = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/bonus.ogg'))
    PAUSE = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/pause.ogg'))
    PAGE = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/page.ogg'))
    MENU = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/menu.ogg'))
    COUNTDOWN = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/countdown.ogg'))
    GET_POINT = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/get-point.ogg'))
    GRAZE_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/graze-a.ogg'))
    GRAZE_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/graze-b.ogg'))
    EXPLODE_PLAYER = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-player.ogg'))
    EXPLODE_ENEMY_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-a.ogg'))
    EXPLODE_ENEMY_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-b.ogg'))
    EXPLODE_ENEMY_C = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-c.ogg'))
    EXPLODE_ENEMY_D = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-d.ogg'))
    PLAYER_SHOOT_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-a.ogg'))
    PLAYER_SHOOT_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-b.ogg'))
    PLAYER_SHOOT_HIT_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-a.ogg'))
    PLAYER_SHOOT_HIT_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-b.ogg'))
    PLAYER_SHOOT_HIT_C = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-c.ogg'))
    PLAYER_SHOOT_HIT_D = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-d.ogg'))
    PLAYER_SHOOT_BLOCK_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-block-a.ogg'))
    PLAYER_SHOOT_BLOCK_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-block-b.ogg'))
    ENEMY_SHOOT_A = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-a.ogg'))
    ENEMY_SHOOT_B = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-b.ogg'))
    ENEMY_SHOOT_C = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-c.ogg'))
    ENEMY_SHOOT_D = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-d.ogg'))
    ENEMY_SHOOT_E = pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-e.ogg'))

for attribute, value in SFX.__dict__.items():
    if isinstance(value, pygame.mixer.Sound):
        value.set_volume(.2)

SFX.COUNTDOWN.set_volume(.5)
SFX.GET_POINT.set_volume(.4)
SFX.PLAYER_SHOOT_A.set_volume(.01)
SFX.PLAYER_SHOOT_B.set_volume(.01)
SFX.PLAYER_SHOOT_HIT_A.set_volume(.02)
SFX.PLAYER_SHOOT_HIT_B.set_volume(.02)
SFX.PLAYER_SHOOT_HIT_C.set_volume(.02)
SFX.PLAYER_SHOOT_HIT_D.set_volume(.02)
SFX.PLAYER_SHOOT_BLOCK_A.set_volume(.1)
SFX.PLAYER_SHOOT_BLOCK_B.set_volume(.1)
SFX.EXPLODE_PLAYER.set_volume(.8)
SFX.EXPLODE_ENEMY_A.set_volume(.3)
SFX.EXPLODE_ENEMY_B.set_volume(.4)
SFX.EXPLODE_ENEMY_C.set_volume(.5)
SFX.EXPLODE_ENEMY_D.set_volume(.5)
SFX.HYPER_ACTIVATE.set_volume(.5)
SFX.HYPER_END.set_volume(.5)
SFX.EXTEND_HYPER.set_volume(.8)
SFX.EXTEND_LIFE.set_volume(.8)
SFX.BOSS_ALERT.set_volume(.6)

@dataclasses.dataclass
class BGM:
    TITLE = ('sound/bgm/title-a.ogg', 'sound/bgm/title-b.ogg')
    STAGE1 = ('sound/bgm/stage1-a.ogg', 'sound/bgm/stage1-b.ogg')
    STAGE2 = ('sound/bgm/stage2-a.ogg', 'sound/bgm/stage2-b.ogg')
    STAGE3 = ('sound/bgm/stage3-a.ogg', 'sound/bgm/stage3-b.ogg')
    STAGE4 = ('sound/bgm/stage4-a.ogg', 'sound/bgm/stage4-b.ogg')
    STAGE5 = ('sound/bgm/stage5-a.ogg', 'sound/bgm/stage5-b.ogg')
    BOSS1 = ('sound/bgm/boss1-a.ogg', 'sound/bgm/boss1-b.ogg')
    BOSS2 = ('sound/bgm/boss2-a.ogg', 'sound/bgm/boss2-b.ogg')
    BOSS3 = ('sound/bgm/boss3-a.ogg', 'sound/bgm/boss3-b.ogg')

def playBgm(bgm: tuple[str, str]):
    if not lib.globals.config['bgm']:
        return
    bgmHeader, bgmLoop = bgm
    pygame.mixer.music.stop()
    pygame.mixer.music.load(lib.utils.getResourceHandler(bgmHeader))
    pygame.mixer.music.play()
    pygame.mixer.music.queue(lib.utils.getResourceHandler(bgmLoop), loops=-1)
