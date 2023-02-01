import pygame
import time

import lib.constants
import lib.font
import lib.globals
import lib.newgame
import lib.replay
import lib.scene.title
import lib.sound
import lib.textures
import lib.utils

arrowSurface = lib.font.FONT_NORMAL.render('▶', pygame.Color(255, 255, 255))
emptySurface = lib.font.FONT_NORMAL.render('还没有保存过的REPLAY。', pygame.Color(255, 255, 255))
incorrectVersionSurface = lib.font.FONT_NORMAL.render('REPLAY版本和主程序对应版本不同，可能无法正常播放。', pygame.Color((255, 255, 0)))
incorrectChecksumSurface = lib.font.FONT_NORMAL.render('REPLAY校验失败，无法播放。', pygame.Color((255, 0, 0)))

replayPathList: list[str] = None
currentPage = 0
currentPageReplayData: list[tuple[str, tuple[bytes, int, int, bytes, bytes, int, int, int, int, int, int]]] = None
currentItem = 0
currentHint: pygame.Surface = None
totalPage = 0

def turnPage():
    global currentPage
    global currentPageReplayData
    if totalPage:
        currentPage %= totalPage
    currentPageReplayData = tuple((x, lib.replay.parseReplay(x)) for x in replayPathList[(currentPage * 10):(currentPage * 10 + 10)])

def update():
    global currentPage
    global currentItem
    global currentHint
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentItem = currentItem + 1
        if currentItem > min(len(currentPageReplayData) - 1, 9):
            currentPage += 1
            turnPage()
            currentItem = 0
        currentHint = None if currentPageReplayData[currentItem][1][1] == lib.replay.REPLAY_VERSION else incorrectVersionSurface
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentItem = currentItem - 1
        if currentItem < 0:
            currentPage -= 1
            turnPage()
            currentItem = len(currentPageReplayData) - 1
        currentHint = None if currentPageReplayData[currentItem][1][1] == lib.replay.REPLAY_VERSION else incorrectVersionSurface
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if lib.replay.loadReplay(currentPageReplayData[currentItem][0]):
            lib.newgame.init()
        else:
            currentHint = incorrectChecksumSurface
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.SFX.PAGE.play()

def draw(surface: pygame.Surface):
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-2-0'], (64, 32)),
        (lib.textures.TITLEUI['title-2-1'], (64, 108)),
        (lib.textures.TITLEUI['shade'], (115, 184)),
    ]

    if len(currentPageReplayData):
        blitSequence.append((arrowSurface, (135, 198 + 36 * currentItem)))
        for index, (replayPath, replayHeader) in enumerate(currentPageReplayData):
            blitSequence.append((
                lib.font.FONT_NORMAL.render(f'No.{index + currentPage * 10 + 1:02d}', pygame.Color(255, 255, 255)),
                (175, 198 + 36 * index),
            ))
            blitSequence.append((
                lib.font.FONT_NORMAL.render(''.join(lib.replay.replayNameCharsFullWidth[x] for x in replayHeader[3]), pygame.Color(255, 255, 255)),
                (275, 198 + 36 * index),
            ))
            blitSequence.append((
                lib.font.FONT_NORMAL.render(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(replayHeader[2])), pygame.Color(255, 255, 255)),
                (555, 198 + 36 * index),
            ))
            blitSequence.append((
                lib.font.FONT_NORMAL.render(lib.constants.OPTION_TYPE_NAME[replayHeader[6] & 0b00000011], pygame.Color(255, 255, 255)),
                (875, 198 + 36 * index),
            ))
        currentReplayHeader = currentPageReplayData[currentItem][1]
        blitSequence.append((
            lib.font.FONT_NORMAL.render('\n'.join((
                f'机签：{"".join(lib.replay.replayNameCharsFullWidth[x] for x in currentReplayHeader[3])}',
                f'分数：{currentReplayHeader[5]}',
                f'难度：{lib.constants.DIFFICULTY_NAME[(currentReplayHeader[6] & 0b00001100) >> 2]}',
                f'录制时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(currentReplayHeader[2]))}',
            )), pygame.Color(255, 255, 255)),
            (220, 660),
        ))
        blitSequence.append((
            lib.font.FONT_NORMAL.render('\n'.join((
                f'自机类型：{lib.constants.OPTION_TYPE_NAME[currentReplayHeader[6] & 0b00000011]}',
                f'MISS次数：{currentReplayHeader[7]}',
                f'火力强化次数：{currentReplayHeader[8]}',
                f'完美击破奖励次数：{currentReplayHeader[9]} / {len(lib.constants.PHASE_NAME)}',
            )), pygame.Color(255, 255, 255)),
            (700, 660),
        ))
        if currentHint:
            blitSequence.append(lib.utils.getBlitWithOrigin(currentHint, 640, 840, 5))
    else:
        blitSequence.append(lib.utils.getBlitWithOrigin(emptySurface, 640, 534, 5))
    surface.blits(blitSequence)

    if len(currentPageReplayData):
        pygame.draw.line(surface, (255, 255, 255), (136, 574), (1144, 574))
