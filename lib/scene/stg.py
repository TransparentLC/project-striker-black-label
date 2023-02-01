import os
import pygame

import lib.constants
import lib.debug
import lib.font
import lib.globals
import lib.replay
import lib.scene.replay
import lib.scene.result
import lib.scene.title
import lib.scroll_map
import lib.sound
import lib.stg_overlay
import lib.sprite.player
import lib.sprite.item
import lib.textures
import lib.utils

def update():
    player: lib.sprite.player.Player = lib.globals.groupPlayer.sprite

    if not lib.globals.continueRemain:
        if lib.globals.replayRecording:
            lib.globals.replayKeyStream.write(bytes([lib.replay.readKeys()]))
        else:
            lib.replay.setKeys(lib.globals.replayKeyStream.read(1)[0] or 0)
        lib.globals.scoreLastFrame = lib.globals.score

        if lib.globals.stageFunctionWait:
            lib.globals.stageFunctionWait -= 1
        if lib.globals.stageFunction and not lib.globals.stageFunctionWait:
            try:
                lib.globals.stageFunctionWait = next(lib.globals.stageFunction) - 1
            except StopIteration:
                pass
        lib.globals.backgroundScrollOffset += lib.globals.backgroundScrollSpeed

        if os.environ.get('STRIKER_DEBUG_PLAYER_INVINCIBLE'):
            player.invincibleRemain = player.frameCounter

        if lib.globals.clearBulletCenter:
            for b in lib.globals.groupEnemyBullet:
                if (b.position - lib.globals.clearBulletCenter).length() < lib.globals.clearBulletRadius:
                    if lib.globals.clearBulletBonus:
                        lib.sprite.item.PointBullet(pygame.Vector2(b.position))
                    b.explode()
            lib.globals.clearBulletRadius += 10
        if lib.globals.clearBulletRadius > 500:
            lib.globals.clearBulletCenter = None

        if lib.globals.timeCountdown is not None:
            lib.globals.timeCountdown -= 1
            if lib.globals.timeCountdown <= 600 and lib.globals.timeCountdown % 60 == 0:
                lib.sound.SFX.COUNTDOWN.play()
        if lib.globals.timeCountdown == 0:
            if lib.globals.groupBoss.sprite:
                lib.globals.groupBoss.sprite.hitpoint = lib.globals.bossHitpointRangeMin - 1
            lib.globals.phaseBonus = 0
            lib.globals.timeCountdown = None
            lib.sound.SFX.HYPER_END.play()

        for g in lib.globals.stgGroups:
            g.update()

        lib.globals.phaseBonus = max(0, lib.globals.phaseBonus - lib.globals.phaseBonusDrop)

        scoreDiff = lib.globals.score - lib.globals.scoreDisplay
        lib.globals.scoreDisplay += scoreDiff if scoreDiff < 1024 else max(1024, scoreDiff >> 3)

        if not lib.globals.continueCount:
            if (
                lib.globals.replayRecording and
                lib.globals.savedata[f'highscore-{lib.globals.optionType}-{lib.globals.difficultyType}'] < lib.globals.score
            ):
                lib.globals.savedata[f'highscore-{lib.globals.optionType}-{lib.globals.difficultyType}'] = lib.globals.score

            for extendLimit in (
                50000000,
                150000000,
                300000000,
                500000000,
            ):
                if (
                    lib.globals.scoreLastFrame < extendLimit and
                    extendLimit <= lib.globals.score and
                    lib.globals.lifeNum < lib.constants.LIMIT_LIFENUM
                ):
                    lib.globals.lifeNum += 1
                    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.LIFE_REMAIN] = 240
                    lib.sound.SFX.EXTEND_LIFE.play()

    if lib.globals.continueRemain:
        if lib.globals.replayRecording and lib.globals.continueEnabled:
            if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
                lib.sound.SFX.HYPER_ACTIVATE.play()
                lib.globals.continueCount += 1
                lib.globals.continueRemain = 0
                lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM + 1
            else:
                if lib.globals.continueRemain % 60 == 0:
                    lib.sound.SFX.COUNTDOWN.play()
                if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
                    lib.globals.continueRemain -= 60
                    if lib.globals.continueRemain < 0:
                        lib.globals.continueRemain = 0
                    lib.sound.SFX.COUNTDOWN.play()
                else:
                    lib.globals.continueRemain -= 1
                if not lib.globals.continueRemain:
                    lib.sound.SFX.HYPER_END.play()
                    pygame.mixer.music.stop()
                    lib.replay.stopRecording()
                    lib.globals.nextScene = lib.scene.result
        else:
            lib.sound.SFX.HYPER_END.play()
            if lib.globals.replayRecording:
                pygame.mixer.music.stop()
                lib.replay.stopRecording()
                lib.globals.nextScene = lib.scene.result
            else:
                lib.sound.playBgm(lib.sound.BGM.TITLE)
                lib.globals.nextScene = lib.scene.replay

    if lib.globals.keys[pygame.K_ESCAPE]:
        lib.sound.playBgm(lib.sound.BGM.TITLE)
        lib.replay.stopRecording()
        lib.globals.nextScene = lib.scene.title

