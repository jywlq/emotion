# Architecture

> Cosmic Brew 的技术架构文档

## 系统概览

Cosmic Brew 采用**分层模块化架构**，将 UI 展示、业务逻辑和 AI 引擎完全解耦。核心设计思想是"本地优先、AI 增强"——基础体验不依赖任何外部 API，AI 作为增强层叠加在本地逻辑之上。

---

## 分层架构

### Layer 1: UI 层 (`ui/`)

负责所有终端交互和视觉效果渲染。

| 模块 | 职责 |
|------|------|
| `welcome.py` | 启动时的星空动画和欢迎语 |
| `menu.py` | 饮品选择、操作菜单的交互式输入 |
| `display.py` | 星座图、星云、报告的富文本渲染 |
| `transitions.py` | 场景切换时的过渡动画（打字机效果、渐入渐出） |

技术依赖：[rich](https://github.com/Textualize/rich) 库。

### Layer 2: 业务逻辑层 (`core/`)

纯逻辑层，不直接调用任何 AI API，通过 `ai/` 层的接口进行 AI 调用。

#### `personality.py` — 人格分析引擎

核心推理流程：

```
1. 用户选择饮品 → 饮品.traits 映射为初始人格分数
2. 3 道测评题 → 用户选择 → 选项.traits 累加到分数
3. [可选] 每道题后 AI 追问 → 用户自由作答 → AI 提取洞察
4. 5 维度分数归一化(1-5) → 匹配星座图 → 确定原型称号
5. [可选] AI 综合所有数据生成最终人格报告
```

数据模型：

- `PersonalityEngine`：维护一个 `scores` 字典 `{维度: 累计分数}` + `followup_insights` 列表
- 5 个维度：温柔、创造力、直觉、探索、神秘
- 4 种原型：织梦者、星际骑士、寻找者、月影诗人
- 5 种星座图：织梦者(Dreamweaver)、星际者(Starseer)、探索者(Pathfinder)、月影者(Moonshadow)、深渊行者(Abysswalker)

#### `mood.py` — 心情分析引擎

双模式设计：

- **本地模式**：关键词匹配 → 分类（happy/sad/anxious/calm/angry）→ 模板建议
- **AI 模式**：MiMo 进行语义理解 → 分类 + 标签 + 个性化建议

本地关键词库覆盖：开心、幸福、喜悦、emo、烦躁、焦虑、平静、愤怒等 50+ 关键词。

#### `dream.py` — 解梦引擎

```
用户梦境文本 → 关键词匹配 10 类梦境符号 → 每个符号获取模板 + AI 增强 → 生成星历坐标报告
```

符号词典（`dream_symbols.json`）：水、飞翔、坠落、追逐、星空、动物、房子、陌生人、光 + 默认兜底。

#### `logger.py` — 用量追踪

JSON Lines 格式日志，记录每次 API 调用的完整元数据。支持日报和周报统计。

### Layer 3: AI 引擎层 (`ai/`)

统一的引擎接口设计，每个引擎实现相同的方法签名：

```python
class BaseEngine:
    def is_available(self) -> bool        # 检测是否可用
    def generate_personality_reading(scores, archetype) -> str
    def generate_dream_reading(dream_text, symbol_meaning) -> str
    def generate_mood_reading(mood, category) -> str
```

#### `mimo_engine.py` — MiMo API（主引擎）

- 基于 OpenAI 兼容协议接入 `api.xiaomimimo.com`
- **独有功能**：追问式对话（`generate_followup_question` + `generate_followup_reading`）
- 支持模型切换（mimo-v2-flash / mimo-v2-pro / mimo-v2.5-pro）
- 配置持久化到 `data/config.json`
- 内置自动迁移旧 API 地址

Prompt 工程：

| 功能 | System Prompt 设计 |
|------|-------------------|
| 人格报告 | 角色扮演为"宇宙咖啡馆咖啡师"，要求温暖诗意有洞察力 |
| 追问生成 | 基于"多轮对话深入了解性格"，控制在 20 字以内 |
| 洞察提取 | "一句话总结性格洞见"，控制在 25 字以内 |
| 心情分析 | "判断情绪类别并给出温暖建议"，结构化输出 |
| 解梦解读 | "温暖诗意方式解读梦境"，150 字以内 |

#### `local_engine.py` — 本地引擎（兜底）

100+ 文本模板，按维度 × 等级组织。随机组合生成报告，无需网络。

#### `gemini_engine.py` — Gemini API（备选）

与 MiMo 相同的方法签名，作为第二优先级引擎。通过 `google-generativeai` SDK 接入。

### 引擎降级策略

```python
def get_active_engine():
    if mimo_engine and mimo_engine.is_available():
        return mimo_engine      # 🥇 MiMo
    if gemini_engine.is_available():
        return gemini_engine    # 🥈 Gemini
    return local_engine         # 🥉 本地兜底
```

降级是静默的——用户只会注意到 AI 报告变成了模板报告，不会看到任何错误提示。

---

## 数据流

### 人格分析完整数据流

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  饮品选择  │────▶│  测评打分  │────▶│  AI 追问  │
│(性格基底) │     │(5维累加)  │     │(3轮对话)  │
└──────────┘     └──────────┘     └──────────┘
       │               │               │
       ▼               ▼               ▼
┌──────────────────────────────────────────────┐
│              多维度数据融合                     │
│  饮品性格 + 测评分数 + 对话洞察 → 5维归一化     │
└──────────────────┬───────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │星座图匹配│ │原型确定  │ │AI报告生成│
   │(ASCII)  │ │(4选1)   │ │(MiMo)   │
   └─────────┘ └─────────┘ └─────────┘
```

### API 调用链路（单次人格分析）

```
MiMo.generate_personality_reading(scores, archetype)     # 1 call
MiMo.generate_followup_question(q1, a1)                  # 1 call
MiMo.generate_followup_reading(q1, a1, f1, fa1)          # 1 call
MiMo.generate_followup_question(q2, a2)                  # 1 call
MiMo.generate_followup_reading(q2, a2, f2, fa2)          # 1 call
MiMo.generate_followup_question(q3, a3)                  # 1 call
MiMo.generate_followup_reading(q3, a3, f3, fa3)          # 1 call
─────────────────────────────────────────────────────────
Total: 7 MiMo API calls (完整流程) / 1 call (无追问)
```

---

## 配置

| 配置项 | 位置 | 说明 |
|--------|------|------|
| MiMo API Key | `data/config.json` 或 `MIMO_API_KEY` 环境变量 | 运行时自动保存 |
| MiMo 模型 | `data/config.json` 或设置菜单 | 默认 `mimo-v2-flash` |
| Gemini API Key | `GEMINI_API_KEY` 环境变量 | 仅环境变量 |
| 饮品数据 | `data/drinks.json` | 可直接编辑扩展 |
| 测评题库 | `data/questions.json` | 可直接编辑扩展 |
| 梦境符号 | `data/dream_symbols.json` | 可直接编辑扩展 |
| 用量日志 | `logs/session_YYYY-MM-DD.jsonl` | 自动生成 |

---

## 扩展指南

### 添加新的 AI 引擎

1. 在 `ai/` 下创建新文件，实现 `BaseEngine` 接口
2. 在 `cosmic_brew.py` 的 `get_active_engine()` 中添加降级逻辑
3. 在 `get_active_engine()` 中按优先级插入

### 添加新功能模块

1. 在 `core/` 下创建业务逻辑
2. 在 `ui/` 下创建渲染函数
3. 在 `cosmic_brew.py` 主循环中添加入口
4. 按需在 `ai/` 各引擎中添加对应的 AI 增强方法
