import pygame

import lib.bullet
import lib.constants
import lib.globals
import lib.sprite.enemy
import lib.sprite.player

def hitboxDisplay():
    for g in (
        lib.globals.groupPlayerBullet,
        lib.globals.groupEnemyBullet,
    ):
        for s in g:
            s: lib.bullet.Bullet
            pygame.draw.circle(
                lib.globals.stgSurface,
                lib.constants.DEBUG_HITBOX,
                s.position,
                s.size,
                1
            )

    s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
    for h in s.hitboxAbsolute:
        pygame.draw.circle(
            lib.globals.stgSurface,
            lib.constants.DEBUG_HITBOX,
            h.offset,
            h.size,
            1
        )
        pygame.draw.circle(
            lib.globals.stgSurface,
            lib.constants.DEBUG_HITBOX,
            h.offset,
            h.size + lib.constants.GRAZE_RANGE,
            1
        )

    for s in lib.globals.groupEnemy:
        s: lib.sprite.enemy.Enemy
        for h in s.hitboxAbsolute:
            pygame.draw.circle(
                lib.globals.stgSurface,
                lib.constants.DEBUG_HITBOX,
                h.offset,
                h.size,
                1
            )
