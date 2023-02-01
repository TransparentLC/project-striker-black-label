import enum
import pygame
import os
import typing

import lib.globals
import lib.replay
import lib.scene.replay
import lib.scene.result
import lib.sound
import lib.sprite
import lib.stg_overlay
import lib.utils

class Opcode(enum.IntEnum):
    NOOP = enum.auto()
    DEBUGGER = enum.auto()
    HALT = enum.auto()
    WAIT = enum.auto()

    JUMP = enum.auto()
    JUMP_E = enum.auto()
    JUMP_NE = enum.auto()
    JUMP_L = enum.auto()
    JUMP_LE = enum.auto()
    JUMP_G = enum.auto()
    JUMP_GE = enum.auto()
    JUMP_BOSS = enum.auto()
    JUMP_NOBOSS = enum.auto()

    STORE = enum.auto()
    RANDOM_INT = enum.auto()
    RANDOM_FLOAT = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    FDIV = enum.auto()

    SET_SCROLL_SPEED = enum.auto()
    SET_MASK_ALPHA = enum.auto()
    SET_MASK_SPEED = enum.auto()
    LOAD_STAGE = enum.auto()
    SPAWN = enum.auto()
    BGM = enum.auto()
    BOSS_WARNING = enum.auto()
    SET_CLEARED = enum.auto()
    DISABLE_CONTINUE = enum.auto()
    SHOW_RESULT = enum.auto()

    # = enum.auto()

enemyScriptCache: dict[str, str] = {}

