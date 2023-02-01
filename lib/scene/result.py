import pygame

import lib.constants
import lib.font
import lib.globals
import lib.replay
import lib.scene.title
import lib.sound
import lib.stg_overlay
import lib.utils

background = pygame.image.load(lib.utils.getResourceHandler('assets/ui-result-background.webp')).convert()

# 一行16个全角字符
commentText = tuple(lib.font.FONT_LARGE.render(x, pygame.Color(255, 255, 255)) for x in (
    '满身疮痍……\n以不续关通关为目标继续努力吧！',
    '虽然击破了最终BOSS但是续关了……\n下次再尝试以没有续关的状态攻略到\n这里吧！',
    '完全通关了呢！真了不起！\n不过这还不是结束……\n尝试在最高难度下不续关通关吧！',
    '击破隐藏BOSS了呢！\n非常感谢你玩这个游戏，在弹幕决斗\n结束后就喝杯茶休息一会儿吧～',
    '以No Miss的结果完美通关了！\n很不容易呢！不中弹很困难吧？',
    'No Miss No Hyper通关了！\n厉害啊……\n你真的没有使用秘籍吗？',
))
saveReplayText = lib.font.FONT_LARGE.render(
    '保存本次游戏的REPLAY？\n\n\n　　　　　　　↑↓←→－输入机签\n　　　　　　　Ｚ－确认　Ｘ－放弃\n　　按住ＬＳｈｉｆｔ快速选择字符',
    pygame.Color(255, 255, 255),
)
cannotSaveReplayText = lib.font.FONT_LARGE.render('在续关的情况下不能保存REPLAY。', pygame.Color(255, 255, 255))
replayNameBuffer = bytearray(ord(' ') for i in range(8))
replayNameInputPosition = 0
replayNameInputPositionBlink = 0

def returnToTitle():
    lib.sound.SFX.PAGE.play()
    lib.sound.playBgm(lib.sound.BGM.TITLE)
    lib.globals.nextScene = lib.scene.title

def update():
    global replayNameInputPosition
    global replayNameInputPositionBlink

    if lib.globals.continueCount:
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            returnToTitle()
    else:
        replayNameInputPositionBlink += 1
        replayNameInputPositionBlink &= 31
        if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
            lib.replay.saveReplay(replayNameBuffer)
            returnToTitle()
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            returnToTitle()
        if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
            replayNameInputPosition -= 1
            replayNameInputPosition %= 8
        if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
            replayNameInputPosition += 1
            replayNameInputPosition %= 8
        if lib.globals.keys[pygame.K_UP] and (lib.globals.keys[pygame.K_LSHIFT] or not lib.globals.keysLastFrame[pygame.K_UP]):
            replayNameBuffer[replayNameInputPosition] = lib.replay.replayNameCharsAscii[(lib.replay.replayNameCharsAscii.index(replayNameBuffer[replayNameInputPosition]) - 1) % len(lib.replay.replayNameChars)]
        if lib.globals.keys[pygame.K_DOWN] and (lib.globals.keys[pygame.K_LSHIFT] or not lib.globals.keysLastFrame[pygame.K_DOWN]):
            replayNameBuffer[replayNameInputPosition] = lib.replay.replayNameCharsAscii[(lib.replay.replayNameCharsAscii.index(replayNameBuffer[replayNameInputPosition]) + 1) % len(lib.replay.replayNameChars)]

def draw(surface: pygame.Surface):
    surface.blit(background, (0, 0))
    for text, (posX, posY) in (
        (lib.constants.OPTION_TYPE_NAME[lib.globals.optionType], (576, 280)),
        (f'Continue×{lib.globals.continueCount}' if lib.globals.continueCount else str(lib.globals.score), (576, 360)),
        (str(lib.globals.grazeCount), (576, 440)),
        (str(lib.globals.missedCount), (576, 520)),
        (str(lib.globals.hyperUsedCount), (576, 600)),
        (f'{lib.globals.phaseBonusCount} / {len(lib.constants.PHASE_NAME)}', (576, 680)),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, pygame.Color(255, 255, 255))
        surface.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
    if not lib.globals.allCleared:
        commentSurface = commentText[0]
    elif lib.globals.continueCount:
        commentSurface = commentText[1]
    elif lib.globals.difficultyType == 2:
        if not lib.globals.missedCount:
            if not lib.globals.hyperUsedCount:
                commentSurface = commentText[5]
            else:
                commentSurface = commentText[4]
        else:
            commentSurface = commentText[3]
    else:
        commentSurface = commentText[2]

    surface.blit(commentSurface, (708, 256))
    if lib.globals.continueCount:
        surface.blit(cannotSaveReplayText, (708, 418))
    else:
        surface.blit(saveReplayText, (708, 418))
        surface.blit(
            lib.font.FONT_LARGE.render(
                '[' + ''.join(lib.replay.replayNameCharsFullWidth[x] for x in replayNameBuffer) + ']',
                pygame.Color(255, 255, 255),
            ),
            (824, 482)
        )
        surface.blit(
            lib.font.FONT_LARGE.render(
                ''.join(('＿' if i == replayNameInputPosition and replayNameInputPositionBlink & 16 else '　') for i in range(8)),
                pygame.Color(255, 255, 255),
            ),
            (834, 490)
        )
