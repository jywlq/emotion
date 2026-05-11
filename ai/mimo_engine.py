"""MiMo AI 引擎 - 基于 MiMo API 的深度解读引擎

兼容 OpenAI 格式，支持：
- 性格解读
- 情绪理解（AI 代替关键词匹配）
- 梦境解读
- 追问式对话

配置方式：
1. 设置环境变量 MIMO_API_KEY
2. 或在 data/config.json 中写入 api_key
"""

import os
import json
from rich.console import Console

console = Console()

# 默认配置
DEFAULT_BASE_URL = "https://api.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2-flash"

# 可用模型列表
AVAILABLE_MODELS = {
    "1": {"id": "mimo-v2-flash", "name": "MiMo-V2-Flash", "desc": "轻量快速，日常使用"},
    "2": {"id": "mimo-v2-pro", "name": "MiMo-V2-Pro", "desc": "旗舰模型，深度推理"},
}


def _load_config() -> dict:
    """从配置文件加载配置"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "config.json"
    )
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save_config(config: dict):
    """保存配置到文件"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "config.json"
    )
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


class MiMoEngine:
    """MiMo AI 引擎"""

    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        self.name = "MiMo AI 引擎"
        self._api_key = api_key or os.environ.get("MIMO_API_KEY", "")
        self._model = model or DEFAULT_MODEL
        self._base_url = base_url or DEFAULT_BASE_URL
        self._client = None

        # 尝试从配置文件读取
        if not self._api_key:
            config = _load_config()
            self._api_key = config.get("api_key", "")
            self._model = config.get("model", DEFAULT_MODEL)
            self._base_url = config.get("base_url", DEFAULT_BASE_URL)

        # 自动修复旧地址
        old_urls = ["https://api.mimo-v2.com/v1", "https://api.mimov2.com/v1"]
        if self._base_url in old_urls:
            self._base_url = DEFAULT_BASE_URL
            if self._api_key:
                _save_config({"api_key": self._api_key, "model": self._model, "base_url": self._base_url})

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = value
        self._client = None  # 重置客户端

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        self._model = value
        self._client = None

    def is_available(self) -> bool:
        """检查 API 是否可用"""
        return bool(self._api_key)

    def _get_client(self):
        """延迟初始化 OpenAI 兼容客户端"""
        if self._client is None:
            try:
                from openai import OpenAI

                self._client = OpenAI(
                    api_key=self._api_key,
                    base_url=self._base_url,
                )
            except ImportError:
                console.print("[dim]  提示: 安装 openai 包可启用 MiMo AI (pip install openai)[/dim]")
                return None
        return self._client

    def _chat(self, system_prompt: str, user_message: str, max_tokens: int = 512) -> str:
        """发送聊天请求，返回文本"""
        client = self._get_client()
        if client is None:
            return None

        try:
            response = client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens,
                temperature=0.9,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
            return None
        except Exception as e:
            error_msg = str(e)
            console.print(f"[dim]  [MiMo] 请求异常: {error_msg[:80]}[/dim]")
            return None

    # ===== 性格解读 =====

    def generate_personality_reading(self, scores: dict, archetype: str) -> str:
        """AI 生成性格解读"""
        stars_display = "\n".join(
            f"- {trait}: {'★' * score}{'☆' * (5 - score)}"
            for trait, score in scores.items()
        )

        system_prompt = """你是一位宇宙咖啡馆的咖啡师，用温暖、诗意、有洞察力的语言解读性格。
你擅长用宇宙、星空、星云、黑洞等天文意象来比喻人的内心世界。
你的解读让人感到被理解，而不是被评判。"""

        user_message = f"""请为以下性格生成一段解读（150字左右）：

性格维度：
{stars_display}

原型：{archetype}

要求：
- 用宇宙/星空的比喻
- 温暖有洞察力
- 不要用列表格式，用连贯段落
- 让人感到被理解"""

        return self._chat(system_prompt, user_message)

    # ===== 情绪理解 =====

    def understand_mood(self, mood_input: str) -> dict:
        """AI 理解用户情绪，返回分类和建议"""
        system_prompt = """你是一位温柔的心理观察者，擅长理解人们的情绪。
你需要判断用户的心情属于哪个类别，并给出温暖的回复。"""

        user_message = f"""用户说今天的心情是：「{mood_input}」

请判断情绪类别，只返回以下之一：happy, sad, anxious, calm, angry
然后给出一个中文的情绪标签（2-3个字）和一句温暖的建议（30字以内）。

请严格按以下格式返回，不要多余文字：
类别: xxx
标签: xxx
建议: xxx"""

        response = self._chat(system_prompt, user_message, max_tokens=200)
        if not response:
            return None

        try:
            lines = response.strip().split("\n")
            result = {}
            for line in lines:
                if line.startswith("类别:"):
                    result["category"] = line.split(":", 1)[1].strip()
                elif line.startswith("标签:"):
                    result["label"] = line.split(":", 1)[1].strip()
                elif line.startswith("建议:"):
                    result["advice"] = line.split(":", 1)[1].strip()

            # 验证分类是否合法
            valid_categories = ["happy", "sad", "anxious", "calm", "angry"]
            if result.get("category") not in valid_categories:
                return None

            return result
        except Exception:
            return None

    # ===== 梦境解读 =====

    def generate_dream_reading(self, dream_text: str, symbol_meaning: str) -> str:
        """AI 生成梦境解读"""
        system_prompt = """你是一位宇宙咖啡馆的咖啡师，擅长解读梦境。
你用温暖、诗意的方式解读，喜欢用宇宙、星空的比喻。
你的解读让人感到安心，而不是害怕。"""

        user_message = f"""请解读以下梦境：

梦境描述：{dream_text}
识别到的象征维度：{symbol_meaning}

要求：
- 150字左右
- 用宇宙/星空的比喻
- 温暖有诗意
- 让人感到安心"""

        return self._chat(system_prompt, user_message)

    # ===== 追问式对话 =====

    def generate_followup_question(self, question: str, answer: str, question_num: int) -> str:
        """根据用户的回答，生成追问"""
        system_prompt = """你是一位宇宙咖啡馆的咖啡师，正在和客人聊天来了解ta的性格。
你擅长通过追问挖掘更深层的性格特质。
你的追问简短自然，像朋友聊天一样，不超过20个字。"""

        user_message = f"""客人回答了第{question_num}个问题：
问题：{question}
回答：{answer}

请根据ta的回答，追问一个简短的问题，挖掘更深层的性格。不超过20个字。"""

        response = self._chat(system_prompt, user_message, max_tokens=100)
        return response

    def generate_followup_reading(self, question: str, answer: str, followup: str, followup_answer: str) -> str:
        """根据追问的回答，生成一句简短洞察"""
        system_prompt = """你是一位宇宙咖啡馆的咖啡师，善于从对话中捕捉性格线索。
你用一句话总结你的洞察，温暖而精准。"""

        user_message = f"""对话记录：
Q: {question}
A: {answer}
追问: {followup}
回答: {followup_answer}

请用一句话（不超过25字）总结你对这位客人的性格洞察。"""

        return self._chat(system_prompt, user_message, max_tokens=80)


