import pygame

import lib.font
import lib.scene.title
import lib.sound
import lib.textures
import lib.globals

configItems = (
    ('窗口模式', '以窗口模式运行游戏，下次启动游戏时生效。', 'windowed', bool),
    ('BGM', '控制是否播放BGM。', 'bgm', bool),
    ('Scale2x', '使用Scale2x算法对游戏画面进行放大，以平滑风格代替像素风格。', 'scale2x', bool),
    ('输入显示', '在右下角显示按下的按键。', 'inputDisplay', bool),
)
configItemSurfaces = tuple(
    (
        lib.font.FONT_LARGE.render(x[0], pygame.Color(255, 255, 255)),
        lib.font.FONT_SMALL.render(x[1], pygame.Color(255, 255, 255)),
    )
    for x in configItems
)
arrowSurface = lib.font.FONT_LARGE.render('▶', pygame.Color(255, 255, 255))
boolSurface = (
    lib.font.FONT_LARGE.render('ＯＦＦ', pygame.Color(255, 255, 255)),
    lib.font.FONT_LARGE.render('Ｏ　Ｎ', pygame.Color(255, 255, 255)),
)
currentItem = 0

def update():
    global currentItem
    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        currentItem -= 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        currentItem += 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if configItems[currentItem][3] == bool:
            lib.globals.config[configItems[currentItem][2]] = not lib.globals.config[configItems[currentItem][2]]
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        if lib.globals.config['bgm']:
            if not pygame.mixer.music.get_busy():
                lib.sound.playBgm(lib.sound.BGM.TITLE)
        else:
            pygame.mixer.music.stop()
        lib.globals.nextScene = lib.scene.title
        lib.sound.SFX.PAGE.play()
    currentItem %= len(configItems)

def draw(surface: pygame.Surface):
    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-5-0'], (64, 32)),
        (lib.textures.TITLEUI['title-5-1'], (64, 108)),
        (lib.textures.TITLEUI['shade'], (115, 184)),
        (arrowSurface, (135, 198 + 96 * currentItem)),
    ]
    for index, item in enumerate(configItems):
        blitSequence.append((configItemSurfaces[index][0], (183, 198 + 96 * index)))
        blitSequence.append((configItemSurfaces[index][1], (183, 246 + 96 * index)))
        if item[3] == bool:
            blitSequence.append((boolSurface[1 if lib.globals.config[item[2]] else 0], (1035, 198 + 96 * index)))
    surface.blits(blitSequence)
