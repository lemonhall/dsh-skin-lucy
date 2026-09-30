"""Chroma-key matting for Seedream output (opaque RGB on a flat key colour).

Implements the verified recipe from ~/.agents/skills/ofox-imagegen/SKILL.md:
  1. estimate the key colour from the image border (median), or take --key
  2. alpha = ramp of the Euclidean distance to the key between --inner and --outer
  3. unmix the colour: F = (observed - (1 - a) * key) / a
  4. despill (pull the key hue back out of partially transparent pixels)
  5. alpha floor (--alpha-floor) then connected-component despeckle (--despeckle-min-area)
Order matters: unmix -> floor -> despill -> despeckle.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def hex_rgb(text):
    text = text.lstrip('#')
    return np.array([int(text[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


def border_pixels(rgb, band):
    h, w, _ = rgb.shape
    b = max(1, band)
    return np.concatenate([
        rgb[:b].reshape(-1, 3), rgb[-b:].reshape(-1, 3),
        rgb[:, :b].reshape(-1, 3), rgb[:, -b:].reshape(-1, 3),
    ])


def label_components(mask):
    """Simple 4-connected component labelling (iterative flood fill)."""
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=np.int32)
    current = 0
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys.tolist(), xs.tolist()):
        if labels[sy, sx]:
            continue
        current += 1
        stack = [(sy, sx)]
        labels[sy, sx] = current
        while stack:
            y, x = stack.pop()
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not labels[ny, nx]:
                    labels[ny, nx] = current
                    stack.append((ny, nx))
    return labels, current


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--key', default=None, help='hex key colour; default = border median')
    ap.add_argument('--inner', type=float, default=12.0, help='distance <= inner is pure background')
    ap.add_argument('--outer', type=float, default=90.0, help='distance >= outer is pure subject')
    ap.add_argument('--alpha-floor', type=int, default=40)
    ap.add_argument('--despeckle-min-area', type=int, default=64)
    ap.add_argument('--key-channel', default='magenta', choices=['magenta', 'green', 'blue'],
                    help='which spill direction to despill')
    ap.add_argument('--pad', type=int, default=8, help='trim transparent border, keep this margin')
    ap.add_argument('--max-side', type=int, default=0, help='optional downscale of the long side')
    args = ap.parse_args()

    src = Path(args.src)
    im = Image.open(src).convert('RGB')
    rgb = np.asarray(im).astype(np.float64)
    h, w, _ = rgb.shape

    if args.key:
        key = hex_rgb(args.key)
        key_source = 'explicit'
    else:
        border = border_pixels(rgb, max(2, min(h, w) // 100))
        key = np.median(border, axis=0)
        key_source = 'border-median'

    dist = np.sqrt(((rgb - key) ** 2).sum(axis=2))
    alpha = np.clip((dist - args.inner) / max(1e-6, args.outer - args.inner), 0.0, 1.0)

    a = alpha[..., None]
    safe = np.maximum(a, 1e-3)
    unmixed = (rgb - (1.0 - a) * key) / safe
    unmixed = np.clip(unmixed, 0, 255)

    # despill: on partial alpha, remove the key's dominant channel excess
    partial = (alpha > 0.05) & (alpha < 0.95)
    r, g, b = unmixed[..., 0], unmixed[..., 1], unmixed[..., 2]
    if args.key_channel == 'magenta':
        excess = np.minimum(r, g) - b
        spill = partial & (excess > 0)
        unmixed[..., 0] = np.where(spill, r - excess * 0.85, r)
        unmixed[..., 1] = np.where(spill, g - excess * 0.85, g)
    elif args.key_channel == 'green':
        excess = g - np.maximum(r, b)
        spill = partial & (excess > 0)
        unmixed[..., 1] = np.where(spill, g - excess * 0.85, g)
    else:
        excess = b - np.maximum(r, g)
        spill = partial & (excess > 0)
        unmixed[..., 2] = np.where(spill, b - excess * 0.85, b)

    alpha8 = (alpha * 255.0).round().astype(np.uint8)
    alpha8[alpha8 < args.alpha_floor] = 0

    rgba = np.dstack([unmixed.round().astype(np.uint8), alpha8])
    out_im = Image.fromarray(rgba, 'RGBA')

    if args.despeckle_min_area > 0:
        mask = np.asarray(out_im.getchannel('A')) > 0
        labels, count = label_components(mask)
        if count:
            sizes = np.bincount(labels.ravel())
            keep = np.zeros(sizes.size, dtype=bool)
            keep[1:] = sizes[1:] >= args.despeckle_min_area
            kept_mask = keep[labels]
            arr = np.asarray(out_im).copy()
            arr[..., 3] = np.where(kept_mask, arr[..., 3], 0)
            out_im = Image.fromarray(arr, 'RGBA')

    if args.pad >= 0:
        bbox = out_im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        if bbox:
            left = max(0, bbox[0] - args.pad)
            top = max(0, bbox[1] - args.pad)
            right = min(out_im.width, bbox[2] + args.pad)
            bottom = min(out_im.height, bbox[3] + args.pad)
            out_im = out_im.crop((left, top, right, bottom))

    if args.max_side and max(out_im.size) > args.max_side:
        scale = args.max_side / max(out_im.size)
        out_im = out_im.resize((round(out_im.width * scale), round(out_im.height * scale)), Image.LANCZOS)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_im.save(out)

    arr = np.asarray(out_im)
    al = arr[..., 3]
    border_ratio = float((al == 0).mean())
    partial_px = int(((al > 0) & (al < 255)).sum())
    report = {
        'src': str(src), 'src_size': [w, h], 'key': [round(float(v), 1) for v in key],
        'key_source': key_source, 'out': str(out), 'out_size': list(out_im.size),
        'transparent_ratio': round(border_ratio, 4),
        'partial_alpha_pixels': partial_px,
        'opaque_pixels': int((al == 255).sum()),
    }
    print(json.dumps(report, ensure_ascii=False))
    Path(str(out) + '.matte.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
