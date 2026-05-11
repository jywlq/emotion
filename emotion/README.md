# 🌌 Cosmic Brew 宇宙咖啡馆

> 一杯来自宇宙的时光，探索内心的星辰大海 ✨

一个 Python 终端交互式 AI 应用——将「宇宙咖啡馆」伪装成沉浸式体验空间，内置 AI 咖啡师为你进行人格占卜、心情分析和星座解梦。

**关键词：MiMo API · 多轮推理 · AI Agent 架构 · 长链路对话 · 情感计算**

---

## ✨ 核心亮点

- **多 Agent 模块化架构** — 人格分析、心情感知、解梦三大独立 Agent 模块，各自构建完整的"输入→AI 推理→增强输出"推理链路
- **长链推理（Multi-step Reasoning）** — 人格分析单次流程涉及 3-6 次 API 调用：测评→追问生成→用户回应→洞察提取→综合报告，全部携带完整上下文
- **三级引擎降级策略** — MiMo API → Gemini → 本地模板引擎，保证在任何网络环境下均可运行
- **全链路用量追踪** — 内置 Logger 模块，每次 API 调用自动记录 Token 消耗、延迟和成功率
- **100% 本地优先** — 无需 API Key 即可使用本地模板引擎，安装即跑

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/jywlq/emotion.git
cd emotion

# 安装依赖
pip install -r requirements.txt

# 运行（无需 API Key 即可体验）
python cosmic_brew.py
```

Windows 用户也可双击 `启动.bat` 直接运行。

---

## 🎮 功能模块

### 🔮 人格占卜（核心模块）

1. 选择一杯宇宙饮品（每种饮品映射不同性格基底）
2. 回答 3 道趣味心理测评题（5 维度：温柔 / 创造力 / 直觉 / 探索 / 神秘）
3. **AI 追问式深度对话**（接入 MiMo API 时）— 咖啡师根据你的每道回答实时追问，深入挖掘性格洞察
4. 多维度数据融合：饮品性格 + 测评得分 + 对话洞察 → 生成个性化占卜报告
5. 匹配专属 ASCII 星座图 + 原型称号（织梦者 / 星际骑士 / 寻找者 / 月影诗人）

**推理链路：**
```
饮品选择(性格基底) → 3道测评(5维打分) → MiMo追问Q1 → 用户作答 → MiMo洞察提取
→ MiMo追问Q2 → 用户作答 → MiMo洞察提取 → MiMo追问Q3 → 用户作答 → MiMo洞察提取
→ 全部上下文综合 → MiMo生成最终人格报告
```
> 单次完整流程：3-6 次 MiMo API 调用，每次均携带完整对话历史

### 🌈 心情星云

输入一段自然语言心情描述（支持非标准表达如"emo 了""hh""烦躁"）：
- **AI 模式**：MiMo 进行语义级别的情感理解与分类，生成上下文相关的个性化建议
- **本地模式**：关键词匹配分类 + 随机建议模板
- 渲染为对应情绪色彩的 ASCII 星云可视化

### 🌙 星座解梦

输入梦境描述 → 匹配梦境符号（10 类：水 / 飞翔 / 坠落 / 追逐 / 星空 / 动物 / 房子 / 陌生人 / 光 / 未知）→ MiMo AI 对每个符号进行上下文化深度解读 → 生成伪科学风格的「星历坐标」解梦报告

---

## 🤖 AI 引擎架构

项目采用三级引擎降级设计，确保在任何环境下都能运行：

```
┌─────────────────────────────────────────────────┐
│                   cosmic_brew.py                 │
│                 (主控 / 路由 / UI)                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐│
│  │ MiMo Engine │  │Gemini Engine│  │  Local   ││
│  │  (主引擎)    │  │  (备选引擎)  │  │  Engine  ││
│  │ mimo_engine │  │gemini_engine│  │local_eng ││
│  └──────┬──────┘  └──────┬──────┘  └────┬─────┘│
│         │                │               │      │
│    OpenAI 兼容       Gemini API      100+模板   │
│    (api.xiaomimimo)                             │
│         │                │               │      │
│  ┌──────┴────────────────┴───────────────┴─────┐│
│  │              core/logger.py                  ││
│  │         全链路 API 用量追踪                    ││
│  └─────────────────────────────────────────────┘│
├─────────────────────────────────────────────────┤
│              core/ (业务逻辑层)                    │
│  personality.py  mood.py  dream.py  templates.py  │
├─────────────────────────────────────────────────┤
│              ui/ (终端 UI 层)                      │
│  welcome.py  menu.py  display.py  transitions.py  │
└─────────────────────────────────────────────────┘
```

### 引擎优先级

| 优先级 | 引擎 | 说明 | API 调用 |
|--------|------|------|----------|
| 🥇 | **MiMo Engine** | 主引擎，支持全功能 | OpenAI 兼容协议 |
| 🥈 | Gemini Engine | 备选，无 MiMo Key 时启用 | Google Generative AI |
| 🥉 | Local Engine | 兜底，无网络时仍可运行 | 纯本地 100+ 模板 |

### 配置 MiMo AI

首次运行时选择「MiMo AI 设置」，按提示输入 API Key 即可。

也可手动配置：

```bash
# 安装 OpenAI SDK
pip install openai

