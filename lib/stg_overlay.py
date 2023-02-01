import enum
import pygame

import lib.constants
import lib.font
import lib.native_utils
import lib.globals
import lib.textures
import lib.utils

phaseNameSurfaces = tuple(
    lib.font.FONT_NORMAL.renderOutlined(x, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0), 3, 18)
    for x in lib.constants.PHASE_NAME
)
phaseNameSurfaces2x = tuple(lib.native_utils.xbrzScale(2, x) for x in phaseNameSurfaces)

class OverLayStatusIndex(enum.IntEnum):
    LIFE_REMAIN = 0
    HYPER_REMAIN = 1
    CLEAR_REMAIN = 2
    WARNING_REMAIN = 3
    PHASE_BONUS_REMAIN = 4
    PHASE_NAME_REMAIN = 5
    PHASE_BONUS_VALUE = 6

overlayStatus = [0, 0, 0, 0, 0, 0, 0, 0]

def update():
    for i in range(6):
        if overlayStatus[i] > 0:
            overlayStatus[i] -= 1

def draw(surface: pygame.Surface):
    if lib.globals.replayRecording and lib.globals.continueRemain:
        surface.blits((
            (lib.textures.STGUI['continue'], (224, 320)),
            lib.utils.getBlitWithOrigin(lib.font.FONT_STGOVERLAY_LARGE.render(str(lib.globals.continueRemain // 60)), 384, 576, 5),
        ))

    blitSeq = []
    for img, remain, centerX, centerY in (
        (lib.textures.STGUI['hyper-extend'], overlayStatus[OverLayStatusIndex.HYPER_REMAIN], 384, 96),
        (lib.textures.STGUI['life-extend'], overlayStatus[OverLayStatusIndex.LIFE_REMAIN], 384, 96),
        (
            lib.textures.STGUI['phase-bonus' if overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE] else 'phase-bonus-failed'],
            overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN], 384, 192
        ),
        (lib.textures.STGUI['all-clear'], overlayStatus[OverLayStatusIndex.CLEAR_REMAIN], 384, 192),
    ):
        if not remain:
            continue
        if remain < 30:
            img = pygame.transform.scale(
                img,
                (
                    img.get_width(),
                    int(lib.utils.linearInterpolation(remain / 30, 0, img.get_height()))
                )
            )
        elif remain > 210:
            img = pygame.transform.scale(
                img, (
                    img.get_width(),
                    int(lib.utils.easeOutQuadInterpolation(1 - (remain - 210) / 30, 0, img.get_height()))
                )
            )
        blitSeq.append(lib.utils.getBlitWithOrigin(img, centerX, centerY, 5))
    if overlayStatus[OverLayStatusIndex.WARNING_REMAIN]:
        appearTime = 330 - overlayStatus[OverLayStatusIndex.WARNING_REMAIN]
        if appearTime < 60:
            appearTime %= 20
            lib.textures.STGUI['boss-warning'].set_alpha(abs(appearTime - 10) / 10 * 255)
        elif appearTime > 300:
            lib.textures.STGUI['boss-warning'].set_alpha((330 - appearTime) / 30 * 255)
        else:
            lib.textures.STGUI['boss-warning'].set_alpha(255)
        blitSeq.append(lib.utils.getBlitWithOrigin(lib.textures.STGUI['boss-warning'], 384, 320, 5))

    if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] and overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE]:
        phaseBonusDigits = lib.utils.splitDigits(overlayStatus[OverLayStatusIndex.PHASE_BONUS_VALUE])
        phaseBonusSurface = pygame.Surface((24 * len(phaseBonusDigits), 64), pygame.SRCALPHA)
        blitSeqInner = []
        for i, x in enumerate(phaseBonusDigits):
            appearTime = 240 - overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN]
            imgDigit = lib.textures.STGUI[f'number-overlay-normal-{x}'].copy()
            imgDigit.set_alpha(lib.utils.clamp((appearTime - 3 * i) / 30 * 255, 0, 255))
            imgX = 24 * i
            imgY = lib.utils.clamp((appearTime - 5 * i) ** 2 / 16, 0, 16)
            blitSeqInner.append((imgDigit, (imgX, imgY)))
        phaseBonusSurface.blits(blitSeqInner)
        if overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] < 30:
            phaseBonusSurface = pygame.transform.scale(
                phaseBonusSurface,
                (
                    phaseBonusSurface.get_width(),
                    int(lib.utils.linearInterpolation(
                        overlayStatus[OverLayStatusIndex.PHASE_BONUS_REMAIN] / 30,
                        0, phaseBonusSurface.get_height()
                    )),
                )
            )
        blitSeq.append(lib.utils.getBlitWithOrigin(phaseBonusSurface, 384, 288, 5))

    if lib.globals.phaseIndex:
        if overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] < 30:
            alpha = round(lib.utils.linearInterpolation(
                overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] / 30,
                255, 0
            ))
            sf = f'{lib.globals.phaseIndex - 1}-{lib.globals.optionType}-{lib.globals.difficultyType}'
            for b in (
                (lib.textures.STGUI['phase-background'], (286, -4)),
                (lib.textures.STGUI['phase-bonus-text'], (445, 56)),
                (lib.textures.STGUI['phase-history-text'], (605, 56)),
                lib.utils.getBlitWithOrigin(
                    lib.font.FONT_STGOVERLAY_SMALL.render(str(lib.globals.phaseBonus) if lib.globals.phaseBonus else '#   '),
                    595, 57, 9,
                ),
                lib.utils.getBlitWithOrigin(
                    lib.font.FONT_STGOVERLAY_SMALL.render((
                        f'{lib.globals.savedata["phase-reward-" + sf]}'
                        '/'
                        f'{lib.globals.savedata["phase-encounter-" + sf]}'
                    )),
                    735, 57, 9,
                ),
            ):
                b[0].set_alpha(alpha)
                blitSeq.append(b)
        if overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] > 60:
            interpolationP = 1 - (overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] - 60) / 60
            phaseNameSurface = phaseNameSurfaces2x[lib.globals.phaseIndex - 1]
            phaseNameSurface = pygame.transform.scale(
                phaseNameSurface,
                tuple(
                    round(x * lib.utils.easeOutCubicInterpolation(interpolationP, 1, .5))
                    for x in phaseNameSurface.get_size()
                )
            )
            phaseNameSurface.set_alpha(round(lib.utils.easeOutCubicInterpolation(interpolationP, 0, 255)))
            blitSeq.append(lib.utils.getBlitWithOrigin(
                phaseNameSurface,
                lib.utils.easeOutCubicInterpolation(interpolationP, 384, 752), 768,
                6,
            ))
        else:
            interpolationP = 1 - overlayStatus[OverLayStatusIndex.PHASE_NAME_REMAIN] / 60
            phaseNameSurface = phaseNameSurfaces[lib.globals.phaseIndex - 1]
            blitSeq.append(lib.utils.getBlitWithOrigin(
                phaseNameSurface,
                752, lib.utils.easeInOutCubicInterpolation(interpolationP, 768, 32),
                6,
            ))

    surface.blits(blitSeq)
