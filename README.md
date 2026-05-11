# ☕ Cosmic Brew 星咖占卜

> 一杯咖啡的时间，探索内心的宇宙 ✨

一个基于 Python 的终端交互项目——走进虚拟的「宇宙咖啡馆」，让 AI 咖啡师为你解读性格、分析梦境、生成专属情绪星云。

---

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/jywlq/emotion.git
cd emotion

# 安装依赖
pip install -r requirements.txt

# 运行
python cosmic_brew.py
```

不需要注册、不需要 API key，装完依赖直接跑。

Windows 用户也可以双击 `启动.bat` 直接启动。

---

## 功能

### 星座解读
选择一杯星空饮品，回答 3 个趣味问题，获得：
- 五维性格分析（温柔 / 创造力 / 直觉 / 探索 / 神秘）
- 专属 ASCII 星座图
- AI 生成的性格解读
- **AI 追问对话**（接入 API 后）：咖啡师会根据你的回答追问，挖掘更深层性格

### 情绪星云
输入今日心情，程序会识别情绪类别，用彩色 ASCII 艺术将你的情绪可视化——开心的星云是金橙色的，忧郁的则是蓝紫色。

- **接入 API 后**：AI 能理解任意表达（"有点emo""心累""hh"都能识别），不再局限于关键词匹配

### 梦境坐标
描述一个梦境，AI 会匹配梦境中的象征符号（飞翔→自由、水→情感、星星→希望…），并以「星际坐标」的格式输出解读。

---

## AI 引擎

项目采用多层引擎架构，兼顾零门槛和深度体验：

| 引擎 | 说明 |
|------|------|
| **本地规则引擎**（默认） | 100+ 解读模板，通过排列组合产生个性化输出，无需任何配置 |
| **MiMo 引擎**（推荐） | 接入小米 MiMo API，支持 AI 解读、情绪理解、追问对话 |
| **Gemini 引擎**（可选） | 设置 `GEMINI_API_KEY` 环境变量后启用 |

### 启用 MiMo AI

在程序内选择「⚙️ MiMo AI 设置」，按提示输入 API Key 即可。

也可以手动配置：

```bash
# 安装依赖
pip install openai

# 设置环境变量
export MIMO_API_KEY="你的key"

python cosmic_brew.py
```

获取 API Key：https://mimo-v2.com/settings/api-keys

**可选模型：**

| 模型 | 说明 |
|------|------|
| `mimo-v2-pro` | 平衡性能，推荐 |
| `mimo-v2.5-pro` | 最强，支持深度思考 |

在程序内可以随时切换模型。

### 启用 Gemini（可选）

```bash
pip install google-generativeai
export GEMINI_API_KEY="你的key"
python cosmic_brew.py
```

---

## 项目结构

```
cosmic-brew/
├── cosmic_brew.py          # 主入口
├── 启动.bat                # Windows 启动器
├── demo.py                # 自动演示脚本（无需交互）
├── requirements.txt
├── ui/
│   ├── welcome.py         # 星空欢迎界面 + 动画
│   ├── menu.py            # 交互式菜单
│   ├── display.py        # 星座图 / 星云 / 解读渲染
│   └── transitions.py    # 过场动画
├── core/
│   ├── personality.py     # 性格计算引擎 + AI 追问
│   ├── dream.py           # 梦境解读引擎
│   ├── mood.py            # 情绪分析引擎（AI 优先 / 本地降级）
│   └── templates.py      # 解读文本模板库
├── ai/
│   ├── local_engine.py    # 本地规则引擎
│   ├── mimo_engine.py    # MiMo API 引擎
│   └── gemini_engine.py  # Gemini API 引擎（可选）
└── data/
    ├── drinks.json        # 饮品数据 & 性格映射
    ├── questions.json     # 趣味问答库
    ├── dream_symbols.json # 梦境象征词典
    └── star_patterns.json # ASCII 星座图案库
```

---

## 技术栈

- **Python 3.8+**
- **[rich](https://github.com/Textualize/rich)** — 终端美化
- **[openai](https://github.com/openai/openai-python)** — MiMo API 兼容层
- **Google Gemini API**（可选）— AI 解读增强

---

## 扩展方向

| 扩展 | 说明 |
|------|------|
| 每日宇宙运势 | 基于历史记录生成趣味运势 |
| 星历档案 | 用 SQLite 存储历史，查看「宇宙足迹」 |
| 社交分享 | 生成可复制的文本卡片 |
| 新饮品 / 新问答 | 直接编辑 `data/` 目录下的 JSON 文件 |

---

## License

MIT
