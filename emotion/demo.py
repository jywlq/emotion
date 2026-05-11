#!/usr/bin/env python3
"""
Cosmic Brew - 自动演示模式
无需用户交互，自动展示所有功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

from rich.console import Console
from ui.welcome import show_welcome
from ui.menu import show_drink_served
from ui.display import render_constellation, render_personality_reading, render_mood_nebula, render_dream_reading
from core.personality import PersonalityEngine
from core.mood import analyze_mood
from core.dream import analyze_dream
from core.templates import get_dream_coordinates, format_dream_coordinates
import json
import time

console = Console()

def demo():
    console.clear()
    
    # 1. 欢迎界面
    console.print()
    console.print("  ✧ ･ ｡ ☆ ･ ｡ ✧ ･ ｡ ☆ ･ ｡ ✧ ･ ｡ ☆")
    console.print("  ╔════════════════════════════════════╗")
    console.print("  ║   ☕  C O S M I C   B R E W  ☕    ║")
    console.print("  ║       宇  宙  咖  啡  馆           ║")
    console.print("  ║    ✦ 一杯咖啡，探索内心宇宙 ✦      ║")
    console.print("  ╚════════════════════════════════════╝")
    console.print("  ✧ ･ ｡ ☆ ･ ｡ ✧ ･ ｡ ☆ ･ ｡ ✧ ･ ｡ ☆")
    console.print()
    console.print("  [bold cyan]欢迎光临~ 我是你的宇宙咖啡师 🌟[/bold cyan]")
    console.print("  [dim]在这里，每一杯咖啡都藏着星辰的秘密[/dim]")
    console.print()
    time.sleep(1)

    # 2. 点单
    with open(os.path.join(_DATA_DIR, 'drinks.json'), 'r', encoding='utf-8') as _f:
        drinks = json.load(_f)
    drink = drinks[0]  # 银河拿铁
    show_drink_served(drink)
    time.sleep(1)

    # 3. 星座解读
    console.print()
    console.print("[bold magenta]🔮 星座解读[/bold magenta]")
    engine = PersonalityEngine()
    engine.add_drink(drink)
    # 模拟回答三个问题
    with open(os.path.join(_DATA_DIR, 'questions.json'), 'r', encoding='utf-8') as _f:
            questions = json.load(_f)
    engine.add_answer(questions[0], 0)
    engine.add_answer(questions[1], 1)
    engine.add_answer(questions[2], 2)
    scores = engine.get_scores()
    archetype = engine.get_archetype()
    constellation = engine.get_star_constellation()
    render_constellation(constellation, scores, archetype)
    render_personality_reading(scores, archetype)
    time.sleep(1)

    # 4. 情绪星云
    console.print()
    console.print("[bold magenta]🌙 情绪星云[/bold magenta]")
    result = analyze_mood('开心')
    render_mood_nebula(result['label'], result['advice'])
    time.sleep(1)

    # 5. 梦境解读
    console.print()
    console.print("[bold magenta]🌌 梦境坐标[/bold magenta]")
    # 模拟等待动画
    frames = ["正在连接宇宙信号", "正在连接宇宙信号.", "正在连接宇宙信号..", "正在连接宇宙信号..."]
    for f in frames:
        console.print(f"\r  🌌 {f}", end="")
        time.sleep(0.3)
    console.print()
    dream_result = analyze_dream('我在星空中飞翔，遇到一只发光的蝴蝶')
    render_dream_reading(
        symbols_found=dream_result['readings'],
        readings=[r['reading'] for r in dream_result['readings']],
        coordinates_str=dream_result['coordinates']
    )

    # 6. 告别
    console.print()
    console.print("[bold cyan]  愿星辰与你同行 ✨[/bold cyan]")
    console.print("[dim]  下次再来宇宙咖啡馆坐坐~[/dim]")
    console.print()

if __name__ == "__main__":
    demo()
