import os
import platform
import pygame

import lib.constants
import lib.globals
import lib.font
import lib.sound
import lib.textures
import lib.utils

import lib.scene.config
import lib.scene.manual
import lib.scene.player_data
import lib.scene.replay
import lib.scene.select_difficulty

VERSION_TEXT = tuple(lib.font.FONT_SMALL.render(x, pygame.Color(255, 255, 255)) for x in (
    (
        f'Built at {lib.constants.BUILD_INFO[1]} (Commit {lib.constants.BUILD_INFO[0][:7]}) with Python {platform.python_version()} Pygame {pygame.version.ver}'
        if lib.constants.BUILD_INFO else
        f'Built with Python {platform.python_version()} Pygame {pygame.version.ver}'
    ),
    '© 2023 TransparentLC https://akarin.dev',
))

menuChoice = 0

def update():
    global menuChoice

    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.sound.SFX.MENU.play()
        if menuChoice == 0:
            lib.globals.nextScene = lib.scene.select_difficulty
            lib.scene.select_difficulty.difficultyChoice = 0
        elif menuChoice == 1:
            lib.globals.nextScene = lib.scene.replay
            lib.scene.replay.currentPage = 0
            lib.scene.replay.currentItem = 0
            lib.scene.replay.replayPathList = tuple(
                f'{lib.constants.REPLAY_DIR}/{x}'
                for x in os.listdir(lib.constants.REPLAY_DIR)
                if x.endswith('.rep')
            )
            lib.scene.replay.totalPage = -(-len(lib.scene.replay.replayPathList) // 10)
            lib.scene.replay.turnPage()
        elif menuChoice == 2:
            lib.globals.nextScene = lib.scene.player_data
            lib.scene.player_data.currentPage = 0
            lib.scene.player_data.currentType = 0
        elif menuChoice == 3:
            lib.globals.nextScene = lib.scene.manual
            lib.scene.manual.currentPage = 0
        elif menuChoice == 4:
            lib.globals.nextScene = lib.scene.config
            lib.scene.config.currentItem = 0
        elif menuChoice == 5:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    elif (
        (lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]) or
        (lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT])
    ):
        menuChoice = (menuChoice - 1) % 6
        lib.sound.SFX.MENU.play()
    elif (
        (lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]) or
        (lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT])
    ):
        menuChoice = (menuChoice + 1) % 6
        lib.sound.SFX.MENU.play()

def draw(surface: pygame.Surface):
    surface.blits((
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        *((lib.textures.TITLEUI[f'menu-{i}-{1 if menuChoice == i else 0}'], (840, 288 + i * 64)) for i in range(6)),
        *((item, (640 - item.get_width() // 2, 880 + index * 24)) for index, item in enumerate(VERSION_TEXT)),
    ))
