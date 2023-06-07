import pygame
import json

import lib.utils
import lib.native_utils

def getPackedSurface(imagePath: str, metadataPath: str) -> dict[str, pygame.Surface]:
    image = pygame.image.load(lib.utils.getResourceHandler(imagePath))
    if image.get_flags() & pygame.SRCALPHA:
        image = image.convert_alpha()
    else:
        image = image.convert()
    with lib.utils.getResourceHandler(metadataPath) as f:
        metadata: dict[str, dict[str, int]] = json.load(f)
    result = {}
    for k, v in metadata.items():
        result[k] = image.subsurface((v['x'], v['y'], v['w'], v['h']))
    return result

PLAYER = getPackedSurface('assets/player.webp', 'assets/player.json')
ENEMY = {
    **getPackedSurface('assets/enemy.webp', 'assets/enemy.json'),
    **getPackedSurface('assets/enemy-alt.webp', 'assets/enemy-alt.json'),
}
EXPLOSION = getPackedSurface('assets/explosion.webp', 'assets/explosion.json')
for k in EXPLOSION:
    if k.startswith('explode-plane-'):
        EXPLOSION[k] = pygame.transform.scale2x(EXPLOSION[k])
EXPLOSION.update({f'{k}-2x': pygame.transform.scale2x(EXPLOSION[k]) for k in EXPLOSION if k.startswith('explode-bullet-')})
ITEM = getPackedSurface('assets/item.webp', 'assets/item.json')
STGBACKGROUND = getPackedSurface('assets/stg-background.webp', 'assets/stg-background.json')
STGUI = getPackedSurface('assets/stg-ui.webp', 'assets/stg-ui.json')
STGUI['boss-warning'] = lib.native_utils.xbrzScale(2, STGUI['boss-warning'])
for i in range(10):
    STGUI[f'number-overlay-large-{i}'] = lib.native_utils.xbrzScale(2, STGUI[f'number-overlay-normal-{i}'])
for i in (
    'bar-bullet-count',
    'bar-time-countdown',
    'bar-boss-status',
):
    STGUI[i] = pygame.transform.scale(STGUI[i], (400, 24))
TITLEIMAGE = getPackedSurface('assets/title-image.webp', 'assets/title-image.json')
TITLEIMAGE['background'] = pygame.image.load(lib.utils.getResourceHandler('assets/title-background.webp')).convert()
TITLEUI = getPackedSurface('assets/title-ui.webp', 'assets/title-ui.json')
TITLEUI['shade'] = pygame.Surface((1050, 700), pygame.SRCALPHA)
pygame.draw.rect(TITLEUI['shade'], (0, 0, 0, 192), TITLEUI['shade'].get_rect(), 0, 8)

STAGEBACKGROUND = tuple(
    tuple(
        i.subsurface((0, 448 * y, 384, 448))
        for y in range(i.get_height() // 448)
    )
    for i in (
        pygame.image.load(lib.utils.getResourceHandler(f'assets/stagebg{i}.webp')).convert()
        for i in range(5)
    )
)