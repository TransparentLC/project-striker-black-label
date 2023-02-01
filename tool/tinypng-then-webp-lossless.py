import os
import random
import requests
import tempfile
import secrets
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

def convert(path: str) -> int:
    with open(path, 'rb') as f:
        data = f.read()
    r = requests.post(
        'https://tinypng.com/web/shrink',
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Forwarded-For': '.'.join([str(random.randint(0, 255)) for i in range(4)]),
        }
    )

    try:
        r = r.json()
        print(f'{os.path.basename(path)} {r["input"]["size"]} -> {r["output"]["size"]} Bytes ({round(r["output"]["ratio"] * 100, 2)}%) {r["output"]["url"]}')
    except:
        print('Failed to compress')
        return

    fn = os.path.join(tempfile.gettempdir(), secrets.token_urlsafe(12))
    r = requests.get(r['output']['url'])
    with open(fn, 'wb') as f:
        f.write(r.content)
    subprocess.Popen((
        'cwebp',
        '-q', '100',
        '-z', '9',
        '-m', '6',
        '-mt',
        '-lossless',
        fn,
        '-o', f'{os.path.splitext(path)[0]}.webp',
    )).wait()
    os.remove(fn)

with ThreadPoolExecutor(os.cpu_count()) as executor:
    executor.map(convert, sys.argv[1:])