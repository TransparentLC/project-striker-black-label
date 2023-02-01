import os
import pygame
import tarfile
import typing

T = typing.TypeVar('T')

PACKED_RESOURCE_HANDLER = tarfile.open('resources.tar', 'r:') if os.path.exists('resources.tar') else None

def clamp(value: T, min: T, max: T) -> T:
    if value < min:
        return min
    elif max < value:
        return max
    else:
        return value

def frameToSeconds(frame: int) -> str:
    return f'{frame / 60:.02f}'

def splitDigits(value: int) -> typing.Sequence[int]:
    if not value:
        return [0]
    result = []
    while value:
        result.append(value % 10)
        value //= 10
    result.reverse()
    return result

def getResourceHandler(path: str) -> typing.IO[bytes]:
    if PACKED_RESOURCE_HANDLER and path in PACKED_RESOURCE_HANDLER.getnames():
        return PACKED_RESOURCE_HANDLER.extractfile(path)
    else:
        return open(path, 'rb')

def getBlitWithOrigin(src: pygame.Surface, x: int, y: int, origin: int) -> tuple[pygame.Surface, tuple[int, int]]:
    return (
        src,
        (
            # Origin as keypad        32: No offset   0: Full offset  1: Half Offset
            #                         0   1   2   3   4   5   6   7   8   9
            x - (src.get_width()  >> (32, 32,  1,  0, 32,  1,  0, 32,  1,  0)[origin]),
            y - (src.get_height() >> (32,  0,  0,  0,  1,  1,  1, 32, 32, 32)[origin]),
        )
    )

def linearInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * p

def easeInQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p ** 2)

def easeOutQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p * (2 - p))

def easeInOutQuadInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((2 * (p ** 2)) if p < .5 else (-1 + (4 - 2 * p) * p))

def easeInCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * (p ** 3)

def easeOutCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((p - 1) ** 3 + 1)

def easeInOutCubicInterpolation(p: float, a: T, b: T) -> T:
    return a + (b - a) * ((4 * (p ** 3)) if p < .5 else (1 + (p - 1) * ((2 * p - 2) ** 2)))
