import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

def convert(path: str) -> int:
    return subprocess.Popen((
        'ffmpeg',
        '-y',
        '-i', path,
        '-c:a', 'libvorbis',
        '-b:a', '192k',
        '-map_metadata', '-1',
        f'{os.path.splitext(path)[0]}.ogg',
    )).wait()

with ThreadPoolExecutor(os.cpu_count()) as executor:
    executor.map(convert, sys.argv[1:])