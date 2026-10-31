# 截图字体（可选）

`body.html` 本身只用系统字体栈（苹方 / 微软雅黑 / 宋体），不依赖任何字体文件。
这里的字体**只用于本地截图**：在没有中文字体的 Linux / 容器里，把下面两个文件放进本目录（或用环境变量 `GZH_FONT_DIR` 指向所在目录），截图时会把「PingFang SC」「Songti SC」映射过去：

- `NotoSansSC.woff2`（思源黑体 / Noto Sans SC）
- `NotoSerifSC.woff2`（思源宋体 / Noto Serif SC）

两款均为 SIL Open Font License 1.1，可从 Google Fonts 下载。字体文件已在 `.gitignore` 中排除，不入库。
Mac / Windows 本机已有中文字体，可以不放。
