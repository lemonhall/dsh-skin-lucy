# Lucy · Night City Signal — DSH skin

English | [中文](README.zh.md)

A cyberpunk fan skin for the DeepSeek Harness web GUI: a bright daytime
megacity rooftop for the light theme and a neon-soaked night skyline for the
dark theme, flanked by two silver-bob netrunner portraits. Distributed as a
pure asset directory that the Skin Center (or the Creative Workshop) drops into
`$DSH_HOME/skins/lucy-nightsignal/`.

How every one of those decisions was reached - the real shell contract read out
of the desktop bundle, the two measured CSS pitfalls, and the verification method
- is written up in [docs/SKIN-TECHNIQUE.md](docs/SKIN-TECHNIQUE.md).

## Layout

```
skins/lucy-nightsignal/     the skin itself — this is the directory that gets installed
  skin.json                 manifest v2 (id, palette metadata, contributions)
  skin.css                  L1 token remap (light on :root, dark on body[data-ds-dark-theme])
  patches.css               L3 free selectors: the two character layers + neon chrome
  assets/                   scene-light / scene-dark / lucy-signal-left / lucy-signal-right
  preview/                  light.jpg + dark.jpg, 1440x900 JPEG q85
docs/ART-PROVENANCE.md      models, prompts, digests and the matting recipe
tools/                      the generator and matting helpers used for the assets
```

## Install

Copy (or let the Workshop install) the skin directory:

```sh
git clone https://github.com/lemonhall/dsh-skin-lucy
Copy-Item -Recurse dsh-skin-lucy/skins/lucy-nightsignal "$env:USERPROFILE\.dsh\skins\"
```

Then open Settings -> Skin Center (or the Creative Workshop card) and pick
"露西·夜城信号". No restart and no reload are required; the Skin Center rescans
`$DSH_HOME/skins` while the card is open.

## How it is built

- **Token first.** `skin.css` only remaps official `--dsw-*` tokens, so every
  surface follows the skin without brittle selectors.
- **Declarative characters.** The two portraits are painted by
  `body:before` / `body:after` in `patches.css`, not by a `hooks.mjs`, because
  the market preview renderer never executes skin hooks — a hooks-only scene
  would not appear in the shop preview. `isolation: isolate` on `body` keeps the
  host's `backgroundMedia` layer (z-index -2, appended to body) visible behind
  the negative-z-index character layers.
- **AI artwork, processed locally.** Both character plates were keyed off a flat
  magenta backdrop, colour-unmixed and despilled locally; the scenes were kept
  opaque. Prompts and digests: `docs/ART-PROVENANCE.md`.

## Preview

`preview/light.jpg` and `preview/dark.jpg` are real 1440x900 screenshots of the
running GUI with this skin applied, captured with Chrome through Playwright at
deviceScaleFactor 1, then saved as JPEG quality 85 — the format the market's
`capture-previews` writes.

## Licence

CC BY-NC-SA 4.0. Unofficial fan artwork; see [NOTICE](NOTICE).
