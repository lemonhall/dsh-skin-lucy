# 露西·夜城信号 — DSH 皮肤

[English](README.md) | 中文

一套给 DeepSeek Harness Web GUI 用的赛博朋克同人皮肤。亮色是云海之上的黄昏都市天台，暗色是霓虹雨雾里的夜之城天际线。两个抠好透明底的银白波波头立绘**分别贴着输入框的左沿与右沿**，并随左右两个抽屉自动跟随。

| | |
| --- | --- |
| 皮肤 id | `lucy-nightsignal` |
| 版本 | 0.1.0 |
| 清单 | v2（`skin.json`，皮肤中心契约） |
| 针对版本 | DSH 0.2.0-rc.2 桌面版 + `@linxin666/dsh-client-ui-skin-center` 0.4.3 |
| 许可 | CC BY-NC-SA 4.0（非官方同人作品） |

## 效果

亮色 —— 数据列收窄后两侧留出站立的余地，左立绘的右沿正好贴住输入框左沿：

![亮色主题](skins/lucy-nightsignal/preview/light.jpg)

暗色 —— 正面姿态的立绘更大，左沿正好贴住输入框右沿：

![暗色主题](skins/lucy-nightsignal/preview/dark.jpg)

两张预览都是 1440x900、JPEG 质量 85，用**市场自己那套 facade 渲染器**（`market/dist/preview.html` + `official-facade.js`，也就是创意工坊画廊用的同一套静态渲染器）拍出来的。复现命令见 `tools/facade/capture-facade.cjs` 与 `tools/facade/README.md`。

## 安装

### 手工安装

```powershell
git clone https://github.com/lemonhall/dsh-skin-lucy
Copy-Item -Recurse dsh-skin-lucy\skins\lucy-nightsignal "$env:USERPROFILE\.dsh\skins\"
```

然后打开 设置 → 皮肤中心（或创意工坊卡片），选 `露西·夜城信号`。**不需要重启、也不需要刷新页面**：皮肤中心在卡片打开时会重扫 `$DSH_HOME/skins`。

### 从创意工坊安装

