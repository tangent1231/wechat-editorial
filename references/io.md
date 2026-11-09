# 输入及交付

命令：`python3 scripts/build.py article.json --brand brand.json --output output`。仅依赖 Python 3 标准库。brand 可省略，省略时不显示任何品牌、二维码或署名。

文章字段：title 必填；subtitle、meta、intro、cover、coverAlt、closing 可选；sections 为列表，每节含 title、paragraphs（段落字符串列表），可选 label、quote、attribution、bullets、images、links。图片项为 file、caption、alt，可加 role: ornament 让小图标以 28% 宽度显示；链接项为 url、label，url 限 http(s)。文章图片路径相对 article.json。

品牌字段：name、primary（#RRGGBB）、accent（预留给后续定制）、logo、website、qr、qrCaption、credits（逐行署名字符串列表）。Logo 与二维码路径相对 brand.json。未填不显示。品牌主色会替换各款强调色，深色封面使用固定深底保证白色标题可读；更深定制需要调整模板后检查对比度。

导出支持 PNG、JPG、WebP、GIF；SVG 装饰上传前使用库内 PNG 版本。已有媒体会复制到输出的 media 目录，正文 HTML 以内嵌图交付。图片能复制不代表能被目标编辑器保存。

示例是虚构的内容结构演示，不含实际公司信息。请将 examples/article.json 与 examples/brand.json 复制到项目，再填入真实素材。默认渲染器只识别这些字段；需更多语义组件时修改渲染器，不向 JSON 随意加不会生效的字段。

输出 preview.html、paste-check.html、十二款 HTML、article.md、media-manifest.json 和独立 media。HTML 是完整排版交付；Markdown 用于文字协作，图片使用相对路径。预览的折叠和图组不会带进静态导出。工作台不是素材编辑器；内容、图片顺序与品牌修改通过 JSON 后重新构建。

v0.2 构建依赖同目录的 layouts.py，预览样式来自 assets/preview.css。封面先后、图片与段落穿插、章节框架会保留在内联 HTML 中；多列拼图、装饰形状和折叠属于预览增强。工作台可切到黑白模式比较构图，也可查看无预览 CSS 的实际导出版式。

## v0.3 配图与动效字段

- `variantCovers`：可选，主题 ID 到图片路径的映射；未指定主题沿用 cover。只改变主视觉，不改正文。Markdown 使用 cover。
- `coverMotionSafe`：可选布尔值，默认 false。只对确认可装饰的首图设 true，允许工作台首图浮动。不会让导出图片带 CSS 动画。
- `coverOrnaments`：可选，主题 ID 到 `{ "file": "../assets/soft3d/keyboard-160.png", "alt": "AI 装饰插画 · 键盘" }` 的映射，标题后的装饰会保留到静态导出；浮动只在预览中。

以上路径均相对 article.json。新增素材还需要修改内容配置并重新构建，不会自动选择或下载外部图像。

## v0.4.0 公众号复制版

构建器使用 `layouts.py` 组织内容，再经 `export_html.py` 输出内联版本。工作台将设计 HTML 与 `exportHtml` 分开保存，默认展示后者，复制与下载也使用后者。`assets/clipboard.js` 被构建时内嵌，无需外部 JS 服务。默认字体为中文系统字体回退链，标题最大 32px、小标题最大 23px，正文沿用输入模板字号。动态方案可通过取消“公众号复制预览”勾选查看。详见 [富文本复制](rich-text-copy.md)。
