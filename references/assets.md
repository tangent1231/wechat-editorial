# 素材库与扩充

内置 24 款原创线性 SVG 及透明 PNG，以及来自原 skill 的 4 款通用 AI 立体图标。没有客户 Logo、二维码或人物照片。清单见 `assets/icons/catalog.json`，AI 图标完整提示词见 `assets/soft3d/manifest.json`。

SVG 可改色；PNG 用于编辑器上传。生成或加工素材时保留原图与来源，不把栅格图伪称可编辑矢量图。图标只作为视觉提示，不替代事实和品牌标志。

## 按文章扩充素材

| 需要的风格 | 提示词方向 | 适合用途 |
|---|---|---|
| 柔和立体 | satin ceramic, frosted glass, soft studio lighting | 科技、活动 |
| 单色线描 | clean monoline, consistent stroke, simple silhouette | 商务、知识 |
| 剪纸拼贴 | layered paper, restrained shadows, tactile edges | 教育、生活 |
| 编辑插画 | flat editorial illustration, limited palette | 观点、企业文化 |
| 手绘水彩 | light watercolor, airy edges, subtle pigment | 生活、公益 |
| 几何等距 | isometric, precise geometry, minimal detail | 产品、技术 |
| 黑白版画 | monochrome engraving, high contrast | 人物、人文 |
| 材质静物 | realistic material study, clean negative space | 品牌、产品概念 |

以上是生成配方，并非已经生成八套素材。Agent 使用环境中的图像生成能力，按具体需求生成独立物件或横幅，并记录实际模型/工具可见信息；没有提供底层型号时不猜测。透明图标要求真实 alpha 通道，并检查在浅深底色及小尺寸下的效果。

素材记录至少有 id、文件、类型、用途、来源、图注；AI 素材另存提示词。照片归属、人物及客户资料的使用范围按本次授权处理。可搜索参考但不擅自将网络照片包装成可自由复用素材。

## v0.3 新增且已接入示例

`assets/editorial-art/` 有三组 AI 概念插画：玻璃科技共创、纸艺共创花园、自然材质静物。每组包含生成原始 PNG 与轻量 JPG；manifest.json 保留完整提示词，模型未由工具返回，不填造型号。它们不是现场照片。12 款 demo 根据主题分配主视觉，正文配图示范三种材质；技术、课堂、活动与发布主题另使用透明小素材。

`assets/gallery.html` 是可直接打开的素材入口。`assets/motion/` 有信号线与轨道两款独立 GIF / PNG，生成脚本可复用；尚未在秀米或微信验证。浏览器的慢动背景和首图浮动详见 [动效规范](motion.md)。
