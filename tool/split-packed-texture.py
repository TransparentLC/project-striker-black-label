import json
import os
import sys
from PIL import Image

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    meta: dict[str, dict[str, int]] = json.load(f)
if os.path.exists(os.path.splitext(sys.argv[1])[0] + '.webp'):
    packed = Image.open(os.path.splitext(sys.argv[1])[0] + '.webp')
elif os.path.exists(os.path.splitext(sys.argv[1])[0] + '.png'):
    packed = Image.open(os.path.splitext(sys.argv[1])[0] + '.png')
outputDir = os.path.splitext(os.path.basename(sys.argv[1]))[0]
os.mkdir(outputDir)

for k, v in meta.items():
    packed.crop((v['x'], v['y'], v['x'] + v['w'], v['y'] + v['h'])).save(os.path.join(outputDir, k + '.png'))