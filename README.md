# Workbook Go

Workbook Go 是一个可定制的儿童练字纸生成器。现在主要用于生成汉字练习 PDF：输入要练习的汉字，程序会按照笔顺生成田字格、参考字、笔画提示和描写练习格。

## 可以做什么

- 生成可打印的汉字练字 PDF。
- 每行格子数量可调，格子会随之变大或变小。
- 支持 `us_letter` 和 `a4` 两种纸张。
- 支持三种练习模式：
  - 模式 1：参考字 + 逐笔提示 + 描写格。
  - 模式 2：参考字 + 逐笔提示 + 空白练习格。
  - 模式 3：参考字 + 描写格，不显示逐笔过程。
- 可设置每份练习页重复几次。
- 不指定输出文件名时，会自动生成带日期的 PDF 文件名。

## 安装

需要 Python 3.11 或更新版本。

```bash
cd chinese_chars
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

生成 PDF 需要系统里有可用的中文字体。如果运行时报字体相关错误，请安装常见中文字体，例如 Noto CJK、Uming 或 Ukai。

## 基本用法

生成“一二三四五”的练习纸，每行 5 个格子，并保存到指定文件：

```bash
cd chinese_chars
chinese-chars 一二三四五 -n 5 -o output/practice.pdf
```

也可以这样运行：

```bash
python -m chinese_chars 一二三四五 -n 5 -o output/practice.pdf
```

如果不写 `-o`，程序会在当前目录生成类似这样的文件：

```text
practice_20260709.pdf
```

如果同名文件已经存在，会自动改成：

```text
practice_20260709_1.pdf
practice_20260709_2.pdf
```

## 常用例子

生成默认练习纸：

```bash
chinese-chars 永
```

每行 6 个格子，使用 A4 纸：

```bash
chinese-chars 春夏秋冬 -n 6 --paper a4
```

生成描写格模式，不显示逐笔提示：

```bash
chinese-chars 山川日月 --mode 3
```

每页重复 3 份：

```bash
chinese-chars 一二三 -k 3
```

## 参数说明

```text
chars                 要练习的汉字，例如 一二三
-n, -c, --density    每行格子数，默认 5
-p, --paper          纸张大小：us_letter 或 a4，默认 us_letter
-m, --mode           练习模式：1、2、3，默认 1
-k, --copies         每份练习页重复次数，默认 2
-o, --output         输出 PDF 文件路径
-v, --version        显示版本号
```

## 练习模式

### 模式 1：参考字 + 笔画提示 + 描写格

这是默认模式。每个字先显示一个黑色参考字，然后按笔顺逐格增加笔画，后面的格子显示完整浅灰字形，适合照着描。

```bash
chinese-chars 永 --mode 1
```

### 模式 2：参考字 + 笔画提示 + 空白格

每个字先显示参考字和逐笔提示，后面留空白田字格，适合已经熟悉字形后自己写。

```bash
chinese-chars 永 --mode 2
```

### 模式 3：参考字 + 描写格

不显示逐笔过程，直接给参考字和完整浅灰字形，适合大量描写练习。

```bash
chinese-chars 永 --mode 3
```

## 格子和排版

每个格子是田字格样式。外框和中心辅助线会打印出来，方便孩子对齐结构。

`-n` 或 `--density` 决定每行多少个格子：

- 数字越小，格子越大。
- 数字越大，一页能放的内容越多。

如果一个字的笔画很多，占用超过一行，内容会继续排到下一行；如果当前页放不下，会自动进入下一页。

## 注意事项

- 只能生成仓库里已有笔画数据的汉字。
- 输出目录需要已经存在；例如使用 `-o output/practice.pdf` 时，请先确保 `output/` 目录存在。
- PDF 渲染依赖系统中文字体。缺字体时，参考字可能无法正常显示。
