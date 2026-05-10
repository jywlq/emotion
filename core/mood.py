"""情绪星云引擎 - 将心情转化为彩色星云"""

import random
from core.templates import get_mood_advice


# 情绪分类映射
MOOD_CATEGORIES = {
    "happy": ["开心", "快乐", "幸福", "高兴", "兴奋", "喜悦", "满足", "愉快", "欣喜"],
    "sad": ["忧郁", "难过", "伤心", "悲伤", "失落", "沮丧", "低落", "消沉", "惆怅"],
    "anxious": ["焦虑", "紧张", "不安", "担心", "忐忑", "烦躁", "急躁", "焦虑不安"],
    "calm": ["平静", "放松", "安宁", "从容", "淡然", "宁静", "安详", "惬意"],
    "angry": ["愤怒", "生气", "恼火", "暴怒", "气愤", "发火", "不爽", "恼怒"],
    "default": [],
}


def classify_mood(mood_text: str) -> str:
    """将用户输入的心情文本分类为情绪类别"""
    mood_text = mood_text.strip().lower()

    for category, keywords in MOOD_CATEGORIES.items():
        if category == "default":
            continue
        for kw in keywords:
            if kw in mood_text:
                return category

    # 没有匹配到，用随机分配增加趣味
    return random.choice(["happy", "calm", "anxious", "sad"])


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


def analyze_mood(mood_input: str) -> dict:
    """分析心情输入，返回情绪信息"""
    category = classify_mood(mood_input)
    label = get_mood_label(category)
    advice = get_mood_advice(category)

    return {
        "input": mood_input,
        "category": category,
        "label": label,
        "advice": advice,
    }
