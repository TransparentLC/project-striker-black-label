import pygame

import lib.globals
import lib.utils
import lib.textures

whiteMask = pygame.Surface((384, 448))
whiteMask.fill((255, 255, 255))

def blitBackground(surface: pygame.Surface):
    while lib.globals.backgroundScrollOffset >= 448:
        lib.globals.backgroundSurfaces.append(lib.globals.backgroundSurfaces.popleft())
        lib.globals.backgroundScrollOffset -= 448

    blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = []
    offset = lib.globals.backgroundScrollOffset
    offsetSurface = 0
    while offset >= -448:
        blitSequence.append((lib.globals.backgroundSurfaces[offsetSurface], (0, offset)))
        offset -= 448
        offsetSurface += 1

    if lib.globals.backgroundMaskChangeSpeed:
        lib.globals.backgroundMaskAlpha = int(lib.utils.clamp(lib.globals.backgroundMaskAlpha + lib.globals.backgroundMaskChangeSpeed, 0, 255))
    whiteMask.set_alpha(lib.globals.backgroundMaskAlpha)
    if lib.globals.backgroundMaskAlpha:
        blitSequence.append((whiteMask, (0, 0)))

    surface.blits(blitSequence)
