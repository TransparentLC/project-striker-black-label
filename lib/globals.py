import collections
import io
import itertools
import json
import os
import pygame
import random
import typing

from jsonschema import Draft7Validator
from jsonschema import ValidationError
from jsonschema import validators

import lib.constants
import lib.utils

# https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
def extendValidatorWithDefault(validator_class: Draft7Validator) -> Draft7Validator:
    def setDefaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if 'default' in subschema:
                instance.setdefault(property, subschema['default'])
        for error in validator_class.VALIDATORS['properties'](validator, properties, instance, schema):
            yield error
    return validators.extend(validator_class, {'properties': setDefaults})
Draft7ValidatorWithDefault = extendValidatorWithDefault(Draft7Validator)

if not os.path.exists(lib.constants.DATA_DIR):
    os.mkdir(lib.constants.DATA_DIR)
if not os.path.exists(lib.constants.REPLAY_DIR):
    os.mkdir(lib.constants.REPLAY_DIR)
config: dict = None
if os.path.exists(lib.constants.PATH_CONFIG):
    with open(lib.constants.PATH_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
try:
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_CONFIG).validate(config)
except ValidationError:
    config = dict()
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_CONFIG).validate(config)

savedata: dict = None
if os.path.exists(lib.constants.PATH_SAVEDATA):
    with open(lib.constants.PATH_SAVEDATA, 'r', encoding='utf-8') as f:
        savedata = json.load(f)
try:
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_SAVEDATA).validate(savedata)
except ValidationError:
    savedata = {
        **{
            f'highscore-{option}-{difficulty}': lib.constants.DEFAULT_HIGHSCORE
            for option, difficulty in itertools.product(
                range(len(lib.constants.OPTION_TYPE_NAME)),
                range(len(lib.constants.DIFFICULTY_NAME)),
            )
        },
        **{
            f'phase-{name}-{phase}-{option}-{difficulty}': 0
            for name, phase, option, difficulty in itertools.product(
                ('encounter', 'reward'),
                range(len(lib.constants.PHASE_NAME)),
                range(len(lib.constants.OPTION_TYPE_NAME)),
                range(len(lib.constants.DIFFICULTY_NAME)),
            )
        },
    }
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_SAVEDATA).validate(savedata)

pygame.display.set_icon(pygame.image.load(lib.utils.getResourceHandler('assets/icon.webp')))
pygame.display.set_caption(lib.constants.TITLE)
screen = pygame.display.set_mode(
    (1280, 960),
    (pygame.SCALED if config['windowed'] else pygame.FULLSCREEN)
)
clock = pygame.time.Clock()
keys: typing.Sequence[bool] = None
keysLastFrame: typing.Sequence[bool] = None
currentScene = None
nextScene = None

stgSurface = pygame.Surface((384, 448))
stgSurface2x = pygame.Surface((768, 896))
stageFunction: typing.Generator[int, None, None] = None
stageFunctionWait = 0
stgRandomSeed: bytes = None
stgRandom = random.Random()
replayKeyStream: io.BytesIO = None
replayRecording = False

backgroundScrollSpeed = 1.5
backgroundScrollOffset = 0
backgroundMaskAlpha = 0
backgroundMaskChangeSpeed = 0
backgroundSurfaces: typing.Deque[pygame.Surface] = collections.deque()

score = 0
scoreDisplay = 0
scoreLastFrame = 0
grazeCount = 0
maxGetPoint = 0
phaseIndex = 0
phaseBonus = 0
phaseBonusDrop = 0
phaseBonusCount = 0
clearBulletCenter: pygame.Vector2 = None
clearBulletRadius = 0
clearBulletBonus = False
lifeNum = 0
hyperNum = 0
difficultyType = 0
optionType = 0
timeCountdown: int = None
timeCountdownMax = 0
missedCount = 0
hyperUsedCount = 0
continueCount = 0
continueRemain = 0
continueEnabled = True
allCleared = False

bossRemain = 0
bossHitpointRangeMin = 0
bossHitpointRangeMax = 0

groupItem = pygame.sprite.Group()
groupPlayer = pygame.sprite.GroupSingle()
groupPlayerOption = pygame.sprite.Group()
groupPlayerBullet = pygame.sprite.Group()
groupEnemy = pygame.sprite.Group()
groupEnemyBullet = pygame.sprite.Group()
groupBoss = pygame.sprite.GroupSingle()
groupParticle = pygame.sprite.Group()
stgGroups = (
    groupPlayer,
    groupPlayerOption,
    groupEnemy,
    groupPlayerBullet,
    groupEnemyBullet,
    groupItem,
    groupParticle,
)
