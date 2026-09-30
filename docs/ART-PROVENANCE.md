# Art provenance — Lucy · Night City Signal

All raster assets were generated through the OFOX image API (endpoint
`POST https://api.ofox.ai/v1/images/generations`) and processed locally
with `tools/ofox_gen.py` and `tools/matte.py`. No photograph, cosplay image
or other third-party picture was sent to the provider; the character design
was described in text only.

## Generation runs

### run-03-bg-light

- model: `openai/gpt-image-2.5-sunburst`
- note: first light background attempt (character in scene) - superseded
- file: `image-0.png` — 2660750 bytes, sha256 `2df0b5fe951d66f554c25f99a366a3d666c5b7c224f7d72681afec9461fcb6ce`
- inspected: 1792x1024 RGB, alpha=False
- prompt:

  ```text
  Wide cinematic 16:9 anime illustration: bright hazy daytime view from a high rooftop in a futuristic megacity, pale white and light-cyan glass towers dissolving into soft sunlight and thin clouds. The left third is calm open sky and distant haze with plenty of empty bright space; on the right side, seen from behind at a three-quarter angle and medium distance, a young woman in a white cropped jacket over a black outfit stands looking out over the city, chin-length silver-white bob with pastel rainbow tips. Soft pastel palette of white, pale cyan and light gold, clean line art, cinematic depth of field, gentle bloom. No text, no letters, no watermark, no logo, no signature.
  ```

### run-04-bg-dark

- model: `openai/gpt-image-2.5-sunburst`
- note: first dark background attempt (character in scene) - superseded
- file: `image-0.png` — 2947468 bytes, sha256 `7061c1ffb025886e778e6aa532585298fc0d12bd0f81bc22f2fff70696d58d95`
- inspected: 1792x1024 RGB, alpha=False
- prompt:

  ```text
  Wide cinematic 16:9 anime illustration: night view from a high rooftop in a neon cyberpunk megacity, deep indigo sky, glowing cyan and magenta holographic light, distant grids of yellow windows, rain-slick haze and drifting fog. The left third is calm dark sky with plenty of empty space; on the right side, seen from behind at a three-quarter angle and medium distance, a young woman in a white cropped jacket over a black outfit stands looking out at the city, chin-length silver-white bob with pastel rainbow tips. Moody high-contrast lighting, strong cyan and magenta rim light, atmospheric depth. No text, no letters, no readable signage, no watermark, no logo, no signature.
  ```

### sd-run-01-cutout-right

- model: `volcengine/doubao-seedream-5.0-pro`
- note: right portrait, front view, flat magenta plate
- file: `image-0.png` — 4925104 bytes, sha256 `956357fb7e9f48c5dd83f824a4de239aded10491b36369b8a908ba6225d28a45`
- inspected: 1664x2496 RGB, alpha=False
- prompt:

  ```text
  动漫插画全身立绘，一位年轻女性网络黑客，正面站姿，全身从头到脚完整入画，身形修长。银白色齐下巴波波头，发尾带粉紫青的柔和彩虹渐变，蓝色大眼睛，冷静自信的表情。身穿白色短款夹克，内搭黑色紧身连体战衣，胸前有红色细丝带装饰，肩部镂空露出双肩，腰间黑色腰带配大腿绑带与小包，脚穿黑色漆皮长靴带红色细节。颈部与锁骨处有淡淡的发光义体线路。干净的赛璐璐上色，青色与洋红轮廓光，线条清晰锐利，人物居中，四周留出空白边距。整幅图的背景必须是单一的纯品红（#FF00FF）平涂，绝对不要场景、地面、阴影、渐变、文字或其他物体。
  ```

### sd-run-02-cutout-left

