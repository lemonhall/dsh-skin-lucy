"""OFOX image generation helper (urllib only, no third-party deps).

Follows the verified recipe in ~/.agents/skills/ofox-imagegen/SKILL.md:
POST https://api.ofox.ai/v1/images/generations with a Bearer key taken from the
Windows machine environment (never printed), through the user's local proxy.
Preserves original bytes + request params + inspection metadata per run.
"""
import argparse
import base64
import hashlib
import io
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
import winreg
from pathlib import Path

ENDPOINT = 'https://api.ofox.ai/v1/images/generations'
MODELS_ENDPOINT = 'https://api.ofox.ai/v1/models'
PROXY = 'http://127.0.0.1:7897'
DEFAULT_MODEL = 'openai/gpt-image-2.5-sunburst'


def api_key():
    key = os.environ.get('OFOX_IMG_API_KEY', '')
    if not key:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
        ) as reg:
            key = winreg.QueryValueEx(reg, 'OFOX_IMG_API_KEY')[0]
    if not key.strip():
        raise SystemExit('OFOX_IMG_API_KEY empty')
    return key


def opener():
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
    )


def probe():
    op = opener()
    req = urllib.request.Request(MODELS_ENDPOINT, headers={'Authorization': 'Bearer ' + api_key()})
    with op.open(req, timeout=60) as r:
        data = json.loads(r.read().decode('utf-8'))
    ids = [m.get('id') for m in data.get('data', [])]
    hits = [i for i in ids if i and ('image' in i or 'seedream' in i or 'seededit' in i)]
    print('total models:', len(ids))
    for i in sorted(hits):
        print(' ', i)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out')
    ap.add_argument('--prompt')
    ap.add_argument('--model', default=DEFAULT_MODEL)
    ap.add_argument('--size', default='1024x1024')
    ap.add_argument('--background', default=None,
                    help='transparent|opaque|auto|omit (default: transparent for openai/*, omit otherwise)')
    ap.add_argument('--probe', action='store_true')
    ap.add_argument('--retries', type=int, default=2)
    args = ap.parse_args()

    if args.probe:
        probe()
        return
    if not args.out or not args.prompt:
        raise SystemExit('--out and --prompt are required')

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    background = args.background or ('transparent' if args.model.startswith('openai/') else 'omit')
    payload = {
        'model': args.model,
        'prompt': args.prompt,
        'size': args.size,
        'n': 1,
        'output_format': 'png',
    }
    if background != 'omit':
        payload['background'] = background
    (out / 'request.json').write_text(
        json.dumps({k: v for k, v in payload.items() if k != 'prompt'} | {'prompt': args.prompt},
                   ensure_ascii=False, indent=2), encoding='utf-8')

    body = json.dumps(payload).encode('utf-8')
    last = None
    for attempt in range(args.retries + 1):
        req = urllib.request.Request(
            ENDPOINT, data=body,
            headers={'Authorization': 'Bearer ' + api_key(), 'Content-Type': 'application/json'},
        )
        try:
            with opener().open(req, timeout=600) as r:
                data = json.loads(r.read().decode('utf-8'))
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', 'replace')
            (out / 'error.txt').write_text(f'HTTP {e.code}\n{detail}', encoding='utf-8')
            print('HTTP', e.code)
            print(detail[:2000])
            raise SystemExit('request rejected; no automatic retry')
        except Exception as e:  # transport error
            last = e
            print(f'transport error attempt {attempt + 1}: {type(e).__name__} {e}', flush=True)
            time.sleep(5 * (attempt + 1))
    else:
        raise SystemExit(f'all attempts failed: {last}')

    items = data.get('data', [])
    (out / 'response-summary.json').write_text(json.dumps(
        {'created': data.get('created'), 'model': data.get('model'), 'output_count': len(items)},
        indent=2), encoding='utf-8')
    if not items:
        raise SystemExit('no output image')
    from PIL import Image
    for index, item in enumerate(items):
        if item.get('b64_json'):
            raw = base64.b64decode(item['b64_json'], validate=True)
        else:
            url = item['url']
            dl = urllib.request.Request(url)
            with opener().open(dl, timeout=180) as r:
                raw = r.read()
        im = Image.open(io.BytesIO(raw))
        im.load()
        (out / f'image-{index}.{im.format.lower()}').write_bytes(raw)
        alpha = im.getchannel('A') if 'A' in im.getbands() else None
        hist = alpha.histogram() if alpha else [0] * 256
        report = dict(
            format=im.format, mode=im.mode, size=list(im.size),
            sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
            transparent_pixels=hist[0] if alpha else 0,
            partial_alpha_pixels=sum(hist[1:255]) if alpha else 0,
            opaque_pixels=hist[255] if alpha else im.width * im.height,
            native_transparency=alpha is not None,
        )
        (out / f'inspection-{index}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
