import collections
import enum
import pygame
import typing

import lib.bullet.enemy_bullet
import lib.globals
import lib.sprite
import lib.sprite.debris
import lib.sprite.enemy
import lib.sprite.explosion
import lib.sprite.item
import lib.sound
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
    REGISTER_DEATH = enum.auto()
    REGISTER_BOSSBREAK = enum.auto()

    STORE = enum.auto()
    RANDOM_INT = enum.auto()
    RANDOM_FLOAT = enum.auto()
    CALC_OFFSET = enum.auto()
    CALC_DIRECTION = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    FDIV = enum.auto()

    SET_POSITION = enum.auto()
    SET_POSITION_RELATIVE = enum.auto()
    SET_TEXTURE = enum.auto()
    SET_HITPOINT = enum.auto()
    SET_MAXGETPOINTADD = enum.auto()
    SET_INVINCIBLE = enum.auto()
    SET_EXPLOSION = enum.auto()
    SET_DEBRIS = enum.auto()
    SET_HITBOX = enum.auto()
    SET_SPEED = enum.auto()
    SET_ANGLE = enum.auto()
    SET_ANGLE_RELATIVE = enum.auto()
    SET_EXPLODE_SFX = enum.auto()
    SET_POINTITEM = enum.auto()

    SET_BOSS = enum.auto()
    SET_BOSS_REMAIN = enum.auto()
    SET_BOSS_HPRANGE = enum.auto()
    SET_PHASE_NAME = enum.auto()
    SET_PHASE_BONUS = enum.auto()

    MOVE = enum.auto()
    MOVE_RELATIVE = enum.auto()
    MOVE_RANDOM = enum.auto()
    MOVE_CLEAR = enum.auto()

    SHOOT = enum.auto()
    SHOOT_AIMING = enum.auto()
    SHOOT_MULTIWAY = enum.auto()
    SHOOT_AIMING_MULTIWAY = enum.auto()

    SFX = enum.auto()

    CLEAR_BULLET = enum.auto()
    BONUS_BULLET = enum.auto()
    BONUS_PHASE = enum.auto()
    DROP_POINTITEM = enum.auto()
    EXTEND_LIFE = enum.auto()
    EXTEND_HYPER = enum.auto()

    PRESET_ENEMY_A = enum.auto()
    PRESET_ENEMY_B = enum.auto()
    PRESET_ENEMY_C = enum.auto()
    PRESET_ENEMY_D = enum.auto()
    PRESET_ENEMY_E = enum.auto()

    # = enum.auto()

EnemyTexturesTable = {
    'ENEMY_A': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/enemy-a-{i}.webp')).convert_alpha() for i in range(2)),
    'ENEMY_B': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/enemy-b-{i}.webp')).convert_alpha() for i in range(2)),
    'ENEMY_C': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/enemy-c-{i}.webp')).convert_alpha() for i in range(2)),
    'ENEMY_D': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/enemy-d-{i}.webp')).convert_alpha() for i in range(2)),
    'ENEMY_E': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/enemy-e-{i}.webp')).convert_alpha() for i in range(2)),
    'BOSS_A': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/boss-a-{i}.webp')).convert_alpha() for i in range(2)),
    'BOSS_B': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/boss-b-{i}.webp')).convert_alpha() for i in range(2)),
    'BOSS_C': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/boss-c-{i}.webp')).convert_alpha() for i in range(2)),
    'BOSS_D': tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/boss-d-{i}.webp')).convert_alpha() for i in range(2)),
}

MoveInterpolationFunctionTable = {
    'LINEAR': lib.utils.linearInterpolation,
    'EASE_IN_QUAD': lib.utils.easeInQuadInterpolation,
    'EASE_OUT_QUAD': lib.utils.easeOutQuadInterpolation,
    'EASE_INOUT_QUAD': lib.utils.easeInOutQuadInterpolation,
    'EASE_IN_CUBIC': lib.utils.easeInCubicInterpolation,
    'EASE_OUT_CUBIC': lib.utils.easeOutCubicInterpolation,
    'EASE_INOUT_CUBIC': lib.utils.easeInOutCubicInterpolation,
}

