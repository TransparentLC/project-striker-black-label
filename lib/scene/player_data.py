import pygame

import lib.constants
import lib.font
import lib.scene.title
import lib.sound
import lib.textures
import lib.globals
import lib.utils

currentPage = 0
currentType = 0
currentDifficulty = 0
totalPage = -(-len(lib.constants.PHASE_NAME) // 16)

def update():
    global currentPage
    global currentType
    global currentDifficulty
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        currentType -= 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        currentType += 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentDifficulty += 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentDifficulty -= 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        currentPage += 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.SFX.PAGE.play()
    currentType %= len(lib.constants.OPTION_TYPE_NAME)
    currentDifficulty %= len(lib.constants.DIFFICULTY_NAME)
    currentPage %= totalPage

def draw(surface: pygame.Surface):
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-3-0'], (64, 32)),
        (lib.textures.TITLEUI['title-3-1'], (64, 108)),
        (lib.textures.TITLEUI['shade'], (115, 184)),
        (lib.font.FONT_LARGE.render(
            f'{lib.constants.OPTION_TYPE_NAME[currentType]} {lib.constants.DIFFICULTY_NAME[currentDifficulty]}',
            pygame.Color(255, 255, 255)), (135, 210),
        ),
    ]

    sd = lib.globals.savedata
    sf = f'{currentType}-{currentDifficulty}'
    blitSequence.append(lib.utils.getBlitWithOrigin(
        lib.font.FONT_SMALL.render(
            f'最高分数：{sd["highscore-" + sf]}',
            pygame.Color(255, 255, 255),
        ),
        1145, 210, 6,
    ))
    blitSequence.append(lib.utils.getBlitWithOrigin(
        lib.font.FONT_SMALL.render(
            (
                '获得过的完美奖励：'
                f'{len(tuple(i for i in range(len(lib.constants.PHASE_NAME)) if sd[f"phase-reward-{i}-{sf}"]))}'
                ' / '
                f'{len(lib.constants.PHASE_NAME)}'
            ),
            pygame.Color(255, 255, 255),
        ),
        1145, 234, 6,
    ))

    for i in range(min(16, len(lib.constants.PHASE_NAME) - currentPage * 16)):
        phaseIndex = i + currentPage * 16
        blitSequence.append(lib.utils.getBlitWithOrigin(
            lib.font.FONT_NORMAL.render(f'No.{phaseIndex + 1:02d}', pygame.Color(255, 255, 255)),
            135, 274 + 36 * i, 4,
        ))
        blitSequence.append(lib.utils.getBlitWithOrigin(
            lib.font.FONT_NORMAL.render(
                lib.constants.PHASE_NAME[phaseIndex] if sd[f'phase-encounter-{phaseIndex}-{sf}'] else '???',
                pygame.Color(255, 255, 255),
            ),
            235, 274 + 36 * i, 4,
        ))
        blitSequence.append(lib.utils.getBlitWithOrigin(
            lib.font.FONT_NORMAL.render(
                (
                    f'{sd[f"phase-reward-{phaseIndex}-{sf}"]}'
                    ' / '
                    f'{sd[f"phase-encounter-{phaseIndex}-{sf}"]}'
                ) if sd[f'phase-encounter-{phaseIndex}-{sf}'] else '??? / ???',
                pygame.Color(255, 255, 255),
            ),
            1145, 274 + 36 * i, 6,
        ))

    surface.blits(blitSequence)
