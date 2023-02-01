import os
import pygame

import lib.constants
import lib.globals
import lib.newgame
import lib.replay
import lib.sound
import lib.textures
import lib.utils

import lib.scene.select_option
import lib.scene.title

difficultyChoice = 0

def update():
    global difficultyChoice

    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.SFX.PAGE.play()
    elif (
        (lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]) or
        (lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP])
    ):
        difficultyChoice = (difficultyChoice - 1) % 3
        lib.sound.SFX.PAGE.play()
    elif (
        (lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]) or
        (lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN])
    ):
        difficultyChoice = (difficultyChoice + 1) % 3
        lib.sound.SFX.PAGE.play()
    elif lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        lib.globals.difficultyType = difficultyChoice
        lib.globals.nextScene = lib.scene.select_option
        lib.scene.select_option.optionChoice = 0
        lib.sound.SFX.MENU.play()

def draw(surface: pygame.Surface):
    surface.blits((
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-0-0'], (64, 32)),
        (lib.textures.TITLEUI['title-0-1'], (64, 108)),
        *(
            lib.utils.getBlitWithOrigin(
                lib.textures.TITLEIMAGE[f'difficulty-{i}-{1 if difficultyChoice == i else 0}'],
                640, 284 + i * 256, 5,
            ) for i in range(3)
        ),
    ))
