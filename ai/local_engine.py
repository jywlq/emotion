"""本地规则引擎 - 零配置的AI解读引擎"""

import random
from core.templates import (
    get_personality_reading,
    get_archetype_description,
    get_mood_advice,
    get_dream_coordinates,
    format_dream_coordinates,
)


class LocalEngine:
    """基于规则和模板的本地AI引擎"""

    def __init__(self):
        self.name = "本地宇宙引擎"

    def is_available(self) -> bool:
        """本地引擎始终可用"""
        return True

    def generate_personality_reading(self, scores: dict, archetype: str) -> str:
        """生成本地性格解读"""
        readings = []
        for trait, score in scores.items():
            reading = get_personality_reading(trait, score)
            readings.append(f"**{trait}**: {reading}")

        archetype_desc = get_archetype_description(archetype)

        combined = "\n\n".join(readings)
        return f"{combined}\n\n**{archetype}**: {archetype_desc}"

    def generate_dream_reading(self, dream_text: str, symbol_meaning: str) -> str:
        """生成本地梦境解读（增强版）"""
        from core.dream import _generate_detail_text

        detail = _generate_detail_text(dream_text)
        templates = [
            f"在你的梦境中，{symbol_meaning}的符号正对你低语。{detail}——闭上眼，让这个梦再停留一会儿，答案就在那些你还没来得及看清的细节里。",
            f"梦是宇宙写给你的加密信件。{symbol_meaning}的关键词已被破译。{detail}——试着在清醒时回忆梦中的感受，那才是真正的解码钥匙。",
            f"这个梦境的{symbol_meaning}维度格外活跃。{detail}——宇宙通过梦境传递的信息，永远比你以为的更温柔。",
        ]
        return random.choice(templates)

    def generate_mood_reading(self, mood: str, category: str) -> str:
        """生成本地情绪解读"""
        advice = get_mood_advice(category)

        extras = [
            "此刻的星象正在回应你的频率——",
            "宇宙的咖啡师看着你的星云说——",
            "今天的宇宙能量和你的心情共振了——",
        ]
        prefix = random.choice(extras)

        return f"{prefix}{advice}"