# 设置环境变量
export MIMO_API_KEY="your-key"

python cosmic_brew.py
```

获取 API Key：https://mimo-v2.com/settings/api-keys

**可选模型：**

| 模型 | 说明 |
|------|------|
| `mimo-v2-flash` | 快速响应，日常使用（默认） |
| `mimo-v2-pro` | 均衡性能，推荐 |
| `mimo-v2.5-pro` | 增强推理能力 |

### 配置 Gemini（可选）

```bash
pip install google-generativeai
export GEMINI_API_KEY="your-key"
python cosmic_brew.py
```

---

## 📊 用量追踪

内置 Logger 模块（`core/logger.py`），自动记录所有 API 调用：

```python
from core.logger import get_session_stats, generate_report

# 查看今日统计
get_session_stats()
# → {'total_calls': 17, 'total_tokens': 3189, 'avg_latency_ms': 3046.3, ...}

# 生成 7 日报告
generate_report(7)
# → {'active_days': 5, 'total_calls': 87, 'total_tokens': 18240, ...}
```

日志格式（JSON Lines），存储于 `logs/session_YYYY-MM-DD.jsonl`：

```json
{
  "timestamp": "2026-05-11T17:30:00",
  "engine": "MiMo",
  "function": "generate_personality_reading",
  "prompt_tokens": 185,
  "completion_tokens": 113,
  "total_tokens": 298,
  "latency_ms": 5561.2,
  "success": true,
  "metadata": {"model": "mimo-v2-flash", "max_tokens": 512}
}
```

---

## 📁 项目结构

```
cosmic-brew/
├── cosmic_brew.py          # 主入口 / 路由 / 主循环
├── 启动.bat                # Windows 一键启动
├── demo.py                # 自动化演示脚本
├── test_cosmic.py         # 模块测试脚本
├── requirements.txt
├── logs/                  # API 用量日志（自动生成）
├── ui/                    # 终端 UI 层
│   ├── welcome.py         # 星空欢迎动画
│   ├── menu.py            # 交互式菜单
│   ├── display.py         # 星座图 / 星云 / 报告渲染
│   └── transitions.py     # 场景过渡动画
├── core/                  # 业务逻辑层
│   ├── personality.py     # 人格分析引擎 + AI 追问
│   ├── dream.py           # 解梦引擎
│   ├── mood.py            # 心情分析（AI 语义 / 本地关键词）
│   ├── templates.py       # 100+ 本地文本模板
│   └── logger.py          # 全链路 API 用量追踪
├── ai/                    # AI 引擎层
│   ├── local_engine.py    # 本地模板引擎（兜底）
│   ├── mimo_engine.py     # MiMo API 引擎（主）
│   └── gemini_engine.py   # Gemini API 引擎（备选）
└── data/                  # 数据文件
    ├── drinks.json        # 饮品数据 & 性格映射
    ├── questions.json     # 心理测评题库
    ├── dream_symbols.json # 梦境符号词典（10 类）
    └── star_patterns.json # ASCII 星座图（5 种）
```

---

## 🛠 技术栈

- **Python 3.8+**
- **[rich](https://github.com/Textualize/rich)** — 终端富文本渲染
- **[openai](https://github.com/openai/openai-python)** — MiMo API 兼容接入
- **[google-generativeai](https://ai.google.dev/)** — Gemini API 接入（可选）

---

## 🔮 设计理念

Cosmic Brew 的核心设计哲学是 **"AI 无感融入"**：

- 用户不需要知道背后有 AI 在运行——它只是一个"有趣的咖啡馆"
- API 调用被自然地嵌入到对话流程中，而不是简单地"输入问题→返回答案"
- 本地模板引擎保证了无网络时的完整体验，AI 是"增强"而非"必需"

---

## 📋 扩展计划

| 方向 | 说明 |
|------|------|
| 历史轨迹 | 用 SQLite 存储分析历史，查看性格变化趋势 |
| 社交卡片 | 生成可分享的精美文本卡片 |
| 语音交互 | 接入 TTS/STT 实现语音对话 |
| 自定义饮品/题库 | 直接编辑 `data/` 目录下的 JSON 文件 |
| 更多 AI 引擎 | 支持更多 OpenAI 兼容 API |

---

## License

MIT