class Engine:
    @staticmethod
    def parseLine(line: str) -> tuple[tuple[Opcode, list[typing.Union[int, float, str]]], typing.Optional[str]]:
        params = line.split()
        if not params:
            return (None, None)
        opcode = params.pop(0)
        if opcode == '#':
            return (None, None)
        opcode = Opcode[opcode]

        for index, value in enumerate(params):
            if value == '#':
                return ((opcode, params[:index]), None)
            elif value == '@':
                return ((opcode, params[:index]), params[index + 1])
            try:
                params[index] = int(value)
            except ValueError:
                try:
                    params[index] = float(value)
                except ValueError:
                    pass
        return ((opcode, params), None)

    @staticmethod
    def parseScript(script: str) -> typing.Sequence[tuple[Opcode, typing.Sequence[typing.Union[int, float, str]]]]:
        result: list[tuple[Opcode, list[typing.Union[int, float, str]]]] = []
        lineTags: dict[str, int] = {}
        lineCounter = 0
        for line in script.splitlines():
            parsed, tag = Engine.parseLine(line)
            if tag:
                lineTags[tag] = lineCounter
            if parsed:
                result.append(parsed)
                lineCounter += 1
        for i, r in enumerate(result):
            for j, p in enumerate(r[1]):
                if isinstance(p, str) and p[0] == '@':
                    r[1][j] = lineTags[p[1:]] - i
        # for r in result:
        #     print(r)
        return result

    def __init__(self, script: str) -> None:
        self.instruction = Engine.parseScript(script)
        self.pointer = 0
        self.wait = 0
        self.halted = False
        self.vars: list[typing.Union[int, float, str]] = list(None for x in range(8))

    def applyParamsReplacement(self, params: typing.Sequence[typing.Union[int, float, str]]) -> None:
        result = []
        for value in params:
            isVar = False
            if isinstance(value, str) and value.startswith('%VAR_'):
                for i in range(8):
                    if value == f'%VAR_{i}%':
                        result.append(self.vars[i])
                        isVar = True
                        break
            if not isVar:
                if value == '%PLAYER_X%':
                    result.append(lib.globals.groupPlayer.sprite.position.x)
                elif value == '%PLAYER_Y%':
                    result.append(lib.globals.groupPlayer.sprite.position.y)
                elif value == '%CONTINUE_COUNT%':
                    result.append(lib.globals.continueCount)
                else:
                    result.append(value)
        return result

    def update(self):
        if self.wait > 0:
            self.wait -= 1

        while not self.halted and not self.wait:
            opcode, params = self.instruction[self.pointer]
            params = self.applyParamsReplacement(params)
            # print(opcode, params, self.vars)
            self.pointer += 1
            self.executeOpcode(opcode, params)

    def executeOpcode(self, opcode: Opcode, params: typing.Sequence[typing.Union[int, float, str]]):
        if opcode == Opcode.NOOP:
            pass
        elif opcode == Opcode.DEBUGGER:
            print('Debugger triggered from line', self.pointer, 'at frame', self.context.frameCounter)
        elif opcode == Opcode.WAIT:
            params: tuple[int] = params
            waitTime, = params

            self.wait = waitTime
        elif opcode == Opcode.HALT:
            self.halted = True
        elif opcode == Opcode.JUMP:
            params: tuple[int] = params
            offset, = params

            self.pointer += offset - 1
        elif opcode == Opcode.JUMP_E:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a == b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_NE:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a != b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_L:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a < b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_LE:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a <= b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_G:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a > b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_GE:
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a >= b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_BOSS:
            params: tuple[int] = params
            offset, = params

            if lib.globals.groupBoss.sprite:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_NOBOSS:
            params: tuple[int] = params
            offset, = params

            if not lib.globals.groupBoss.sprite:
                self.pointer += offset - 1
        elif opcode == Opcode.STORE:
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] = value
        elif opcode == Opcode.RANDOM_INT:
            params: tuple[int, int, int] = params
            address, minValue, maxValue = params

            self.vars[address] = lib.globals.stgRandom.randint(minValue, maxValue)
        elif opcode == Opcode.RANDOM_FLOAT:
            params: tuple[int, float, float] = params
            address, minValue, maxValue = params

            self.vars[address] = minValue + (maxValue - minValue) * lib.globals.stgRandom.random()
        elif opcode == Opcode.INC:
            params: tuple[int] = params
            address, = params

            self.vars[address] += 1
        elif opcode == Opcode.DEC:
            params: tuple[int] = params
            address, = params

            self.vars[address] -= 1
        elif opcode == Opcode.ADD:
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] += value
        elif opcode == Opcode.SUB:
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] -= value
        elif opcode == Opcode.MUL:
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] *= value
        elif opcode == Opcode.DIV:
            params: tuple[int, int] = params
            address, value = params

            self.vars[address] = int(self.vars[address]) // int(value)
        elif opcode == Opcode.MOD:
            params: tuple[int, int] = params
            address, value = params

            self.vars[address] = int(self.vars[address]) % int(value)
        elif opcode == Opcode.FDIV:
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] /= value
        elif opcode == Opcode.SET_SCROLL_SPEED:
            params: tuple[float] = params
            speed, = params

            lib.globals.backgroundScrollSpeed = speed
        elif opcode == Opcode.SET_MASK_ALPHA:
            params: tuple[int] = params
            alpha, = params

            lib.globals.backgroundMaskAlpha = alpha
        elif opcode == Opcode.SET_MASK_SPEED:
            params: tuple[int] = params
            speed, = params

            lib.globals.backgroundMaskChangeSpeed = speed
        elif opcode == Opcode.LOAD_STAGE:
            params: tuple[str] = params
            scriptFile, = params

            self.halted = True
            with lib.utils.getResourceHandler(scriptFile) as f:
                lib.globals.stageEngine = Engine(f.read().decode())
        elif opcode == Opcode.SPAWN:
            # (-30, -80) (424, 478)
            params: tuple[float, float, float, str] = params
            x, y, angle, scriptFile = params

            enemy = lib.sprite.enemy.Enemy()
            enemy.position.update(x, y)
            enemy.angle = angle
            if scriptFile in enemyScriptCache and not os.environ.get('STRIKER_DEBUG_DISABLE_ENEMY_CACHE'):
                script = enemyScriptCache[scriptFile]
            else:
                with lib.utils.getResourceHandler(scriptFile) as f:
                    script = f.read().decode('utf-8')
            enemy.setScript(script)
        elif opcode == Opcode.BGM:
            params: tuple[str] = params
            bgmName, = params

            lib.sound.playBgm(bgmName)
        elif opcode == Opcode.BOSS_WARNING:
            lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.WARNING_REMAIN] = 330
            lib.sound.SFX.BOSS_ALERT.play(loops=1)
        elif opcode == Opcode.SET_CLEARED:
            lib.globals.allCleared = True
            lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.CLEAR_REMAIN] = 240
            lib.sound.SFX.EXTEND_LIFE.play()
        elif opcode == Opcode.DISABLE_CONTINUE:
            lib.globals.continueEnabled = False
        elif opcode == Opcode.SHOW_RESULT:
            if lib.globals.replayRecording:
                pygame.mixer.music.stop()
                lib.replay.stopRecording()
                lib.globals.nextScene = lib.scene.result
            else:
                lib.sound.playBgm(lib.sound.BGM.TITLE)
                lib.globals.nextScene = lib.scene.replay

        # elif opcode == Opcode.:
        #     params: tuple[] = params
        #      = params
        else:
            print('Unknown opcode:', opcode)
