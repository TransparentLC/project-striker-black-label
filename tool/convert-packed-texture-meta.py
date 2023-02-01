import json

import os
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    originalMeta = json.load(f)

generatedMeta = {}
for k, v in originalMeta['frames'].items():
    generatedMeta[os.path.splitext(k)[0]] = v['frame']

with open(sys.argv[1], 'w', encoding='utf-8') as f:
    json.dump(generatedMeta, f, ensure_ascii=False, separators=(',', ':'))