- model: `volcengine/doubao-seedream-5.0-pro`
- note: left portrait, back view, flat magenta plate
- file: `image-0.png` — 4956507 bytes, sha256 `b56270cd956026fa746cb841f996b03f028cb85b7407f82fafae3ea17c4b038d`
- inspected: 1664x2496 RGB, alpha=False
- prompt:

  ```text
  动漫插画全身立绘，同一位年轻女性网络黑客，背对镜头、回头看向观众，全身从头到脚完整入画，身形修长。银白色齐下巴波波头，发尾带粉紫青的柔和彩虹渐变，蓝色大眼睛，神情冷静。身穿白色短款夹克，内搭黑色紧身连体战衣，肩部镂空，腰间黑色腰带与大腿绑带，脚穿黑色漆皮长靴带红色细节。背部有淡淡的发光义体接口线路。干净的赛璐璐上色，青色与洋红轮廓光，线条清晰锐利，人物居中，四周留出空白边距。整幅图的背景必须是单一的纯品红（#FF00FF）平涂，绝对不要场景、地面、阴影、渐变、文字或其他物体。
  ```

### sd-run-03-bg-light

- model: `volcengine/doubao-seedream-5.0-pro`
- note: light scene attempt (character in scene) - superseded
- file: `image-0.png` — 5978205 bytes, sha256 `5db7ec6ff0e5c696327130e2032222acb5fba4dc07dfd2db68c13965d9e49e66`
- inspected: 2496x1664 RGB, alpha=False
- prompt:

  ```text
  宽幅电影感动漫插画，16:9。白天，未来大都市高处的天台视野，白与淡青色的玻璃高塔没入柔和阳光与薄云中。画面左侧三分之一是安静的开阔天空与远景薄雾，留出大片明亮的空白；画面右侧站着一位银白色齐下巴波波头、发尾带柔和彩虹渐变的年轻女性，背对镜头四分之三角度、中景距离，穿白色短款夹克与黑色服装，望着城市。柔和的粉白、淡青与浅金色调，干净的线条，电影级景深，轻微泛光。不要文字、不要字母、不要水印、不要签名。
  ```

### sd-run-04-bg-dark

- model: `volcengine/doubao-seedream-5.0-pro`
- note: dark scene attempt (character in scene) - superseded
- file: `image-0.png` — 6668267 bytes, sha256 `09a1b6200b7f3bb1abbfdb2582c0e08e5f78e6e24f458ec626fda10f153ac5dd`
- inspected: 2496x1664 RGB, alpha=False
- prompt:

  ```text
  宽幅电影感动漫插画，16:9。夜晚，霓虹赛博朋克大都市高处的天台视野，深靛蓝夜空，青与洋红的全息霓虹辉光，远处成片暖黄窗格，湿漉漉的地面反光与流动雾气。画面左侧三分之一是安静的深色天幕，留出大片空白；画面右侧站着一位银白色齐下巴波波头、发尾带柔和彩虹渐变的年轻女性，背对镜头四分之三角度、中景距离，穿白色短款夹克与黑色服装，俯瞰城市。强烈青洋红轮廓光，高对比度，浓厚的大气纵深。不要文字、不要字母、不要可辨识的招牌文字、不要水印、不要签名。
  ```

### sd-run-05-scene-light

- model: `volcengine/doubao-seedream-5.0-pro`
- note: light scene attempt (came back too high-key to read under a light scrim) - superseded
- file: `image-0.png` — 5934204 bytes, sha256 `c2abd3ef42b5b20169021594dd589d1245f87ca99cc3a41dd0691667252a89f8`
- inspected: 2496x1664 RGB, alpha=False
- prompt:

  ```text
  宽幅电影感动漫插画，16:9。白天，未来大都市高处的天台视野，白与淡青色的玻璃高塔没入柔和阳光与薄云中。画面左侧三分之一是安静的开阔天空与远景薄雾，留出大片明亮的空白；画面右侧站着一位银白色齐下巴波波头、发尾带柔和彩虹渐变的年轻女性，背对镜头四分之三角度、中景距离，穿白色短款夹克与黑色服装，望着城市。柔和的粉白、淡青与浅金色调，干净的线条，电影级景深，轻微泛光。不要文字、不要字母、不要水印、不要签名。
  ```

