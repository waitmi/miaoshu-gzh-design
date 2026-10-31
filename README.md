# 喵叔说保 · 公众号排版（miaoshu-gzh-design）

保险科普公众号「喵叔说保」的排版 skill：把一篇文章按类型套进 7 套主题之一，生成**可直接粘贴进公众号编辑器**的 HTML（带一键复制按钮）、干净正文和手机预览长图，同时自动检查公众号平台限制与保险合规禁用词。

**原则：原文一字不改，只加结构与标签。** 构建时逐句比对原文，缺一句、改一字都会报出来。

![7 套主题总览](docs/previews/overview.jpg)

## 特点

- **7 套主题**，按文章类型分工：日常科普、测评读物、数据测算、清单指南、保单诊断、知识笔记、产品横评。
- **公众号兼容**：只用 section / p / span / table，样式全内联，文字统一 `<span leaf>` 包裹；不用 flex / grid / 定位 / 渐变 / 外部字体。
- **三道校验**：平台限制、保险合规禁用词（原文已有的只提示不改）、375px 手机版面自检（孤字、行首标点、越界、溢出）。
- **原文覆盖比对**：排版后的正文与原文逐句核对，保证不漏字、不改字。
- **给 Agent 用**：`SKILL.md` 是完整工作流，Agent 读文章 → 选主题让用户确认 → 写标记稿 → build → validate 0 ERROR → 交付。

## 7 套主题

### ① 喵叔蓝 · 科普卡片（`miaolan`）

- **适合文章**：日常主力：条款释义、避坑、医保选择、家庭场景
- **示例文章**：《同部位复发，第二笔重疾为什么一分不给》
- **核心组件**：海军蓝标题区、客户来问卡、条款原文卡＋人话、判据框、对比表、算一笔账＋双数据卡、避坑提醒、深蓝判断线

<img src="docs/previews/1-miaolan-palette.png" alt="① 喵叔蓝 · 科普卡片 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/1-miaolan-top.jpg" alt="① 喵叔蓝 · 科普卡片 首屏" width="300"> | <a href="docs/previews/1-miaolan-full.jpg"><img src="docs/previews/1-miaolan-full.jpg" alt="① 喵叔蓝 · 科普卡片 完整长图" width="120"></a><br>点击查看完整长图 |

### ② 暖纸编辑 · 测评风（`nuanzhi`）

- **适合文章**：案例复盘、观点长文、深度测评
- **示例文章**：《同部位复发，第二笔重疾为什么一分不给》
- **核心组件**：杂志式刊头（大期号）、牛皮纸案卷、宋体导语、大号章节号、荧光笔笔记卡、对比擂台表、打分进度条、宋体金句

<img src="docs/previews/2-nuanzhi-palette.png" alt="② 暖纸编辑 · 测评风 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/2-nuanzhi-top.jpg" alt="② 暖纸编辑 · 测评风 首屏" width="300"> | <a href="docs/previews/2-nuanzhi-full.jpg"><img src="docs/previews/2-nuanzhi-full.jpg" alt="② 暖纸编辑 · 测评风 完整长图" width="120"></a><br>点击查看完整长图 |

### ③ 深蓝鎏金 · 数据测算（`shenlan`）

- **适合文章**：养老 / 年金 / 分红 / 退休现金流 / 医保档位算账
- **示例文章**：《同部位复发，第二笔重疾为什么一分不给》
- **核心组件**：深蓝头图＋三格关键指标、PART 章节、条款规格卡、深色数据面板、深蓝算账板＋双格大数字、金字表头、金框判断线

<img src="docs/previews/3-shenlan-palette.png" alt="③ 深蓝鎏金 · 数据测算 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/3-shenlan-top.jpg" alt="③ 深蓝鎏金 · 数据测算 首屏" width="300"> | <a href="docs/previews/3-shenlan-full.jpg"><img src="docs/previews/3-shenlan-full.jpg" alt="③ 深蓝鎏金 · 数据测算 完整长图" width="120"></a><br>点击查看完整长图 |

### ④ IP蓝瑞士网格 · 清单指南（`wangge`）

- **适合文章**：选购指南、清单、「先看什么后看什么」
- **示例文章**：《同样叫0免赔，有的一款全额赔有的一款只报80%》
- **核心组件**：粗线刊头＋三格元信息、大号编号章节、数字网格 grid、粗细线表格、方头进度条、顺序清单 seq、编号条款卡

<img src="docs/previews/4-wangge-palette.png" alt="④ IP蓝瑞士网格 · 清单指南 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/4-wangge-top.jpg" alt="④ IP蓝瑞士网格 · 清单指南 首屏" width="300"> | <a href="docs/previews/4-wangge-full.jpg"><img src="docs/previews/4-wangge-full.jpg" alt="④ IP蓝瑞士网格 · 清单指南 完整长图" width="120"></a><br>点击查看完整长图 |

