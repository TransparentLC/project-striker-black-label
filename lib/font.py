import functools
import math
import pygame

import lib.utils
import lib.textures

@functools.cache
def getOutlineOffsets(outlineWidth: int, divide: int = None) -> set[tuple[int, int]]:
    if divide is None:
        divide = outlineWidth * 4
    result = set()
    for r in range(1, outlineWidth + 1):
        result.update(
            (
                round(outlineWidth + r * math.cos(i / divide * 2 * math.pi)),
                round(outlineWidth + r * math.sin(i / divide * 2 * math.pi)),
            )
            for i in range(divide)
        )
    return result

class Font:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def render(self, text: str, color: pygame.Color) -> pygame.Surface:
        lines = text.splitlines()
        lineSizes = tuple(self.font.size(x) for x in lines)
        result = pygame.Surface((max(x[0] for x in lineSizes), sum(x[1] for x in lineSizes)), pygame.SRCALPHA)
        acc = 0
        blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = []
        for line in lines:
            line = self.font.render(line, True, color)
            blitSequence.append((line, (0, acc)))
            acc += line.get_height()
        result.blits(blitSequence)
        return result

    def renderOutlined(
        self, text: str, color: pygame.Color,
        outlineColor: pygame.Color, outlineWidth: int, divide: int = None,
    ) -> pygame.Surface:
        outline = self.render(text, outlineColor)
        result = pygame.Surface(tuple(x + 2 * outlineWidth for x in outline.get_size()), pygame.SRCALPHA)
        blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = [(outline, x) for x in getOutlineOffsets(outlineWidth, divide)]
        blitSequence.append((self.render(text, color), (outlineWidth, outlineWidth)))
        result.blits(blitSequence)
        return result

class BitmapFont:
    emptySurface = pygame.Surface((1, 1), pygame.SRCALPHA)

    @classmethod
    def fromPacked(cls, textures: dict[str, pygame.Surface], prefix: str, chars: str, width: int, height: int):
        return cls({x: textures[prefix + x] for x in chars}, width, height)

    def __init__(self, font: dict[str, pygame.Surface], width: int, height: int) -> None:
        self.font = font
        self.width = width
        self.height = height
        for alias, char in (
            ('comma', ','),
            ('dot', '.'),
            ('hash', '#'),
            ('asterisk', '*'),
            ('slash', '/'),
            ('question', '?'),
        ):
            if alias in self.font:
                self.font[char] = self.font[alias]

    def render(self, text: str):
        if not text:
            return self.emptySurface
        lines = text.splitlines()
        result = pygame.Surface((self.width * max(len(x) for x in lines), self.height * len(lines)), pygame.SRCALPHA)
        blitSequence: list[tuple[pygame.Surface, tuple[float, float]]] = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in self.font:
                    blitSequence.append((self.font[char], (self.width * x, self.height * y)))
        result.blits(blitSequence)
        return result

class FontRenderer:
    def __init__(self, font: pygame.font.Font, color: pygame.Color) -> None:
        self.cached: pygame.Surface = None
        self.font = font
        self.color = color
        self.text = ''

    def render(self, text: str) -> pygame.Surface:
        if not self.cached or text != self.text:
            # print('Create font cache')
            self.text = text
            sizes = tuple(self.font.size(x) for x in text.splitlines())
            width = max(x[0] for x in sizes)
            height = sum(x[1] for x in sizes)
            self.cached = pygame.Surface((width, height), pygame.SRCALPHA)
            acc = 0
            for line, (width, height) in zip(text.splitlines(), sizes):
                self.cached.blit(self.font.render(line, True, self.color), (0, acc))
                acc += height
        return self.cached

FONT_FILE = 'font/LXGWWenKai-Regular.ttf'

FONT_SMALL = Font(pygame.font.Font(lib.utils.getResourceHandler(FONT_FILE), 16))
FONT_NORMAL = Font(pygame.font.Font(lib.utils.getResourceHandler(FONT_FILE), 24))
FONT_LARGE = Font(pygame.font.Font(lib.utils.getResourceHandler(FONT_FILE), 32))

digits = '0123456789'
FONT_ITEM = BitmapFont.fromPacked(lib.textures.ITEM, 'item-effect-', digits, 6, 8)
FONT_ITEM_HIGHLIGHT = BitmapFont.fromPacked(lib.textures.ITEM, 'item-effect-highlight-', digits, 6, 8)
FONT_STGOVERLAY_SMALL = BitmapFont.fromPacked(lib.textures.STGUI, 'number-overlay-small-', (*digits, 'hash', 'slash'), 12, 16)
FONT_STGOVERLAY_NORMAL = BitmapFont.fromPacked(lib.textures.STGUI, 'number-overlay-normal-', digits, 24, 32)
FONT_STGOVERLAY_LARGE = BitmapFont.fromPacked(lib.textures.STGUI, 'number-overlay-large-', digits, 48, 64)
FONT_STGUI = BitmapFont.fromPacked(
    lib.textures.STGUI,
    'number-ui-',
    (*digits, 'comma', 'dot', 'hash', 'asterisk', 'slash', 'question'),
    21, 36,
)