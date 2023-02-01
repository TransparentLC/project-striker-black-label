import itertools
import os
import pygame
import sys

import lib.native_utils
import lib.utils

if os.path.exists('build-info.txt'):
    with open('build-info.txt', 'r', encoding='utf-8') as f:
        BUILD_INFO = f.read().splitlines()
else:
    BUILD_INFO = None

with lib.utils.getResourceHandler('scriptfiles/phase-name.txt') as f:
    PHASE_NAME = f.read().decode('utf-8').splitlines()
OPTION_TYPE_NAME = (
    'Type-A 诱导攻击型',
    'Type-A 广角范围型',
    'Type-B 水平偏转型',
    'Type-B 前方集中型',
)
DIFFICULTY_NAME = (
    'Novice',
    'Original',
    'Extreme',
)

TITLE = 'Striker Black Label'
DATA_DIR = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.split(sys.argv[0])[0], 'savedata')
REPLAY_DIR = os.path.join(DATA_DIR, 'replay')
PATH_CONFIG = os.path.join(DATA_DIR, 'config.json')
PATH_SAVEDATA = os.path.join(DATA_DIR, 'savedata.json')

DEFAULT_HIGHSCORE = 50000000

# {
#     "type": "object",
#     "properties": {
#         "windowed": {
#             "type": "boolean",
#             "default": false
#         },
#         "bgm": {
#             "type": "boolean",
#             "default": true
#         },
#         "scale2x": {
#             "type": "boolean",
#             "default": false
#         },
#         "inputDisplay": {
#             "type": "boolean",
#             "default": false
#         }
#     }
# }
SCHEMA_CONFIG = {
    "type": "object",
    "properties": {
        "windowed": {
            "type": "boolean",
            "default": False,
        },
        "bgm": {
            "type": "boolean",
            "default": True,
        },
        "scale2x": {
            "type": "boolean",
            "default": False,
        },
        "inputDisplay": {
            "type": "boolean",
            "default": False,
        }
    }
}

# {
#     "type": "object",
#     "properties": {
#         "key-option-difficulty": {
#             "type": "integer",
#             "default": "0",
#             "minimum": 0
#         }
#     }
# }
SCHEMA_SAVEDATA = {
    "type": "object",
    "properties": {
        **{
            f'highscore-{option}-{difficulty}': {
                "type": "integer",
                "default": DEFAULT_HIGHSCORE,
                "minimum": 0,
            } for option, difficulty in itertools.product(
                range(len(OPTION_TYPE_NAME)),
                range(len(DIFFICULTY_NAME)),
            )
        },
        **{
            f'phase-{name}-{phase}-{option}-{difficulty}': {
                "type": "integer",
                "default": 0,
                "minimum": 0,
            } for name, phase, option, difficulty in itertools.product(
                ('encounter', 'reward'),
                range(len(PHASE_NAME)),
                range(len(OPTION_TYPE_NAME)),
                range(len(DIFFICULTY_NAME)),
            )
        },
    }
}

DEBUG_INPUT_DISPLAY_PRESSED = pygame.Color(255, 255, 0)
DEBUG_INPUT_DISPLAY_NOTPRESSED = pygame.Color(127, 127, 127)
DEBUG_HITBOX = pygame.Color(255, 255, 0)

PLAYER_A_SPEED_NORMAL = 4
PLAYER_A_SPEED_SLOW = 1.8
PLAYER_B_SPEED_NORMAL = 5
PLAYER_B_SPEED_SLOW = 2.5

ITEM_GAIN_RANGE = 6
ITEM_MAGNET_RANGE = 50
ITEM_GET_BORDER = 112
GRAZE_RANGE = 30
HYPER_TIME = 480
HYPER_INVINCIBLE_TIME = 180

INITIAL_MAXGETPOINT = 100000
INITIAL_LIFENUM = 2
INITIAL_HYPERNUM = 3
LIMIT_LIFENUM = 7
LIMIT_HYPERNUM = 7