### sd-run-06-scene-dark

- model: `volcengine/doubao-seedream-5.0-pro`
- note: FINAL dark background, people-free
- file: `image-0.png` — 7083459 bytes, sha256 `4c7b868a9ec6e9e359cf6facb42d008bfe59ab5964faca43b8c9484b83c2a0da`
- inspected: 2496x1664 RGB, alpha=False
- prompt:

  ```text
  宽幅电影感动漫插画，16:9。夜晚，霓虹赛博朋克大都市高处的天台视野，深靛蓝夜空，青与洋红的全息霓虹辉光，远处成片暖黄窗格，湿漉漉的地面反光与流动雾气。画面左侧三分之一是安静的深色天幕，留出大片空白；画面右侧站着一位银白色齐下巴波波头、发尾带柔和彩虹渐变的年轻女性，背对镜头四分之三角度、中景距离，穿白色短款夹克与黑色服装，俯瞰城市。强烈青洋红轮廓光，高对比度，浓厚的大气纵深。不要文字、不要字母、不要可辨识的招牌文字、不要水印、不要签名。
  ```

### sd-run-07-scene-light-v2

- model: `volcengine/doubao-seedream-5.0-pro`
- note: FINAL light background, people-free, blue-hour colour depth
- file: `image-0.png` — 7027832 bytes, sha256 `91e2f866e7e68c464c20a5efb55731bc062a2cc83b6133a3ef1222aef2be5936`
- inspected: 2496x1664 RGB, alpha=False
- prompt:

  ```text
  宽幅电影感动漫插画，16:9。黄昏蓝调时刻的一座未来大都市天台视野：覆盖薄云的天空同时有青蓝与暖金两色层次，白与青色的玻璃高塔群，云层被夕阳染成金粉色，远处海湾大桥与水面反光，近景是干净的玻璃护栏天台地面。画面里绝对不要出现任何人物、动物或人影。左侧三分之一留出大片相对干净的天空，整体明亮通透但要有充足的对比与色彩层次，不要一片惨白。干净的线条，电影级景深，轻微泛光。不要文字、不要字母、不要水印、不要签名。
  ```

## Local matting (chroma key)

Recipe implemented in `tools/matte.py`, order matters —
estimate the key colour from the image border (median), ramp alpha on the
Euclidean distance to that key, unmix the colour
(`F = (observed - (1 - a) * key) / a`), despill the magenta excess on
partial-alpha pixels, apply the alpha floor (40) and finally a connected-
component despeckle (minimum area 64).

| run | source | matted | shipped as |
| --- | --- | --- | --- |
| `lzsd-run-01-cutout-right` | `sd-run-01-cutout-right/image-0.png` | `matte/right.png` key=[247.0, 11.0, 213.0] (border-median), transparent=0.679, partial=21235 | `assets/lucy-signal-right.webp` |
| `lzsd-run-02-cutout-left` | `sd-run-02-cutout-left/image-0.png` | `matte/left.png` key=[246.0, 10.0, 187.0] (border-median), transparent=0.525, partial=16673 | `assets/lucy-signal-left.webp` |

## Shipped assets

| file | size | bytes | role |
| --- | --- | --- | --- |
| `scene-light.webp` | 1920x1280 | 280238 | backgroundMedia.light |
| `scene-dark.webp` | 1920x1280 | 226890 | backgroundMedia.dark |
| `lucy-signal-left.webp` | 609x1800 | 189226 | patches.css body:before (back view) |
| `lucy-signal-right.webp` | 915x1800 | 189602 | patches.css body:after (front view) |

## Licence

CC BY-NC-SA 4.0 — attribution required, non-commercial, share-alike. The
depicted character remains the property of its rights holders.
