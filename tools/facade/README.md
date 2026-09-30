# Facade preview tooling

`preview/{light,dark}.jpg` are shot with the market's own static renderer, not
with a hand-built mock: the dsh-web repository commits `market/dist`, whose
`preview.html` + `official-facade.js` paint the desensitised official GUI and
inject the selected skin's stylesheets (skin.css + patches.css) and its
declarative `backgroundMedia`. `scripts/capture-previews` in that repository uses
the same page. These two scripts are a dependency-light equivalent that reuses
the locally installed Chrome instead of downloading Chromium.

## Getting a facade directory

```sh
git clone --filter=blob:none --no-checkout https://github.com/zhu1090093659/dsh-web dsh-web
cd dsh-web
git checkout dev -- market/dist scripts/capture-previews
```

Then add the skin to the facade: copy `skins/<id>/` to
`market/dist/assets/skins/<id>/`, and append the skin's entry to
`market/dist/manifest.js` (`window.SKIN_MANIFEST`) and its stylesheet text to
`market/dist/styles.js` (`window.SKIN_STYLES`) - that is what the market build
does for every published skin.

## Usage

```sh
PLAYWRIGHT_PATH=<prefix>/node_modules/playwright \
  node tools/facade/diag.cjs <facade-dir> <id>

PLAYWRIGHT_PATH=<prefix>/node_modules/playwright \
  node tools/facade/capture-facade.cjs <facade-dir> <out-dir> <id>
```

`diag.cjs` prints the numbers behind the layout: whether anchor positioning is
supported, how many elements carry the anchor name, the input card's rect, and
the computed inset / size / background of both portraits. `capture-facade.cjs`
writes `<out-dir>/{light,dark}.jpg` at 1440x900, device scale 1, JPEG q85.

## Drawer-state variants

The facade snapshot ships the sidebar expanded and the details pane closed. To
check the other states offline, copy the facade and rewrite the desensitised
skeleton's own inline geometry before rendering:

- collapsed rail: add `data-sidebar-collapsed` and `data-windows-titlebar` to the
  frame, rewrite its inline `grid-template-columns` first track to `0px`, and set
  the sidebar body's inline width to `0px`;
- details pane open: drop `data-rightbar-collapsed` from the frame and inject
  `<div data-rightbar-col style="position:fixed;inset:0 0 0 auto;width:45vw">`.

That is how the drawer behaviour was verified while developing this skin,
without touching the live GUI.
