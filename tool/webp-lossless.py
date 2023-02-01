import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

def convert(path: str) -> int:
    return subprocess.Popen((
        'cwebp',
        '-q', '100',
        '-z', '9',
        '-m', '6',
        '-mt',
        '-lossless',
        path,
        '-o', f'{os.path.splitext(path)[0]}.webp',
    )).wait()

with ThreadPoolExecutor(os.cpu_count()) as executor:
    executor.map(convert, sys.argv[1:])