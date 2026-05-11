"""Gemini AI引擎 - 可选的深度解读增强"""

import os
import time
from core.logger import log_api_call


class GeminiEngine:
    """基于 Google Gemini API 的AI引擎（可选增强）"""

    def __init__(self):
        self.name = "Gemini 宇宙引擎"
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self._client = None

    def is_available(self) -> bool:
        """检查 Gemini API 是否可用"""
        return bool(self.api_key)

    def _get_client(self):
        """延迟初始化 Gemini 客户端"""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel("gemini-2.0-flash")
            except ImportError:
                print("  [dim]提示: 安装 google-generativeai 包可启用 Gemini 增强[/dim]")
                return None
        return self._client

    def generate_personality_reading(self, scores: dict, archetype: str) -> str:
        """使用 Gemini 生成深度性格解读"""
        client = self._get_client()
        if client is None:
            return None

        prompt = f"""你是一位宇宙咖啡馆的咖啡师，用温暖、诗意、有洞察力的语言解读性格。

用户的五维性格分数（1-5星）：
- 温柔: {'★' * scores['温柔']}{'☆' * (5 - scores['温柔'])}
- 创造力: {'★' * scores['创造力']}{'☆' * (5 - scores['创造力'])}
- 直觉: {'★' * scores['直觉']}{'☆' * (5 - scores['直觉'])}
- 探索: {'★' * scores['探索']}{'☆' * (5 - scores['探索'])}
- 神秘: {'★' * scores['神秘']}{'☆' * (5 - scores['神秘'])}

原型: {archetype}

请写一段150字左右的性格解读，用宇宙/星空的比喻，温暖有诗意。不要用列表格式，用连贯的段落。"""

        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return None

    def generate_dream_reading(self, dream_text: str, symbol_meaning: str) -> str:
        """使用 Gemini 生成深度梦境解读"""
        client = self._get_client()
        if client is None:
            return None

        prompt = f"""你是一位宇宙咖啡馆的咖啡师，擅长解读梦境。

用户描述的梦境: {dream_text}
识别到的象征维度: {symbol_meaning}

请用温暖、诗意的方式解读这个梦境，150字左右。用宇宙/星空的比喻。不要用列表格式。"""

        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return None

    def generate_mood_reading(self, mood: str, category: str) -> str:
        """使用 Gemini 生成情绪解读"""
        client = self._get_client()
        if client is None:
            return None

        prompt = f"""你是一位宇宙咖啡馆的咖啡师，正在安慰一位客人。

客人说今天的心情是: {mood}
情绪类别: {category}

请用温暖、诗意的方式给出建议和安慰，100字左右。用宇宙/星空的比喻。"""

        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return None
