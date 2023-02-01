import os
import platform
import pygame

import lib.constants
import lib.font
import lib.scene.title
import lib.sound
import lib.globals
import lib.textures
import lib.utils

# 一行42个全角字符，一页最多17行，用----------------分页
with lib.utils.getResourceHandler('scriptfiles/manual.txt') as f:
    manualPages = tuple(
        lib.font.FONT_NORMAL.render(x.strip(), pygame.Color(255, 255, 255))
        for x in (f.read().decode('utf-8') + f'''
----------------
# 关于

源代码以GNU AGPL 3.0许可证发布。
https://github.com/TransparentLC/project-striker

Commit: {lib.constants.BUILD_INFO[0] if lib.constants.BUILD_INFO else None}
Build time: {lib.constants.BUILD_INFO[1] if lib.constants.BUILD_INFO else None}

Built with:
　Python {platform.python_version()}
　Pygame {pygame.version.ver}
''').split('----------------'))

currentPage = 0

def update():
    global currentPage
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        currentPage -= 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        currentPage += 1
        lib.sound.SFX.PAGE.play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.SFX.PAGE.play()
    currentPage %= len(manualPages)

def draw(surface: pygame.Surface):
    surface.blits((
        (lib.textures.TITLEIMAGE['background'], (0, 0)),
        (lib.textures.TITLEIMAGE['corner'], (0, 0)),
        (lib.textures.TITLEUI['title-4-0'], (64, 32)),
        (lib.textures.TITLEUI['title-4-1'], (64, 108)),
        (lib.textures.TITLEUI['shade'], (115, 184)),
        (manualPages[currentPage], (135, 198)),
    ))
