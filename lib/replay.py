import hmac
import io
import lzma
import os
import pygame
import struct
import time

import lib.constants
import lib.globals

REPLAY_HEADER_STRUCT = struct.Struct('<4sIQ8s8sQBBBBI')
REPLAY_HEADER_SIZE = REPLAY_HEADER_STRUCT.size
REPLAY_VERSION = 0x00000010
REPLAY_HMAC_KEY = b'D4yd23aM_C4F3'
KEY_MAPPING = {
    1 << 0: pygame.K_UP,
    1 << 1: pygame.K_DOWN,
    1 << 2: pygame.K_LEFT,
    1 << 3: pygame.K_RIGHT,
    1 << 4: pygame.K_LSHIFT,
    1 << 5: pygame.K_z,
    1 << 6: pygame.K_x,
    1 << 7: pygame.K_c, # Unused
}

# ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
# ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
# ０１２３４５６７８９＋－＝．，！？＠：；［］（）＿／｛｝｜～＾＃＄％＆＊
replayNameChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=.,!?@:;[]()_/{}|~^#$%&* '
replayNameCharsAscii = tuple(ord(x) for x in replayNameChars)
replayNameCharsHalfWidth = {ord(x): x for x in replayNameChars}
replayNameCharsFullWidth = {ord(x): chr(ord(x) + 0xFEE0) for x in replayNameChars}
replayNameCharsFullWidth[ord(' ')] = '　'

def readKeys() -> int:
    keyByte = 0
    for bit, key in KEY_MAPPING.items():
        if lib.globals.keys[key]:
            keyByte |= bit
    return keyByte

def setKeys(keyByte: int):
    for bit, key in KEY_MAPPING.items():
        lib.globals.keys[key] = bool(keyByte & bit)

def startRecording():
    lib.globals.replayKeyStream = io.BytesIO()
    lib.globals.replayRecording = True

def stopRecording():
    lib.globals.replayRecording = False

def saveReplay(name: bytes):
    header = REPLAY_HEADER_STRUCT.pack(
        b'RPLY',
        REPLAY_VERSION,
        int(time.time()),
        name[:8],
        lib.globals.stgRandomSeed,
        lib.globals.score,
        lib.globals.optionType | (lib.globals.difficultyType << 2),
        lib.globals.missedCount,
        lib.globals.hyperUsedCount,
        lib.globals.phaseBonusCount,
        0,
    )
    replayData = lib.globals.replayKeyStream.getvalue()
    replayIndex = 0
    while True:
        replayPath = f'{lib.constants.REPLAY_DIR}/{replayIndex:04d}.rep'
        if not os.path.exists(replayPath):
            break
        replayIndex += 1
    with open(replayPath, 'wb') as f:
        f.write(header)
        f.write(hmac.digest(REPLAY_HMAC_KEY, header + replayData, 'sha256'))
        f.write(lzma.compress(replayData, format=lzma.FORMAT_ALONE, preset=9))

def parseReplay(path: str) -> tuple[bytes, int, int, bytes, bytes, int, int, int, int, int, int]:
    with open(path, 'rb') as f:
        return REPLAY_HEADER_STRUCT.unpack(f.read(REPLAY_HEADER_SIZE))

def loadReplay(path: str) -> bool:
    with open(path, 'rb') as f:
        header = f.read(REPLAY_HEADER_SIZE)
        checksum = f.read(32)
        replayData = lzma.decompress(f.read(), format=lzma.FORMAT_ALONE)
    if not hmac.compare_digest(hmac.digest(REPLAY_HMAC_KEY, header + replayData, 'sha256'), checksum):
        return False
    parsedHeader = REPLAY_HEADER_STRUCT.unpack(header)
    lib.globals.stgRandomSeed = parsedHeader[4]
    lib.globals.optionType = parsedHeader[6] & 0b00000011
    lib.globals.difficultyType = (parsedHeader[6] & 0b00001100) >> 2
    lib.globals.replayKeyStream = io.BytesIO(replayData)
    return True

def verifyReplay(path: str) -> bool:
    hmacCtx = hmac.new(REPLAY_HMAC_KEY, digestmod='sha256')
    with open(path, 'rb') as f:
        hmacCtx.update(f.read(REPLAY_HEADER_SIZE))
        checksum = f.read(32)
        hmacCtx.update(lzma.decompress(f.read(), format=lzma.FORMAT_ALONE))
    return hmac.compare_digest(hmacCtx.digest(), checksum)