ExplosionTable = {
    'SMALL_A': lib.sprite.explosion.ExplosionPlaneSmallA,
    'SMALL_B': lib.sprite.explosion.ExplosionPlaneSmallB,
    'MEDIUM_A': lib.sprite.explosion.ExplosionPlaneMediumA,
    'MEDIUM_B': lib.sprite.explosion.ExplosionPlaneMediumB,
    'LARGE': lib.sprite.explosion.ExplosionPlaneLarge,
}

DebrisTable = {
    'DEBRIS_A': lib.sprite.debris.DebrisA,
    'DEBRIS_B': lib.sprite.debris.DebrisB,
}

BulletTextureTable = {
    'TYPE_A': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-a.webp')).convert_alpha(),
    'TYPE_B': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-b.webp')).convert_alpha(),
    'TYPE_C': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-c.webp')).convert_alpha(),
    'TYPE_D': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-d.webp')).convert_alpha(),
    'TYPE_E': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-e.webp')).convert_alpha(),
    'TYPE_A_2X': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-a-2x.webp')).convert_alpha(),
    'TYPE_B_2X': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-b-2x.webp')).convert_alpha(),
    'TYPE_C_2X': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-c-2x.webp')).convert_alpha(),
    'TYPE_D_2X': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-d-2x.webp')).convert_alpha(),
    'TYPE_E_2X': pygame.image.load(lib.utils.getResourceHandler('assets/enemy-bullet-e-2x.webp')).convert_alpha(),
}

