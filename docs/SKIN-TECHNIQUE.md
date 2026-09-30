# Skin technique — how lucy-nightsignal is built

English summary below; 中文说明在后半部分。No emoji, per the dsh-skins family rules.

## English

### The layout contract this skin targets

The desktop shell (0.2.0-rc.2) does **not** expose the semantic attributes the
skin-center contract documents (`data-pane`, `data-dsh-surface`,
`data-dsh-part`, `data-dsh-frame` all have zero occurrences in the shipped app
bundle). What it does expose, verified by reading `resources/app.asar`:

| fact | evidence in the bundle |
| --- | --- |
| frame element carries `*_frame` class, plus `data-sidebar-collapsed` / `data-rightbar-collapsed` flags | `"data-sidebar-collapsed": sidebarCollapsed || void 0` on the frame element |
| the frame publishes its own sidebar width as a CSS variable | `"--dsh-windows-sidebar-width": `${cols.sidebar}px`` (Windows titlebar host only) |
| collapsed sidebar width | `const collapsedWidth = darwin || hasAttribute("data-windows-titlebar") ? 0 : 56` |
| the details pane is `<div data-rightbar-col>` | `RightbarColumn` sets `"data-rightbar-col": true` |
| the details pane can take up to 45% of the frame | `rightbarPreference = layoutInfo.rightbar ?? viewport * .45` |
| chat column width comes from the chat body | `.…_body{--dsh-chat-content-width:var(--dsh-chat-user-width, clamp(680px, column*0.64, 920px))}` |
| stable composer hooks | `data-composer-card`, `data-composer-seat`, `data-composer-input` |
| sidebar / centre / details classes | `*_sidebarCol`, `*_centerCol`, `*_rightbarCol` |

Because `--dsh-chat-content-width` is redefined on the chat body, a skin cannot
narrow the column by setting that name on an ancestor. It must set
`--dsh-chat-user-width` (and `!important` on both names to outrank the inner
declaration).

### Why there are no hooks

`hooks.mjs` is the maid-atelier approach for drawer-aware characters, but it is
unavailable here for two reasons:

1. the market preview renderer never executes skin hooks, so a hooks-only scene
   does not appear in the shop preview;
2. the skin center runs hooks for a user-directory skin only when its bytes match
   an official market install (`dsh-market.provenance.json`). A hand-placed skin
   is refused by design, and forging provenance would be circumventing a
   security check.

So the portraits are declarative CSS.

### The two measured pitfalls

Both were only visible by measuring the rendered page, not by reading CSS:

1. **`right: calc(100% - anchor(--x left))` does not behave as
   `viewport - anchor`.** Measured in Chrome 154: `body::before` computed
   `right: 562.906px` for an anchor whose left edge was also 562.906 - the
   drawing landed ~314px inside the input card. The fix is to avoid percentage
   arithmetic entirely: put the element's *left* edge on the anchor's left edge
   and shift it by its own width with `translate: -100% 0`.
2. **A box wider than the artwork breaks flush edges.** With
   `background-size: contain` the art is centred, so a 317px box around a 231px
   drawing leaves a 43px gap on each side and the drawing can never touch the
   card. Giving each portrait `height + aspect-ratio + width: auto` makes the
   box identical to the drawing.

Additionally, `z-index: 5` is not enough: the shell's frame subtree carries
`z-index: 15` layers, so the portraits sat behind an opaque centre-column fill
and were invisible in the dark theme. The skin uses `z-index: 9999`.

### The layout itself

```css
[data-composer-card] { anchor-name: --lucy-composer; }

body::before {                       /* left portrait */
  left: anchor(--lucy-composer left, 40vw);
  translate: -100% 0;                /* its right edge lands on the card's left edge */
  height: clamp(400px, 76vh, 940px);
  aspect-ratio: 609 / 1800;          /* box == drawing */
  width: auto;
}

body::after {                        /* right portrait */
  left: anchor(--lucy-composer right, 80vw);
  height: clamp(400px, 66vh, 900px);
  aspect-ratio: 915 / 1800;
  width: auto;
}
```

The input card is the anchor, so both portraits follow the left rail and the
right details pane for free: the card re-centres whenever either drawer moves,
and no width ever has to be measured. With the details pane open the card's right
edge already touches the pane, so only the left portrait stays.

Supporting fixes that make the artwork visible at all:

```css
[id="root"]              { background: none; }        /* else the -2 backdrop layer never paints */
[class*="_frame"]        { background: transparent !important; }
body                     { isolation: isolate; }      /* keeps the -2 backdrop above the canvas step */
:is(body, [class*="_frame"], [data-phase], …) {
  --dsh-chat-user-width: min(clamp(420px, 38vw, 700px), calc(100% - 24px)) !important;
}
```

### Verification method

