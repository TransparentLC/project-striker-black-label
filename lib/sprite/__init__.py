import dataclasses
import typing
import pygame

EmptyTexture = pygame.Surface((1, 1))
EmptyTextureRect = EmptyTexture.get_rect()

@dataclasses.dataclass
class Hitbox:
    offset: pygame.Vector2
    size: float

class Sprite(pygame.sprite.Sprite):
    textures: typing.Sequence[pygame.Surface]
    texturesRotated: typing.Optional[typing.Sequence[pygame.Surface]]
    position: pygame.Vector2
    angle: float = 0
    frameCounter: int = 0
    interval: int = 1
    freeze: bool = False
    speed: pygame.Vector2
    boundary: pygame.Rect
    hitbox: list[Hitbox]
    hitboxAbsoluteCached: typing.Optional[tuple[Hitbox]]

    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.hitboxAbsoluteCached = None

    def update(self) -> None:
        self.hitboxAbsoluteCached = None
        if not self.freeze:
            self.position += self.speed
        if hasattr(self, 'texturesRotated') and self.texturesRotated:
            self.image = self.texturesRotated[(self.frameCounter // self.interval) % len(self.texturesRotated)]
        elif hasattr(self, 'textures') and self.textures:
            self.image = pygame.transform.rotate(
                self.textures[(self.frameCounter // self.interval) % len(self.textures)],
                self.angle,
            )
        else:
            self.image = EmptyTexture
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.frameCounter += 1

    @property
    def outOfBoundary(self):
        return not self.boundary.collidepoint(self.position)

    @property
    def hitboxAbsolute(self) -> typing.Sequence[Hitbox]:
        if not self.hitboxAbsoluteCached:
            self.hitboxAbsoluteCached = tuple(Hitbox(h.offset.rotate(-self.angle) + self.position, h.size) for h in self.hitbox)
        return self.hitboxAbsoluteCached
