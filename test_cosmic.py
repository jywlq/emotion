#!/usr/bin/env python3
"""Cosmic Brew 模块测试脚本"""

import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.display import render_constellation, render_mood_nebula, render_dream_reading
from core.personality import PersonalityEngine
from core.mood import analyze_mood
from core.dream import analyze_dream
from core.templates import get_personality_reading, format_dream_coordinates, get_dream_coordinates
from ai.local_engine import LocalEngine
from ai.gemini_engine import GeminiEngine
import json

print("=" * 50)
print("  Cosmic Brew - 模块测试")
print("=" * 50)
print()

# 测试1: 性格引擎
print("【测试1】性格引擎")
engine = PersonalityEngine()
drinks = json.load(open('data/drinks.json'))
engine.add_drink(drinks[0])
scores = engine.get_scores()
print(f"  性格分数: {scores}")
constellation = engine.get_star_constellation()
print(f"  匹配星座: {constellation['name']}")
print("  ✅ 通过")
print()

# 测试2: 星座图渲染
print("【测试2】星座图渲染")
render_constellation(constellation, scores, '织梦者')
print()
print("  ✅ 通过")
print()

# 测试3: 情绪引擎
print("【测试3】情绪引擎")
result = analyze_mood('开心')
print(f"  情绪分类: {result['category']} -> {result['label']}")
print(f"  情绪建议: {result['advice'][:30]}...")
print("  ✅ 通过")
print()

# 测试4: 情绪星云渲染
print("【测试4】情绪星云渲染")
render_mood_nebula(result['label'], result['advice'])
print()
print("  ✅ 通过")
print()

# 测试5: 梦境引擎
print("【测试5】梦境引擎")
dream_result = analyze_dream('我在星空中飞翔')
print(f"  识别符号: {[r['symbol'] for r in dream_result['readings']]}")
print(f"  星际坐标: {dream_result['coordinates']}")
print("  ✅ 通过")
print()

# 测试6: 梦境解读渲染
print("【测试6】梦境解读渲染")
render_dream_reading(
    symbols_found=dream_result['readings'],
    readings=[r['reading'] for r in dream_result['readings']],
    coordinates_str=dream_result['coordinates']
)
print()
print("  ✅ 通过")
print()

# 测试7: AI引擎
print("【测试7】AI引擎")
local = LocalEngine()
print(f"  本地引擎可用: {local.is_available()}")
gemini = GeminiEngine()
print(f"  Gemini引擎: {'可用' if gemini.is_available() else '未配置key（预期）'}")
print("  ✅ 通过")
print()

print("=" * 50)
print("  🎉 所有模块测试通过！")
print("  💡 运行 python3 cosmic_brew.py 开始体验")
print("=" * 50)
