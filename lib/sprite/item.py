import pygame

import lib.constants
import lib.font
import lib.globals
import lib.sound
import lib.sprite
import lib.sprite.player
import lib.stg_overlay
import lib.textures
import lib.utils

itemBoundary = pygame.Rect(-20, -20, 384 + 20, 448 + 20)

class ItemEffect(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, image: pygame.Surface) -> None:
        super().__init__(lib.globals.groupParticle)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = position
        self.frameCounter = 0

    def update(self) -> None:
        self.frameCounter += 1
        self.rect.centery -= .025
        self.image.set_alpha((60 - self.frameCounter) / 60 * 255)
        if self.frameCounter > 60:
            self.kill()

class Item(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, texture: pygame.Surface) -> None:
        super().__init__(lib.globals.groupItem)
        self.position = pygame.Vector2(position)
        self.speed = pygame.Vector2(0, -.75)
        self.textures = (texture,)
        self.magnetNear = False
        self.magnetBorder = False
        self.image = lib.sprite.EmptyTexture
        self.rect = lib.sprite.EmptyTextureRect
        self.boundary = itemBoundary

    def gain(self):
        pass

    def update(self) -> None:
        super().update()

        if self.outOfBoundary:
            self.kill()

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if s.deathWait and (self.magnetNear or self.magnetBorder):
            self.magnetNear = False
            self.magnetBorder = False
            self.speed.update(0, 0)
        self.speed.y = min(self.speed.y + .015, 1.5)
        if not s.deathWait:
            if s.position.y < lib.constants.ITEM_GET_BORDER:
                self.magnetBorder = True

            distance = (s.position - self.position).length()
            if distance < lib.constants.ITEM_GAIN_RANGE:
                self.gain()
                self.kill()
                return
            elif not self.magnetBorder and distance < lib.constants.ITEM_MAGNET_RANGE:
                self.magnetNear = True

            if self.magnetNear or self.magnetBorder:
                delta = s.position - self.position
                if delta.length_squared() >= 36:
                    delta.normalize_ip()
                    delta *= 9 if self.magnetBorder else 6
                delta.y -= .015
                self.speed.update(delta)

class Point(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, lib.textures.ITEM['item-point'])

    def gain(self):
        # 25%-60% 100%
        if self.magnetBorder:
            point = lib.globals.maxGetPoint
            number = lib.font.FONT_ITEM_HIGHLIGHT
        else:
            point = int(lib.utils.linearInterpolation(
                (self.position.y - lib.constants.ITEM_GET_BORDER) / (448 - lib.constants.ITEM_GET_BORDER),
                .6,
                .25,
            ) * lib.globals.maxGetPoint)
            number = lib.font.FONT_ITEM

        lib.globals.score += point
        lib.globals.maxGetPoint += (8, 12, 16)[lib.globals.difficultyType]
        ItemEffect(self.position, number.render(str(point)))
        lib.sound.SFX.GET_POINT.play()

class PointBullet(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, lib.textures.ITEM['item-point-bullet'])
        self.speed.y = -.5

    def update(self) -> None:
        if self.frameCounter == 30:
            self.magnetBorder = True
        super().update()

    def gain(self):
        lib.globals.score += lib.globals.maxGetPoint >> 5
        lib.globals.maxGetPoint += (32, 48, 64)[lib.globals.difficultyType]
        lib.sound.SFX.GET_POINT.play()

class PointClear(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, lib.textures.ITEM['item-point-clear'])
        self.speed.y = -.5

    def update(self) -> None:
        if self.frameCounter == 30:
            self.magnetNear = True
        super().update()

    def gain(self):
        lib.globals.score += len(lib.globals.groupEnemyBullet) << 4
        lib.sound.SFX.GET_POINT.play()

class LifeExtend(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, lib.textures.ITEM['item-life-extend'])

    def gain(self):
        if lib.globals.lifeNum < lib.constants.LIMIT_LIFENUM:
            lib.globals.lifeNum += 1
        lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.LIFE_REMAIN] = 240
        ItemEffect(self.position, lib.textures.ITEM['item-effect-highlight-life-extend'])
        lib.sound.SFX.EXTEND_LIFE.play()

class HyperExtend(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, lib.textures.ITEM['item-hyper-extend'])

    def gain(self):
        if lib.globals.hyperNum < lib.constants.LIMIT_HYPERNUM:
            lib.globals.hyperNum += 1
        lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.HYPER_REMAIN] = 240
        ItemEffect(self.position, lib.textures.ITEM['item-effect-highlight-hyper-extend'])
        lib.sound.SFX.EXTEND_HYPER.play()
