import ctypes
import math
import platform
import pygame
import typing

libraryExtension = {
    'Windows': '.dll',
    'Linux': '.so',
    'Darwin': '.dylib',
}[platform.system()]

libstgnative = ctypes.cdll.LoadLibrary(f'./libstgnative{libraryExtension}')
libstgnative.xbrz_scale.argtypes = (
    ctypes.c_size_t,
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_int, ctypes.c_int,
    ctypes.c_int,
)
libstgnative.xbrz_scale.restype = None
libstgnative.perspective_blit.argtypes = (
    ctypes.c_void_p,
    ctypes.c_size_t, ctypes.c_size_t,
    ctypes.c_void_p,
    ctypes.c_size_t, ctypes.c_size_t,
    ctypes.c_float, ctypes.c_float, ctypes.c_float,
    ctypes.c_float, ctypes.c_float, ctypes.c_float,
    ctypes.c_bool,
)
libstgnative.perspective_blit.restype = None

def xbrzScale(factor: int, src: pygame.Surface, dest: typing.Optional[pygame.Surface] = None) -> pygame.Surface:
    if not 2 <= factor <= 6:
        raise ValueError('Scale factor must between 2 and 6.')
    if src.get_parent() is not None:
        src = src.copy()
    w, h = src.get_size()
    if dest is None:
        dest = pygame.Surface((w * factor, h * factor), src.get_flags() & pygame.SRCALPHA)
    bp = src.get_buffer()
    srcBuf = (ctypes.c_uint8 * (w * h * 4)).from_buffer_copy(bp.raw)
    del bp
    destBuf = (ctypes.c_uint8 * (w * factor * h * factor * 4))()
    libstgnative.xbrz_scale(factor, srcBuf, destBuf, w, h, 1 if src.get_flags() & pygame.SRCALPHA else 0)
    bp = dest.get_buffer()
    bp.write(destBuf)
    del bp
    return dest

def perspectiveBlit(
    src: pygame.Surface, dest: pygame.Surface,
    horizon: float, fov: float, scaling: float,
    offset: pygame.Vector2, rotate: float = 0,
    repeat: bool = False
):
    if src.get_parent() is not None:
        src = src.copy()
    sw, sh = src.get_size()
    dw, dh = dest.get_size()
    bp = src.get_buffer()
    srcBuf = (ctypes.c_uint8 * (sw * sh * 4)).from_buffer_copy(bp.raw)
    del bp
    destBuf = (ctypes.c_uint8 * (dw * dh * 4))()
    libstgnative.perspective_blit(
        srcBuf,
        sw, sh,
        destBuf,
        dw, dh,
        horizon, fov, scaling,
        offset.x, offset.y, rotate / 180 * math.pi,
        repeat,
    )
    bp = dest.get_buffer()
    bp.write(destBuf)
    del bp