`preview/{light,dark}.jpg` are 1440x900 JPEG q85 shot through the market's own
facade renderer (`market/dist/preview.html` + `official-facade.js`), i.e. the
same static renderer `scripts/capture-previews` uses:

- `tools/facade/diag.cjs <facade-dir>` prints the real numbers (anchor owner,
  card rect, computed insets of both pseudo-elements);
- `tools/facade/capture-facade.cjs <facade-dir> <out-dir> <skin-id>` writes the
  two previews.

A collapsed-drawer and a details-open variant of the facade were rendered the
same way while developing, which is how the drawer behaviour was checked without
touching the live GUI.

## 中文

### 这套皮肤针对的真实契约

桌面版 0.2.0-rc.2 **没有**皮肤中心契约文档里写的那些语义属性（`data-pane`、
`data-dsh-surface`、`data-dsh-part`、`data-dsh-frame` 在 app.asar 里命中数都是 0）。
真正能用的东西（全部由读取 `resources/app.asar` 得到）：

| 事实 | 证据 |
| --- | --- |
| frame 元素带 `*_frame` 类名 + `data-sidebar-collapsed` / `data-rightbar-collapsed` 标记 | frame 元素上的 `"data-sidebar-collapsed": sidebarCollapsed \|\| void 0` |
| frame 会把自己的侧栏宽度发布成 CSS 变量 | `"--dsh-windows-sidebar-width": \`${cols.sidebar}px\``（仅 Windows 标题栏宿主） |
| 收折后的侧栏宽度 | `const collapsedWidth = darwin \|\| hasAttribute("data-windows-titlebar") ? 0 : 56` |
| 右栏是 `<div data-rightbar-col>` | `RightbarColumn` 打 `"data-rightbar-col": true` |
| 右栏最大可占 45% | `rightbarPreference = layoutInfo.rightbar ?? viewport * .45` |
| 对话列宽来自对话 body | `.…_body{--dsh-chat-content-width:var(--dsh-chat-user-width, clamp(680px, 列宽*0.64, 920px))}` |
| 可用的输入框钩子 | `data-composer-card`、`data-composer-seat`、`data-composer-input` |
| 三栏类名 | `*_sidebarCol`、`*_centerCol`、`*_rightbarCol` |

因为 `--dsh-chat-content-width` 在对话 body 上被**重新定义**，皮肤在祖先上写这个名字
是无效的；必须写 `--dsh-chat-user-width`，并且两个名字都要 `!important` 才能压过内层声明。

### 为什么不用 hooks

女仆那套用 `hooks.mjs` 量侧栏宽度，这里用不了，两个原因：

1. 市场预览渲染器从不执行皮肤 hooks —— 只靠 hooks 画的场景在商店预览里不会出现；
2. 皮肤中心只对「字节级匹配官方市场安装」的用户目录皮肤放行 hooks
   （`dsh-market.provenance.json`）。手工投放的目录会被按设计拒绝，伪造 provenance
   等于绕过安全检查。

所以两个立绘是纯声明式 CSS。

### 两个只有实测才能发现的坑

1. **`right: calc(100% - anchor(--x left))` 并不等于「视口 - 锚点」**。Chrome 154 实测：
   锚点左沿 562.906 时，`body::before` 的 `right` 也算成 562.906，画直接压进输入框 314px。
   解法是干脆不用百分比运算：把元素的**左沿**对齐锚点左沿，再用 `translate: -100% 0`
   按自身宽度左移。
2. **盒子比画宽，边缘就永远贴不上**。`background-size: contain` 会把画居中，317px 的盒子
   装 231px 的画，两侧各留 43px 空隙。改成 `height + aspect-ratio + width: auto`，
   盒子等于画。

另外 `z-index: 5` 不够：官方 frame 子树里有 `z-index: 15` 的层，立绘会落在中栏不透明
fill 之下（暗色主题里等于看不见）。本皮肤用 `z-index: 9999`。

### 布局本身

见上面的 CSS 片段：以输入框卡片为锚点，左立绘右沿贴卡片左沿、右立绘左沿贴卡片右沿。
抽屉一动，输入框重新居中，两个立绘跟着走，全程不需要测量任何宽度。右栏展开时卡片右沿
已经顶到栏边，所以只保留左边那位。

### 验证方式

`preview/{light,dark}.jpg` 是用市场自己的 facade 渲染器（`market/dist/preview.html` +
`official-facade.js`，也就是 `scripts/capture-previews` 用的同一套静态渲染器）拍出的
1440x900 JPEG q85：

- `tools/facade/diag.cjs <facade-dir>` 打印真实数字（锚点归属、卡片矩形、两个伪元素的
  计算后 inset）；
- `tools/facade/capture-facade.cjs <facade-dir> <out-dir> <skin-id>` 输出两张预览图。

开发过程中还用同一套办法渲染了「左栏收折」和「右栏展开」两个变体，抽屉行为就是这样在不
碰真实 GUI 的前提下验证的。
