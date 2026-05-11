"""情绪星云引擎 - 将心情转化为彩色星云

优先使用 AI 理解情绪，本地关键词匹配作为降级方案
"""

import random
from core.templates import get_mood_advice


# 情绪分类映射（本地降级方案）
MOOD_CATEGORIES = {
    "happy": ["开心", "快乐", "幸福", "高兴", "兴奋", "喜悦", "满足", "愉快", "欣喜"],
    "sad": ["忧郁", "难过", "伤心", "悲伤", "失落", "沮丧", "低落", "消沉", "惆怅"],
    "anxious": ["焦虑", "紧张", "不安", "担心", "忐忑", "烦躁", "急躁", "焦虑不安"],
    "calm": ["平静", "放松", "安宁", "从容", "淡然", "宁静", "安详", "惬意"],
    "angry": ["愤怒", "生气", "恼火", "暴怒", "气愤", "发火", "不爽", "恼怒"],
    "default": [],
}


def classify_mood_local(mood_text: str) -> str:
    """本地关键词匹配分类（降级方案）"""
    mood_text = mood_text.strip().lower()

    for category, keywords in MOOD_CATEGORIES.items():
        if category == "default":
            continue
        for kw in keywords:
            if kw in mood_text:
                return category

    # 没有匹配到，用随机分配增加趣味
    return random.choice(["happy", "calm", "anxious", "sad"])


def classify_mood(mood_text: str, mimo_engine=None) -> str:
    """分类情绪，优先用 AI，降级到本地匹配"""
    if mimo_engine and mimo_engine.is_available():
        result = mimo_engine.understand_mood(mood_text)
        if result and result.get("category"):
            return result["category"], result.get("label"), result.get("advice")

    # 降级到本地
    category = classify_mood_local(mood_text)
    return category, None, None


def get_mood_label(category: str) -> str:
    """将情绪类别转为中文标签"""
    label_map = {
        "happy": random.choice(["开心", "快乐", "幸福"]),
        "sad": random.choice(["忧郁", "低落", "惆怅"]),
        "anxious": random.choice(["焦虑", "紧张", "不安"]),
        "calm": random.choice(["平静", "安宁", "从容"]),
        "angry": random.choice(["愤怒", "恼火", "不爽"]),
    }
    return label_map.get(category, "神秘")


def analyze_mood(mood_input: str, mimo_engine=None) -> dict:
    """分析心情输入，返回情绪信息

    Args:
        mood_input: 用户输入的心情文字
        mimo_engine: MiMo AI 引擎实例（可选）
    """
    # 尝试 AI 理解
    result = classify_mood(mood_input, mimo_engine)

    if isinstance(result, tuple):
        # AI 理解成功
        category, ai_label, ai_advice = result
        label = ai_label or get_mood_label(category)
        advice = ai_advice or get_mood_advice(category)
    else:
        # 本地匹配
        category = result
        label = get_mood_label(category)
        advice = get_mood_advice(category)

    return {
        "input": mood_input,
        "category": category,
        "label": label,
        "advice": advice,
    }