已按 `skins/lucy-nightsignal` 提交到 [zhu1090093659/dsh-skins](https://github.com/zhu1090093659/dsh-skins)。合入后创意工坊会按需装进 `$DSH_HOME/skins/lucy-nightsignal`。投稿清单与可直接粘贴的 PR 正文在 [docs/PR-dsh-skins.md](docs/PR-dsh-skins.md)。

## 布局做法与理由

皮肤中心契约里写的语义属性（`data-dsh-surface`、`data-dsh-part`、`data-pane`）在**实际发布的 0.2.0 桌面版里并不存在**。所以这里全部改用真实构建里确实有的钩子，逐条都是从 `resources/app.asar` 里读出来的：

- 输入框是 `[data-composer-card]`，直接当几何锚点：左立绘用 `left: anchor(--lucy-composer left)` 配 `translate: -100% 0`，右立绘用 `left: anchor(--lucy-composer right)`。抽屉一动，输入框重新居中，**两个立绘就跟着走 —— 全程不需要测量任何宽度**；
- 每个立绘的元素盒子**等于画本身**（`height` + `aspect-ratio` + `width: auto`）。盒子比画宽时 `background-size: contain` 会把画居中留缝，边缘就永远贴不上；
- 立绘画在 `z-index: 900`：高于所有官方面板（frame 自身那几层是 15~40），但**低于鲸鱼娘挂件**（它的根固定在 `<body>` 上、`z-index: 9999`）。同值时平局按树的先后判，而伪元素是最后一个子盒 —— 早先的版本因此把挂件气泡盖住了；
- 数据列使用官方自己的旋钮 `--dsh-chat-user-width` 收窄（必须带 `!important`，因为对话 body 内部会重新定义 `--dsh-chat-content-width`），立绘的"两翼"就是这么来的。

**故意不带 `hooks.mjs`**：市场预览渲染器从不执行皮肤 hooks，而皮肤中心只对「字节级匹配官方市场安装」的用户目录皮肤放行 hooks。用纯声明式 CSS，商店预览才跟实机一致。完整推导（含两个只有实测才能发现的坑）见 [docs/SKIN-TECHNIQUE.md](docs/SKIN-TECHNIQUE.md)。

### 抽屉联动（带证据）

| 状态 | 表现 |
| --- | --- |
| 两个抽屉都收起 | 两个立绘各站一侧，边缘与输入框严丝合缝 |
| 左侧栏收起 | 输入框重新居中，左立绘跟着滑到窗口最左 |
| 右侧 details 栏展开 | 输入框右沿已顶到栏边，右立绘改为站在栏上，而不是消失 |

左侧栏收成 0px 轨道：

![左侧栏收折](docs/shots/drawer-collapsed-light.jpg)

右侧 details 栏展开（那层深色叠加是我为验证加的栏区示意，不是皮肤的一部分）：

![右侧栏展开](docs/shots/details-open-light.jpg)

右下角挂件仍然是它的：下面这个 mock 挂件按真实的 `z-index: 9999` 渲染，画在立绘靴子之上：

![挂件避让](docs/shots/widget-clearance-dark.jpg)

## 仓库结构

```
skins/lucy-nightsignal/     皮肤本体 —— 被安装的就是这个目录
  skin.json                 清单 v2（id、配色元数据、贡献项）
  skin.css                  L1 token 重映射（亮色挂 :root，暗色挂 body[data-ds-dark-theme]）
  patches.css               L3 自由选择器：两层立绘 + 霓虹描边
  assets/                   scene-light、scene-dark、lucy-signal-left、lucy-signal-right
  preview/                  light.jpg + dark.jpg，1440x900 JPEG q85
  README.md / README.zh.md  皮肤自带的中英说明
docs/ART-PROVENANCE.md      模型、提示词、摘要与抠图配方
docs/SKIN-TECHNIQUE.md      布局契约与实测坑
docs/PR-dsh-skins.md        dsh-skins 仓投稿清单
docs/shots/                 抽屉状态与层级验证图
tools/ofox_gen.py           OFOX 生图助手（生成 + 检查报告）
tools/matte.py              色度键控抠图：unmix → despill → alpha floor → despeckle
tools/prompts/              每个素材实际使用的提示词
tools/facade/               通过市场 facade 拍预览图 + 量布局数字
```

## 素材是怎么来的

每张位图都是 AI 生成后再本地处理；**没有**把任何照片、cosplay 图或第三方图片上传给模型（人物形象是纯文本描述的）。

1. **场景** —— OFOX images API 上的 `volcengine/doubao-seedream-5.0-pro`，不透明、画面中无人物：一张明亮的黄昏天台、一张霓虹夜景天际线。长边缩到 1920；亮色那张再补一点色彩与对比度（它出图偏惨白）。
2. **立绘** —— 同一模型，全身，画在纯品红 `#FF00FF` 平涂底上。再用本地 `tools/matte.py` 抠：从边框估计键色、按颜色距离生成 alpha 斜坡、解混（`F = (observed - (1 - a) * key) / a`）、去品红溢色、alpha 阈值，最后按连通域去噪。抠完实测溢色：3px 采样网格上分别是 38 与 50 个像素，可忽略。
3. 摘要、逐次提示词与每轮的检查报告都记录在 [docs/ART-PROVENANCE.md](docs/ART-PROVENANCE.md)。

## 验证

在投稿目标的检出里放入本皮肤后，本地门禁实跑结果：

| 门禁 | 结果 |
| --- | --- |
| `node scripts/dsh-skin.cjs validate skins/lucy-nightsignal` | PASS |
| `node scripts/skin-hooks-registry.mjs --check` | OK（无 hooks facet，注册表无漂移） |
| `pnpm skin-center:check` | OK（54 套目录皮肤全过） |
| `pnpm typecheck` | OK |
| `pnpm test` | 771 passed（52 个文件） |
| `pnpm build` | OK |
| `git diff --exit-code -- lib` | clean |

实机：安装并激活后，`GET /api/skin-center/v2/catalog` 列出本皮肤且无 diagnostics；`stylesheet` / `patches` 两条路由都返回 200（通过 CSS 安全管线）。亮/暗主题 × 左右抽屉开关四种组合均已确认。

## 已知取舍

- **不带 hooks**（原因见上）：所以立绘是跟着输入框走，而不是像女仆那套那样去量侧栏宽度。
- 锚点定位需要 Chrome 125+（本机 Chrome 154、WebView2 143）。每条锚点声明都配了按"侧栏展开"几何调的普通回退值，老引擎也能落位。
- `patches.css` 有几处匹配 CSS-Modules 哈希类名（`*_frame`、`*_sidebarCol`、`*_rightbarCol`、`*_centerCol`），`dsh-skin validate` 会因此给出 warning：官方重建后类名可能变化。
- 右栏展开时右立绘站在栏上。这是刻意取舍：另一种选择是让她消失，而那个布局里任何位置都免不了压到点什么。

## 许可与溯源

CC BY-NC-SA 4.0 —— 必须署名、非商业、相同方式共享。人物与世界观归其权利方所有；本作品为非官方同人，与 CD Projekt Red / Studio Trigger 无关。详见 [NOTICE](NOTICE) 与 [LICENSE](LICENSE)。