### ⑤ 保单体检报告单 · 诊断排查（`tijian`）

- **适合文章**：保单诊断、条款避坑排查、政策/条款原文逐段解读
- **示例文章**：《保证续保20年，保的只是不被单独踢出去》
- **核心组件**：报告单抬头＋图例、检验依据、检验项目表 report（✓/!/✕）、样本原文＋判读、红框异常标签 chips、计算单、诊断意见 Rx、体检结论

<img src="docs/previews/5-tijian-palette.png" alt="⑤ 保单体检报告单 · 诊断排查 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/5-tijian-top.jpg" alt="⑤ 保单体检报告单 · 诊断排查 首屏" width="300"> | <a href="docs/previews/5-tijian-full.jpg"><img src="docs/previews/5-tijian-full.jpg" alt="⑤ 保单体检报告单 · 诊断排查 完整长图" width="120"></a><br>点击查看完整长图 |

### ⑥ 黑板荧光笔 · 知识笔记（`heiban`）

- **适合文章**：医保怎么选、名词解释、一个公式讲清楚
- **示例文章**：《居民医保交一档还是二档，一次住院就能算清》
- **核心组件**：黑板头图、红圈序号章节、荧光半截划重点、便签名词卡、公式板 formula、黑板推演 calc（粉笔圈数字）、板书表、易错框

<img src="docs/previews/6-heiban-palette.png" alt="⑥ 黑板荧光笔 · 知识笔记 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/6-heiban-top.jpg" alt="⑥ 黑板荧光笔 · 知识笔记 首屏" width="300"> | <a href="docs/previews/6-heiban-full.jpg"><img src="docs/previews/6-heiban-full.jpg" alt="⑥ 黑板荧光笔 · 知识笔记 完整长图" width="120"></a><br>点击查看完整长图 |

### ⑦ 测评擂台 · 产品横评（`leitai`）

- **适合文章**：多款横评、两款 PK、单品拆解
- **示例文章**：《保费差不到100块的重疾险，赔的钱能差一半》
- **核心组件**：擂台黑头图＋同口径说明、ROUND 回合章节、选手卡 roster、红蓝对阵表 vs、单品卡 card、分项条、黑表头横评表、犯规提醒

<img src="docs/previews/7-leitai-palette.png" alt="⑦ 测评擂台 · 产品横评 色板" width="600">

| 首屏 | 完整长图 |
|---|---|
| <img src="docs/previews/7-leitai-top.jpg" alt="⑦ 测评擂台 · 产品横评 首屏" width="300"> | <a href="docs/previews/7-leitai-full.jpg"><img src="docs/previews/7-leitai-full.jpg" alt="⑦ 测评擂台 · 产品横评 完整长图" width="120"></a><br>点击查看完整长图 |

各主题的色板用法、字号、组件清单和配方表见 [docs/THEMES.md](docs/THEMES.md)。

## 快速开始

```bash
# 1. 安装依赖（Python 3.9+）
pip install -r requirements.txt
playwright install chromium        # 或设置 GZH_CHROMIUM=/path/to/chromium

# 2. 用示例标记稿出一套
python3 scripts/build.py tijian examples/保证续保.gzh.md

# 3. 7 套全出，对比效果
python3 scripts/build.py all examples/同部位复发.gzh.md

# 4. 排自己的文章：先拼标记稿，再带原文构建（原文覆盖比对 + 原文禁用词降级为提示）
python3 scripts/compose.py --dump 我的文章.md       # 看原文段落编号
python3 scripts/compose.py 我的文章.spec            # 生成 我的文章.gzh.md
python3 scripts/build.py miaolan 我的文章.gzh.md --src 我的文章.md --out output/我的文章
```

产物（默认在 `output/<标记稿名>/<主题id>/`）：

| 文件 | 用途 |
|---|---|
| `article.html` | 浏览器打开，点「复制到公众号」，到编辑器 Ctrl/⌘+V |
| `body.html` | 干净正文 HTML |
| `preview.png` | 375px 手机宽 2x 长图 |
| `check.txt` | 校验报告：ERROR / WARN、锚点次数、原文覆盖、版面自检 |

标记稿语法见 [templates/标记语法.md](templates/标记语法.md)，可从 [templates/示例标记稿.gzh.md](templates/示例标记稿.gzh.md) 起步。

## 目录结构