def draw(surface: pygame.Surface):
    lib.scroll_map.blitBackground(lib.globals.stgSurface)
    # lib.globals.stgSurface.fill((255, 0, 255))

    for g in lib.globals.stgGroups:
        g.draw(lib.globals.stgSurface)

    if os.environ.get('STRIKER_DEBUG_HITBOX_DISPLAY'):
        lib.debug.hitboxDisplay()

    if lib.globals.config['scale2x']:
        pygame.transform.scale2x(lib.globals.stgSurface, lib.globals.stgSurface2x)
    else:
        pygame.transform.scale(lib.globals.stgSurface, (768, 896), lib.globals.stgSurface2x)

    lib.stg_overlay.update()
    lib.stg_overlay.draw(lib.globals.stgSurface2x)

    surface.blits((
        (lib.textures.STGBACKGROUND['left'], (0, 0)),
        (lib.textures.STGBACKGROUND['right'], (800, 0)),
        (lib.textures.STGBACKGROUND['top'], (32, 0)),
        (lib.textures.STGBACKGROUND['bottom'], (32, 928)),
        (lib.globals.stgSurface2x, (32, 32)),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI[f'text-difficulty-{lib.globals.difficultyType}'], 1040, 24, 8),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-high-score'], 832, 96, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-score'], 832, 156, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-life-remain'], 832, 246, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-hyper-remain'], 832, 306, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-max-getpoint'], 832, 396, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-graze'], 832, 456, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-bullet-count'], 832, 546, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['bar-border'], 832, 596, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-boss-status'], 832, 776, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['bar-border'], 832, 826, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['text-time-countdown'], 832, 661, 4),
        lib.utils.getBlitWithOrigin(lib.textures.STGUI['bar-border'], 832, 711, 4),
    ))

    surface.blits(tuple(
        lib.utils.getBlitWithOrigin(lib.font.FONT_STGUI.render(text), posX, posY, 6)
        for text, (posX, posY) in (
            ('{:,}'.format(
                lib.globals.savedata[f'highscore-{lib.globals.optionType}-{lib.globals.difficultyType}']
                if lib.globals.savedata[f'highscore-{lib.globals.optionType}-{lib.globals.difficultyType}'] != lib.globals.score else
                lib.globals.scoreDisplay
            ), (1244, 96)),
            (f'#       {lib.globals.continueCount}' if lib.globals.continueCount else f'{lib.globals.scoreDisplay:,}', (1244, 156)),
            (f'{lib.globals.maxGetPoint:,}', (1244, 396)),
            (f'{lib.globals.grazeCount:,}', (1244, 456)),
            (str(len(lib.globals.groupEnemyBullet)), (1244, 546)),
            (
                '{0}/{1}'.format(
                    lib.utils.clamp(
                        lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
                        0,
                        lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                    ),
                    lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                ) if lib.globals.groupBoss.sprite else '',
                (1244, 876),
            ),
        )
    ))
    surface.blit(*lib.utils.getBlitWithOrigin(
        lib.font.FONT_STGUI.render(f'* {lib.globals.bossRemain}' if lib.globals.groupBoss.sprite else ''),
        832, 876,
        4,
    ))

    surface.blits(tuple(
        lib.utils.getBlitWithOrigin(
            lib.textures.STGUI['life-1' if x + lib.globals.lifeNum >= lib.constants.LIMIT_LIFENUM else 'life-0'],
            1244 - 32 * x, 246,
            6,
        )
        for x in range(lib.constants.LIMIT_LIFENUM)
    ))
    if lib.globals.groupPlayer.sprite.hyperRemain:
        surface.blit(*lib.utils.getBlitWithOrigin(
            lib.font.FONT_STGUI.render(str(lib.utils.frameToSeconds(lib.globals.groupPlayer.sprite.hyperRemain))),
            1244, 306,
            6,
        ))
    else:
        surface.blits(tuple(
            lib.utils.getBlitWithOrigin(
                lib.textures.STGUI['hyper-1' if x + lib.globals.hyperNum >= lib.constants.LIMIT_HYPERNUM else 'hyper-0'],
                1244 - 32 * x, 306,
                6,
            )
            for x in range(lib.constants.LIMIT_HYPERNUM)
        ))

    barOffset = lib.globals.groupPlayer.sprite.frameCounter * 4
    for bar, (posX, posY) in (
        (lib.textures.STGUI['bar-bullet-count'], (840, 584)),
        (lib.textures.STGUI['bar-time-countdown'], (840, 699)),
        (lib.textures.STGUI['bar-boss-status'], (840, 814)),
    ):
        w = bar.get_width()
        h = bar.get_height()
        b = barOffset % w
        surface.blits((
            (bar.subsurface((0, 0, w - b, h)), (posX + b, posY)),
            (bar.subsurface((w - b, 0, b, h)), (posX, posY)),
        ))
    w = int((1 - lib.utils.clamp(len(lib.globals.groupEnemyBullet), 0, 512) / 512) * 400)
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        (1240 - w, 584, w, 24),
    )
    if lib.globals.groupBoss.sprite:
        w = int((1 - lib.utils.clamp(
            lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
            0, lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
        ) / ((lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin) or 1)) * 400)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (1240 - w, 814, w, 24),
        )
        surface.blit(*lib.utils.getBlitWithOrigin(
            lib.textures.STGUI['enemy-marker'],
            lib.globals.groupBoss.sprite.position.x * 2 + 32, 947,
            5,
        ))
    else:
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (840, 814, 400, 24),
        )
    if lib.globals.timeCountdown is not None:
        surface.blit(*lib.utils.getBlitWithOrigin(
            lib.font.FONT_STGUI.render(str(lib.utils.frameToSeconds(lib.utils.clamp(lib.globals.timeCountdown, 0, lib.globals.timeCountdownMax)))),
            1244, 661,
            6,
        ))
        w = int((1 - lib.utils.clamp(lib.globals.timeCountdown / lib.globals.timeCountdownMax, 0, 1)) * 400)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (1240 - w, 699, w, 24),
        )
    else:
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (840, 699, 400, 24),
        )
    if not lib.globals.replayRecording:
        surface.blit(*lib.utils.getBlitWithOrigin(
            lib.textures.STGUI['text-replay'],
            1040, 920,
            5,
        ))