# ===== 配置管理 =====

def setup_mimo_engine() -> MiMoEngine:
    """交互式设置 MiMo 引擎"""
    engine = MiMoEngine()

    # 如果已有配置，直接返回
    if engine.is_available():
        return engine

    console.print()
    console.print("[bold cyan]  🔧 首次使用 MiMo AI，需要配置 API Key[/bold cyan]")
    console.print("[dim]  获取 Key: https://mimo-v2.com/settings/api-keys[/dim]")
    console.print("[dim]  留空则使用本地引擎（无需 API）[/dim]")
    console.print()

    api_key = input("  请输入 MiMo API Key: ").strip()

    if not api_key:
        console.print("  [dim]已跳过，将使用本地引擎[/dim]")
        return engine

    # 选择模型
    console.print()
    console.print("  [bold]选择模型:[/bold]")
    for key, model in AVAILABLE_MODELS.items():
        console.print(f"    [cyan]{key}[/cyan]. {model['name']} — {model['desc']}")
    console.print()

    while True:
        choice = input("  请输入编号 (1-2, 默认1): ").strip()
        if choice in AVAILABLE_MODELS:
            engine.model = AVAILABLE_MODELS[choice]["id"]
            break
        elif choice == "" or choice == "1":
            engine.model = DEFAULT_MODEL
            break
        else:
            console.print("  [dim]请输入 1 或 2[/dim]")

    engine.api_key = api_key

    # 保存配置
    _save_config({
        "api_key": api_key,
        "model": engine.model,
        "base_url": engine._base_url,
    })

    console.print()
    console.print(f"  [bold green]✓ MiMo AI 配置完成 (模型: {engine.model})[/bold green]")
    console.print("  [dim]配置已保存，下次无需重新设置[/dim]")

    return engine


if __name__ == "__main__":
    # 测试
    engine = MiMoEngine()
    if engine.is_available():
        print("MiMo 引擎可用")
        result = engine.understand_mood("有点emo")
        print(f"情绪理解: {result}")
    else:
        print("MiMo 引擎未配置")