BulletSizeTable = {
    'TYPE_A': 2,
    'TYPE_B': 4,
    'TYPE_C': 2.5,
    'TYPE_D': 3,
    'TYPE_E': 5,
    'TYPE_A_2X': 5,
    'TYPE_B_2X': 8,
    'TYPE_C_2X': 5,
    'TYPE_D_2X': 6,
    'TYPE_E_2X': 9,
}

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

    def __init__(self, context: 'lib.sprite.enemy.Enemy', script: str) -> None:
        self.instruction = Engine.parseScript(script)
        self.context = context
        self.pointer = 0
        self.pointerDeath: int = None
        self.pointerRangeBreak: int = None
        self.wait = 0
        self.halted = False
        self.movementTask: tuple[
            pygame.Vector2,
            int,
            typing.Callable[
                [float, pygame.Vector2, pygame.Vector2],
                pygame.Vector2
            ]
        ] = None
        self.movementCounter = 0
        self.movementFrom: pygame.Vector2 = None
        # 只使用append和popleft作为队列使用
        self.movementQueue: typing.Deque[tuple[pygame.Vector2, int]] = collections.deque()
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
                if value == '%HITPOINT%':
                    result.append(self.context.hitpoint)
                elif value == '%FRAMECOUNTER%':
                    result.append(self.context.frameCounter)
                elif value == '%AIM_PLAYER%':
                    result.append(-pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - self.context.position) - 90)
                elif value == '%PLAYER_X%':
                    result.append(lib.globals.groupPlayer.sprite.position.x)
                elif value == '%PLAYER_Y%':
                    result.append(lib.globals.groupPlayer.sprite.position.y)
                elif value == '%ENEMY_X%':
                    result.append(self.context.position.x)
                elif value == '%ENEMY_Y%':
                    result.append(self.context.position.y)
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

        if not self.movementTask and self.movementQueue:
            self.movementCounter = 0
            self.movementFrom = pygame.Vector2(self.context.position)
            self.movementTask = self.movementQueue.popleft()
        if self.movementTask:
            self.movementCounter += 1
            self.context.position.update(
                self.movementTask[2](
                    self.movementCounter / self.movementTask[1],
                    self.movementFrom,
                    self.movementTask[0],
                )
            )
            if self.movementCounter >= self.movementTask[1]:
                self.movementTask = None

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
        elif opcode == Opcode.REGISTER_DEATH:
            params: tuple[int] = params
            offset, = params

            self.pointerDeath = self.pointer + offset - 1
        elif opcode == Opcode.REGISTER_BOSSBREAK:
            params: tuple[int] = params
            offset, = params

            self.pointerRangeBreak = self.pointer + offset - 1
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
        elif opcode == Opcode.CALC_OFFSET:
            params: tuple[int, float, float] = params
            address, x, y = params

            position = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            self.vars[address] = position.x
            self.vars[address + 1] = position.y
        elif opcode == Opcode.CALC_DIRECTION:
            params: tuple[int, float, float, float, float] = params
            address, x1, y1, x2, y2 = params

            self.vars[address] = -pygame.Vector2().angle_to(pygame.Vector2(x2 - x1, y2 - y1)) - 90
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
        elif opcode == Opcode.SET_POSITION:
            params: tuple[float, float] = params
            x, y = params

            self.context.position.update(x, y)
        elif opcode == Opcode.SET_POSITION_RELATIVE:
            params: tuple[float, float] = params
            x, y = params

            self.context.position += pygame.Vector2(x, y)
        elif opcode == Opcode.SET_TEXTURE:
            params: tuple[str] = params
            textures, = params

            self.context.textures = EnemyTexturesTable[textures]
        elif opcode == Opcode.SET_HITPOINT:
            params: tuple[int] = params
            hitpoint, = params

            self.context.hitpoint = hitpoint
        elif opcode == Opcode.SET_MAXGETPOINTADD:
            params: tuple[int] = params
            num, = params

            self.context.maxGetPointAdd = num
        elif opcode == Opcode.SET_INVINCIBLE:
            params: tuple[int] = params
            invincibleRemain, = params

            self.context.invincibleRemain = invincibleRemain
        elif opcode == Opcode.SET_EXPLOSION:
            params: tuple[str] = params
            explosion, = params

            self.context.explosion = ExplosionTable[explosion]
        elif opcode == Opcode.SET_DEBRIS:
            params: tuple[str, float, float, float, float, float, float, int] = params
            debris, x, y, spreadSpeedMin, spreadSpeedMax, rotateSpeedMin, rotateSpeedMax, count = params

            for i in range(count):
                self.context.debris.append((
                    DebrisTable[debris],
                    pygame.Vector2(x, y),
                    spreadSpeedMin, spreadSpeedMax,
                    rotateSpeedMin, rotateSpeedMax,
                ))
        elif opcode == Opcode.SET_HITBOX:
            params: tuple[float, float, float] = params
            x, y, r = params

            self.context.hitbox.append(lib.sprite.Hitbox(pygame.Vector2(x, y), r))
        elif opcode == Opcode.SET_SPEED:
            params: tuple[float] = params
            speed, = params

            self.context.speed.update(pygame.Vector2(0, -speed).rotate(-self.context.angle))
        elif opcode == Opcode.SET_ANGLE:
            params: tuple[float] = params
            angle, = params

            self.context.angle = angle
        elif opcode == Opcode.SET_ANGLE_RELATIVE:
            params: tuple[float] = params
            angle, = params

            self.context.angle += angle
        elif opcode == Opcode.SET_EXPLODE_SFX:
            params: tuple[str] = params
            sfxName, = params

            self.context.explodeSfx = lib.sound.SFX.sfxName
        elif opcode == Opcode.SET_POINTITEM:
            params: tuple[int] = params
            num, = params

            self.context.pointItemNum = num
        elif opcode == Opcode.SET_BOSS:
            lib.globals.groupBoss.sprite = self.context
        elif opcode == Opcode.SET_BOSS_REMAIN:
            params: tuple[int] = params
            remain, = params

            lib.globals.bossRemain = remain
        elif opcode == Opcode.SET_BOSS_HPRANGE:
            params: tuple[int, int] = params
            hpMin, hpMax = params

            lib.globals.bossHitpointRangeMin = hpMin
            lib.globals.bossHitpointRangeMax = hpMax
        elif opcode == Opcode.SET_PHASE_NAME:
            params: tuple[int] = params
            index, = params

            lib.globals.phaseIndex = index
            lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_NAME_REMAIN] = 120 if index else 0
            if index:
                lib.sound.SFX.PHASE_START.play()
        elif opcode == Opcode.SET_PHASE_BONUS:
            params: tuple[int, int] = params
            multiple, drop = params

            lib.globals.phaseBonus = multiple * lib.globals.maxGetPoint
            lib.globals.phaseBonusDrop = drop
        elif opcode == Opcode.MOVE:
            params: tuple[float, float, int, str] = params
            x, y, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                pygame.Vector2(x, y),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.MOVE_RELATIVE:
            params: tuple[float, float, int, str] = params
            x, y, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                self.context.position + pygame.Vector2(x, y),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.MOVE_RANDOM:
            params: tuple[float, float, float, float, int, str] = params
            x, y, width, height, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                pygame.Vector2(x + lib.globals.stgRandom.random() * width, y + lib.globals.stgRandom.random() * height),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.MOVE_CLEAR:
            self.movementQueue.clear()
            self.movementTask = None
        elif opcode == Opcode.SHOOT:
            params: tuple[str, float, float, float, float] = params
            bullet, x, y, speed, angle = params

            lib.bullet.enemy_bullet.EnemyBullet(
                self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                speed,
                angle,
                BulletSizeTable[bullet],
                BulletTextureTable[bullet],
            )
        elif opcode == Opcode.SHOOT_MULTIWAY:
            params: tuple[str, float, float, float, float, float, int] = params
            bullet, x, y, speed, angle, fanSize, ways = params

            for i in range(ways):
                fanAngle = (i - (ways - 1) / 2) / (ways - 1) * fanSize
                lib.bullet.enemy_bullet.EnemyBullet(
                    self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                    speed,
                    fanAngle + angle,
                    BulletSizeTable[bullet],
                    BulletTextureTable[bullet],
                )
        elif opcode == Opcode.SHOOT_AIMING:
            params: tuple[str, float, float, float, float] = params
            bullet, x, y, speed, angle = params

            shootPosition = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            lib.bullet.enemy_bullet.EnemyBullet(
                shootPosition,
                speed,
                -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + angle,
                BulletSizeTable[bullet],
                BulletTextureTable[bullet],
            )
        elif opcode == Opcode.SHOOT_AIMING_MULTIWAY:
            params: tuple[str, float, float, float, float, float, int] = params
            bullet, x, y, speed, angle, fanSize, ways = params

            shootPosition = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            for i in range(ways):
                fanAngle = (i - (ways - 1) / 2) / (ways - 1) * fanSize
                lib.bullet.enemy_bullet.EnemyBullet(
                    shootPosition,
                    speed,
                    -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + fanAngle + angle,
                    BulletSizeTable[bullet],
                    BulletTextureTable[bullet],
                )
        elif opcode == Opcode.SFX:
            params: tuple[str] = params
            sfxName, = params

            lib.sound.SFX.sfxName.play()
        elif opcode == Opcode.CLEAR_BULLET:
            for b in lib.globals.groupEnemyBullet:
                b: lib.bullet.enemy_bullet.EnemyBullet
                b.explode()
        elif opcode == Opcode.BONUS_BULLET:
            for b in lib.globals.groupEnemyBullet:
                b: lib.bullet.enemy_bullet.EnemyBullet
                lib.sprite.item.PointBullet(pygame.Vector2(b.position))
                b.explode()
            lib.sound.SFX.BONUS.play()
        elif opcode == Opcode.BONUS_PHASE:
            if lib.globals.replayRecording:
                lib.globals.savedata[lib.globals.optionType]['phaseHistory'][lib.globals.phaseIndex - 1]['total'] += 1
            lib.globals.score += lib.globals.phaseBonus
            lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_BONUS_REMAIN] = 240
            lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.PHASE_BONUS_VALUE] = lib.globals.phaseBonus
            if lib.globals.replayRecording and lib.globals.phaseBonus:
                lib.globals.phaseBonusCount += 1
                lib.globals.savedata[lib.globals.optionType]['phaseHistory'][lib.globals.phaseIndex - 1]['bonus'] += 1
            lib.globals.phaseIndex = 0
            lib.globals.phaseBonus = 0
        elif opcode == Opcode.DROP_POINTITEM:
            params: tuple[int] = params
            num, = params

            minwh = min(self.context.rect.width, self.context.rect.height)
            for i in range(num):
                pos = pygame.Vector2(lib.globals.stgRandom.random() * minwh, 0)
                pos.rotate_ip(lib.globals.stgRandom.random() * 360)
                pos += self.context.position
                lib.sprite.item.Point(pos)
        elif opcode == Opcode.EXTEND_LIFE:
            lib.sprite.item.LifeExtend(self.context.position)
        elif opcode == Opcode.EXTEND_HYPER:
            lib.sprite.item.HyperExtend(self.context.position)
        elif opcode == Opcode.PRESET_ENEMY_A:
            # SET_TEXTURE ENEMY_A
            # SET_EXPLOSION LARGE
            # SET_HITBOX 0 12 10
            # SET_HITBOX 0 -10 12
            # SET_HITBOX -19 -6 8
            # SET_HITBOX 19 -6 8
            # SET_DEBRIS DEBRIS_A -20 -6 .125 2 1 5 1
            # SET_DEBRIS DEBRIS_A 20 -6 .125 2 1 5 1
            # SET_DEBRIS DEBRIS_B 0 12 .125 2 1 5 2
            # SET_DEBRIS DEBRIS_B 0 -10 .125 2 1 5 1
            # SET_MAXGETPOINTADD 1000
            self.context.textures = EnemyTexturesTable['ENEMY_A']
            self.context.explosion = ExplosionTable['LARGE']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 12), 10),
                lib.sprite.Hitbox(pygame.Vector2(0, -10), 12),
                lib.sprite.Hitbox(pygame.Vector2(-19, -6), 8),
                lib.sprite.Hitbox(pygame.Vector2(19, -6), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-20, -6), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(20, -6), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 12), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 12), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, -10), .125, 2, 1, 5),
            ]
            self.context.score = 1000
            self.context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_C
        elif opcode == Opcode.PRESET_ENEMY_B:
            self.context.textures = EnemyTexturesTable['ENEMY_B']
            self.context.explosion = ExplosionTable['MEDIUM_A']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 500
            self.context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
        elif opcode == Opcode.PRESET_ENEMY_C:
            self.context.textures = EnemyTexturesTable['ENEMY_C']
            self.context.explosion = ExplosionTable['MEDIUM_B']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 500
            self.context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
        elif opcode == Opcode.PRESET_ENEMY_D:
            self.context.textures = EnemyTexturesTable['ENEMY_D']
            self.context.explosion = ExplosionTable['MEDIUM_B']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 200
            self.context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_B
        elif opcode == Opcode.PRESET_ENEMY_E:
            self.context.textures = EnemyTexturesTable['ENEMY_E']
            self.context.explosion = ExplosionTable['SMALL_A']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(4, 0), 6),
                lib.sprite.Hitbox(pygame.Vector2(-4, 0), 6),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_A'], pygame.Vector2(4, 0), .125, 1.75, .5, 2),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(-4, 0), .125, 1.75, .5, 2),
            ]
            self.context.score = 100
            self.context.explodeSfx = lib.sound.SFX.EXPLODE_ENEMY_A

        # elif opcode == Opcode.:
        #     params: tuple[] = params
        #      = params
        else:
            print('Unknown opcode:', opcode)