```
miaoshu-gzh-design/
├── SKILL.md              Agent 入口：工作流、分工表、平台限制、合规规则
├── README.md
├── LICENSE               MIT
├── requirements.txt
├── engine/               引擎
│   ├── parse.py          标记稿解析
│   ├── base.py           组件基类（内联样式、leaf 包裹、孤字保护、未知组件降级）
│   ├── builder.py        构建：标记稿 → body / article / preview / check
│   ├── checker.py        校验：平台限制、leaf、半角标点、禁用词、免责
│   ├── source.py         原文读取与覆盖比对
│   ├── shot.py           截图与 375px 版面自检
│   └── page.py           带复制按钮的预览页模板
├── themes/               7 套主题（④–⑦ 继承 ① 的组件并换色）
├── templates/            标记语法说明 + 示例标记稿
├── examples/             5 篇真实文章的标记稿
├── scripts/              build / validate / screenshot / compose / make_previews
├── docs/
│   ├── THEMES.md         主题详解与配方
│   └── previews/         首屏、长图、色板、总览图
└── fonts/                截图用中文字体说明（字体文件不入库）
```

## 主题分工表

| 文章类型 | 首选 | 备选 |
|---|---|---|
| 日常条款释义、家庭场景避坑 | ① 喵叔蓝 | ⑤ 体检报告单 |
| 选购指南、清单、「先看什么后看什么」 | ④ 瑞士网格 | ① 喵叔蓝 |
| 保单诊断、已买保单复查、免责排查 | ⑤ 体检报告单 | ① 喵叔蓝 |
| 政策/监管文件、条款原文逐段解读 | ⑤ 体检报告单 | ① 喵叔蓝 |
| 医保怎么选、名词解释、带公式的科普 | ⑥ 黑板荧光笔 | ③ 深蓝鎏金（纯算账时） |
| 多款产品横评、两款 PK | ⑦ 测评擂台 | ② 暖纸编辑（偏读物、偏故事时） |
| 案例复盘、观点长文、深度测评 | ② 暖纸编辑 | ⑦ 测评擂台 |
| 养老/年金/分红/退休现金流测算 | ③ 深蓝鎏金 | ⑥ 黑板荧光笔 |

建议主力保持 ①，每周按文章类型轮换 ④⑤⑥⑦ 中的一套，避免同一套连用超过 3 篇。

## 公众号平台限制

公众号编辑器会过滤大量 HTML/CSS，本项目从严执行，`validate` 违反即报 ERROR：

- 标签只用 `section / p / span / strong / em / br / img / table / tr / td`，不用 div、class、id、`<style>`、`<script>`；
- 样式全内联，不用 `position`、`float`、`flex / grid`、CSS 变量、外部字体、`@media`、动画；
- 不用渐变背景（容易在暗黑模式下被反色）；
- 所有文字包在 `<span leaf="">` 里，粘贴后不丢样式；
- 中文语境不用半角标点；
- 以 375px 手机宽检查孤字、行首标点、越界和容器溢出；正文最大宽度 677px；图片需在公众号后台重新上传。

## 保险合规

- **禁用词**：回本、取钱、利息、本金、保本、稳赚、零风险、收益 / 收益率 / 回报率、复利、比存款、停售 / 窗口期、最高、第一、唯一、排行榜、排名。排版新加的文字出现即 ERROR；**原文里本来就有的只在报告里列出，不改原文**，由作者决定是否改稿。
- **替换建议**：复利 → IRR；回本 → 现价超过已交保费；收益 → 利益 / 演示利益。
- **需人工确认**：保证续保、首选、最好、最值得、必买、闭眼。
- **免责必含**「以保险合同条款及核保结果为准」。

## 致谢

- 方法论参考 [isjiamu/gzh-design-skill](https://github.com/isjiamu/gzh-design-skill)（克制用色、按文章类型配方、平台限制清单、校验思路），**代码独立编写**，未复制其代码。
- 截图字体使用思源黑体 / 思源宋体（Noto Sans SC / Noto Serif SC，SIL OFL 1.1），不随仓库分发。

## 许可

代码与主题以 [MIT](LICENSE) 许可发布。`examples/` 中的文章内容版权归「喵叔说保」所有，仅作排版示例；文中产品仅作条款举例，不构成任何购买推荐。

## 关于作者 / 联系喵叔

这套排版是喵叔给自己的公众号「喵叔说保」做的，开源出来，希望别的行业也能直接用上。用的时候遇到问题、想定制一套自己行业的主题，或者想聊内容合作，都欢迎来找我。

<p align="center"><img src="assets/brand/contact-card.jpg" alt="喵叔联系方式名片" width="720"></p>

<table align="center">
  <tr>
    <td align="center" width="50%"><img src="assets/brand/gzh-qr.png" alt="公众号「喵叔说保」二维码" width="200"></td>
    <td align="center" width="50%"><img src="assets/brand/reward-qr.png" alt="赞赏码" width="200"></td>
  </tr>
  <tr>
    <td align="center"><b>关注公众号「喵叔说保」</b><br>看这套排版在真实文章里的样子</td>
    <td align="center"><b>觉得有用，请喵叔喝杯咖啡</b><br>微信扫码赞赏，随意就好</td>
  </tr>
</table>

<p align="center">名片上的二维码是喵叔的个人微信：各行业的公众号排版、内容合作都可以聊，加好友时备注「GitHub」。</p>
