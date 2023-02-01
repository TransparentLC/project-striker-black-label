import os
import pygame

import lib.constants
import lib.globals
import lib.newgame
import lib.replay
import lib.sound
import lib.textures
import lib.utils

import lib.scene.stg
import lib.scene.select_difficulty

optionChoice = 0

def update():
    global optionChoice

    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.select_difficulty
        lib.sound.SFX.PAGE.play()
    elif (
        (lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]) or
        (lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP])
    ):
        optionChoice = (optionChoice - 1) % 4
        lib.sound.SFX.PAGE.play()
    elif (
        (lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]) or
        (lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN])
    ):
        optionChoice = (optionChoice + 1) % 4
        lib.sound.SFX.PAGE.play()
    elif lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.globals.optionType = optionChoice
        lib.globals.stgRandomSeed = os.urandom(8)
        lib.newgame.init()
        lib.replay.startRecording()

def draw(surface: pygame.Surface):
    if optionChoice in {0, 1}:
        previewBackground = lib.textures.TITLEIMAGE['option-preview-a']
    elif optionChoice in {2, 3}:
        previewBackground = lib.textures.TITLEIMAGE['option-preview-b']

    surface.blits((
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-1-0'], (64, 32)),
        (lib.textures.TITLEUI['title-1-1'], (64, 108)),
        lib.utils.getBlitWithOrigin(
            previewBackground,
            404, 540, 5,
        ),
        lib.utils.getBlitWithOrigin(
            lib.textures.TITLEUI[f'option-preview-{optionChoice}'],
            404, 540, 5,
        ),
        lib.utils.getBlitWithOrigin(
            lib.textures.TITLEUI[f'option-title-{optionChoice}'],
            934, 390, 5,
        ),
        lib.utils.getBlitWithOrigin(
            lib.textures.TITLEUI[f'option-description-{optionChoice}'],
            934, 660, 5,
        ),
    ))
