#!/usr/bin/env python3
"""
☕ Cosmic Brew 星咖占卜
一杯咖啡的时间，探索内心的宇宙

Usage: python cosmic_brew.py
"""

import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from ui.welcome import show_welcome
from ui.menu import choose_drink, show_drink_served, choose_action
from ui.display import (
    render_constellation,
    render_personality_reading,
    render_mood_nebula,
    render_dream_reading,
)
from core.personality import PersonalityEngine, ask_personality_questions, TRAIT_NAMES
from core.mood import analyze_mood
from core.dream import analyze_dream, show_reading_animation
from ai.local_engine import LocalEngine
from ai.gemini_engine import GeminiEngine

console = Console()

# 初始化AI引擎
local_engine = LocalEngine()
gemini_engine = GeminiEngine()


def get_active_engine():
    """获取当前可用的AI引擎（Gemini 优先，本地保底）"""
    if gemini_engine.is_available():
        return gemini_engine
    return local_engine


def run_personality(drink: dict):
    """运行星座解读流程"""
    console.print()
    console.print("[bold magenta]🔮 星座解读[/bold magenta]")
    console.print("[dim]  让我来读取你的星象...[/dim]")
    console.print()

    # 步骤1：问答
    engine = ask_personality_questions(drink)
    scores = engine.get_scores()
    archetype = engine.get_archetype()

    # 步骤2：匹配星座图案
    constellation = engine.get_star_constellation()

    # 步骤3：渲染星座图
    render_constellation(constellation, scores, archetype)

    # 步骤4：渲染性格解读
    # 尝试使用 Gemini 增强解读
    active = get_active_engine()
    if active is gemini_engine:
        gemini_reading = gemini_engine.generate_personality_reading(scores, archetype)
        if gemini_reading:
            content = f"""
[bold magenta]═══════ 深层解读 (Gemini) ═══════[/bold magenta]

  [italic]"{gemini_reading}"[/italic]

[dim]  —— 宇宙咖啡师 🌟 via Gemini[/dim]
"""
            console.print(Panel(content.strip(), border_style="yellow", padding=(1, 2)))
        else:
            render_personality_reading(scores, archetype)
    else:
        render_personality_reading(scores, archetype)

    console.print()
    console.print("[dim]  按下回车继续...[/dim]", end="")
    input()


def run_mood():
    """运行情绪星云流程"""
    console.print()
    console.print("[bold magenta]🌙 情绪星云[/bold magenta]")
    console.print("[dim]  告诉我你今天的心情，让我看看你的星云是什么颜色[/dim]")
    console.print()

    mood_input = input("  今天的心情是: ").strip()
    if not mood_input:
        mood_input = "平静"

    # 分析情绪
    result = analyze_mood(mood_input)

    # 尝试 Gemini 增强解读
    active = get_active_engine()
    if active is gemini_engine:
        enhanced_advice = gemini_engine.generate_mood_reading(mood_input, result["category"])
        if enhanced_advice:
            result["advice"] = enhanced_advice

    # 渲染星云
    render_mood_nebula(result["label"], result["advice"])

    console.print()
    console.print("[dim]  按下回车继续...[/dim]", end="")
    input()


def run_dream():
    """运行梦境解读流程"""
    console.print()
    console.print("[bold magenta]🌌 梦境坐标[/bold magenta]")
    console.print("[dim]  描述你最近的梦境，宇宙咖啡师来帮你解码[/dim]")
    console.print()

    dream_input = input("  你的梦境是: ").strip()
    if not dream_input:
        dream_input = "我在一片星空中漂浮"

    # 仪式感等待动画
    show_reading_animation()

    # 分析梦境
    result = analyze_dream(dream_input)

    # 尝试 Gemini 增强解读
    active = get_active_engine()
    if active is gemini_engine:
        for r in result["readings"]:
            enhanced = gemini_engine.generate_dream_reading(dream_input, r["meaning"])
            if enhanced:
                r["reading"] = enhanced

    # 渲染梦境解读
    render_dream_reading(
        symbols_found=result["readings"],
        readings=[r["reading"] for r in result["readings"]],
        coordinates_str=result["coordinates"],
    )

    console.print()
    console.print("[dim]  按下回车继续...[/dim]", end="")
    input()


def main():
    """主入口"""
    try:
        # 欢迎界面
        show_welcome()

        # 点单
        drink = choose_drink()
        show_drink_served(drink)

        # 主循环
        while True:
            action = choose_action()

            if action == "personality":
                run_personality(drink)
            elif action == "mood":
                run_mood()
            elif action == "dream":
                run_dream()
            elif action == "reorder":
                drink = choose_drink()
                show_drink_served(drink)
            elif action == "exit":
                break

        # 告别
        console.print()
        goodbye = Panel(
            "[bold cyan]愿星辰与你同行 ✨[/bold cyan]\n"
            "[dim]下次再来宇宙咖啡馆坐坐~[/dim]",
            border_style="magenta",
            padding=(1, 2),
        )
        console.print(Align.center(goodbye))
        console.print()

    except KeyboardInterrupt:
        console.print()
        console.print("[dim]  宇宙咖啡馆打烊了~ 下次再来 ☕✨[/dim]")
        sys.exit(0)


if __name__ == "__main__":
    main()
