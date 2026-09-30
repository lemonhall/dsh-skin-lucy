# 露西·夜城信号 — DSH 皮肤

[English](README.md) | 中文

一套给 DeepSeek Harness Web GUI 用的赛博朋克同人皮肤：亮色是白天云海之上的未来都市天台，暗色是霓虹雨雾中的夜之城天际线，两侧各立一位银白波波头、发尾彩虹渐变的网络黑客立绘。以纯资产目录的形式分发，由皮肤中心（或创意工坊）装进 `$DSH_HOME/skins/lucy-nightsignal/`。

## 目录

```
skins/lucy-nightsignal/     皮肤本体 —— 被安装的就是这个目录
  skin.json                 清单 v2（id、配色元数据、贡献项）
  skin.css                  L1 token 重映射（亮色挂 :root，暗色挂 body[data-ds-dark-theme]）
  patches.css               L3 自由选择器：两层立绘 + 霓虹描边
  assets/                   scene-light / scene-dark / lucy-signal-left / lucy-signal-right
  preview/                  light.jpg + dark.jpg，1440x900 JPEG q85
docs/ART-PROVENANCE.md      模型、提示词、摘要与抠图配方
tools/                      生成与抠图脚本
```

## 安装

把这个皮肤目录放进去（或让创意工坊一键装）：

```sh
git clone https://github.com/lemonhall/dsh-skin-lucy
Copy-Item -Recurse dsh-skin-lucy/skins/lucy-nightsignal "$env:USERPROFILE\.dsh\skins\"
```

然后打开 设置 → 皮肤中心（或创意工坊卡片），选「露西·夜城信号」。不需要重启，也不用刷新页面：皮肤中心在卡片打开时重扫 `$DSH_HOME/skins`。

## 实现要点

- **token 优先**：`skin.css` 只重映射官方 `--dsw-*` token，所有面板跟随皮肤，不写脆弱选择器。
- **声明式立绘**：两张立绘由 `patches.css` 的 `body:before` / `body:after` 绘制，**没有** `hooks.mjs`——因为市场预览渲染器从不执行皮肤 hooks，只靠 hooks 画的场景在商店预览里根本不会出现。`body` 上的 `isolation: isolate` 保证宿主的 `backgroundMedia` 层（z-index -2，挂在 body 上）在负 z-index 立绘层之后依然可见。
- **AI 素材 + 本地处理**：两张立绘在纯品红底上生成后，本地做色度键控、去溢色与去噪；场景保持不透明。提示词与摘要见 `docs/ART-PROVENANCE.md`。

## 预览图

`preview/light.jpg` 与 `preview/dark.jpg` 是应用本皮肤后运行中 GUI 的真实 1440x900 截图：用 Playwright 驱动 Chrome、deviceScaleFactor 1 拍摄，再存成 JPEG q85——与市场 `capture-previews` 写出的规格一致。

## 许可

CC BY-NC-SA 4.0。非官方同人作品，见 [NOTICE](NOTICE)。
