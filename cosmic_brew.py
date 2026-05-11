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
from ui.transitions import (
    transition_to_menu,
    transition_to_reading,
    transition_question_pause,
    transition_drink_complete,
    transition_goodbye,
)
from core.personality import PersonalityEngine, ask_personality_questions, TRAIT_NAMES
from core.mood import analyze_mood
from core.dream import analyze_dream, show_reading_animation
from ai.local_engine import LocalEngine
from ai.gemini_engine import GeminiEngine
from ai.mimo_engine import MiMoEngine, setup_mimo_engine

console = Console()

# 初始化AI引擎
local_engine = LocalEngine()
gemini_engine = GeminiEngine()
mimo_engine = None  # 延迟初始化，需要时再配置


def get_active_engine():
    """获取当前可用的AI引擎（MiMo > Gemini > 本地）"""
    global mimo_engine
    if mimo_engine and mimo_engine.is_available():
        console.print("[dim]  [调试] 使用 MiMo AI 引擎[/dim]")
        return mimo_engine
    if gemini_engine.is_available():
        console.print("[dim]  [调试] 使用 Gemini 引擎[/dim]")
        return gemini_engine
    console.print("[dim]  [调试] 使用本地引擎（未接入API）[/dim]")
    return local_engine


def run_personality(drink: dict):
    """运行星座解读流程"""
    # 过场：进入解读前的过渡
    transition_to_reading("personality")

    console.print("[bold magenta]🔮 星座解读[/bold magenta]")
    console.print("[dim]  让我来读取你的星象...[/dim]")
    console.print()

    # 步骤1：问答（带 AI 追问）
    engine = ask_personality_questions(
        drink,
        pause_callback=transition_question_pause,
        mimo_engine=mimo_engine,
    )
    scores = engine.get_scores()
    archetype = engine.get_archetype()

    # 过场：问答结束 → 生成解读
    transition_to_reading("personality")

    # 步骤2：匹配星座图案
    constellation = engine.get_star_constellation()

    # 步骤3：渲染星座图
    render_constellation(constellation, scores, archetype)

    # 步骤4：渲染性格解读
    active = get_active_engine()
    if active is mimo_engine:
        # MiMo 解读
        ai_reading = mimo_engine.generate_personality_reading(scores, archetype)
        if ai_reading:
            # 如果有追问洞察，也展示
            insights_text = ""
            if engine.followup_insights:
                insights = "\n".join(f"  · {ins}" for ins in engine.followup_insights)
                insights_text = f"\n\n[bold cyan]─── 对话中的发现 ───[/bold cyan]\n{insights}\n"

            content = f"""
[bold magenta]═══════ AI 深层解读 (MiMo) ═══════[/bold magenta]

  [italic]"{ai_reading}"[/italic]
{insights_text}
[dim]  —— 宇宙咖啡师 🌟 via MiMo[/dim]
"""
            console.print(Panel(content.strip(), border_style="yellow", padding=(1, 2)))
        else:
            render_personality_reading(scores, archetype)
    elif active is gemini_engine:
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

    # 过场：回到菜单
    transition_to_menu()


def run_mood():
    """运行情绪星云流程"""
    console.print()
    console.print("[bold magenta]🌙 情绪星云[/bold magenta]")
    console.print("[dim]  告诉我你今天的心情，让我看看你的星云是什么颜色[/dim]")
    console.print()

    mood_input = input("  今天的心情是: ").strip()
    if not mood_input:
        mood_input = "平静"

    # 过场：情绪分析中的过渡
    transition_to_reading("mood")

    # 分析情绪（AI 优先，本地降级）
    result = analyze_mood(mood_input, mimo_engine=mimo_engine)

    # 如果 AI 没返回建议，尝试 Gemini
    if mimo_engine is None or not mimo_engine.is_available():
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

    # 过场：回到菜单
    transition_to_menu()


def run_dream():
    """运行梦境解读流程"""
    console.print()
    console.print("[bold magenta]🌌 梦境坐标[/bold magenta]")
    console.print("[dim]  描述你最近的梦境，宇宙咖啡师来帮你解码[/dim]")
    console.print()

    dream_input = input("  你的梦境是: ").strip()
    if not dream_input:
        dream_input = "我在一片星空中漂浮"

    # 过场：梦境解读的仪式感动画
    transition_to_reading("dream")

    # 分析梦境
    result = analyze_dream(dream_input)

    # 尝试 AI 增强解读
    active = get_active_engine()
    if active is mimo_engine:
        for r in result["readings"]:
            enhanced = mimo_engine.generate_dream_reading(dream_input, r["meaning"])
            if enhanced:
                r["reading"] = enhanced
    elif active is gemini_engine:
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

    # 过场：回到菜单
    transition_to_menu()


def run_settings():
    """MiMo AI 设置"""
    global mimo_engine
    from ai.mimo_engine import AVAILABLE_MODELS

    console.print()
    console.print("[bold magenta]⚙️ MiMo AI 设置[/bold magenta]")
    console.print()

    if mimo_engine and mimo_engine.is_available():
        console.print(f"  当前状态: [bold green]已连接[/bold green]")
        console.print(f"  当前模型: [cyan]{mimo_engine.model}[/cyan]")
        console.print()
        console.print("  [1] 更换 API Key")
        console.print("  [2] 更换模型")
        console.print("  [3] 断开 MiMo AI（使用本地引擎）")
        console.print("  [0] 返回")
        console.print()

        choice = input("  请选择: ").strip()

        if choice == "1":
            new_key = input("  新的 API Key: ").strip()
            if new_key:
                mimo_engine.api_key = new_key
                from ai.mimo_engine import _save_config
                _save_config({"api_key": new_key, "model": mimo_engine.model, "base_url": mimo_engine._base_url})
                console.print("  [bold green]✓ API Key 已更新[/bold green]")
        elif choice == "2":
            console.print()
            for key, model in AVAILABLE_MODELS.items():
                console.print(f"    [cyan]{key}[/cyan]. {model['name']} — {model['desc']}")
            model_choice = input("  请选择模型 (1-2): ").strip()
            if model_choice in AVAILABLE_MODELS:
                mimo_engine.model = AVAILABLE_MODELS[model_choice]["id"]
                from ai.mimo_engine import _save_config
                _save_config({"api_key": mimo_engine.api_key, "model": mimo_engine.model, "base_url": mimo_engine._base_url})
                console.print(f"  [bold green]✓ 已切换到 {mimo_engine.model}[/bold green]")
        elif choice == "3":
            mimo_engine = None
            console.print("  [dim]已断开 MiMo AI，使用本地引擎[/dim]")

        time.sleep(0.5)
    else:
        mimo_engine = setup_mimo_engine()

    transition_to_menu()


def main():
    """主入口"""
    global mimo_engine

    # 启动时尝试加载 MiMo 配置
    mimo_engine = MiMoEngine()

    try:
        # 欢迎界面
        show_welcome()

        # 点单
        drink = choose_drink()
        show_drink_served(drink)

        # 过场：咖啡完成
        transition_drink_complete(drink["name"])

        # 主循环
        while True:
            # 动态生成菜单（根据 AI 是否可用）
            if mimo_engine and mimo_engine.is_available():
                console.print()
                console.print("[bold magenta]✧ 今天想体验什么？[/bold magenta] [dim](MiMo AI 已连接)[/dim]")
            else:
                console.print()
                console.print("[bold magenta]✧ 今天想体验什么？[/bold magenta]")

            console.print()
            console.print("  [cyan]1[/cyan]. 🔮 星座解读 — 发现你的专属星座")
            console.print("  [cyan]2[/cyan]. 🌙 情绪星云 — 看看今天的心情星云")
            console.print("  [cyan]3[/cyan]. 🌌 梦境坐标 — 解读你的梦境")
            console.print("  [cyan]4[/cyan]. ☕ 重新点单 — 换一杯试试")
            console.print("  [cyan]5[/cyan]. ⚙️ MiMo AI 设置")
            console.print("  [cyan]6[/cyan]. 👋 离开咖啡馆")
            console.print()

            choice = input("  请输入编号 (1-6): ").strip()

            if choice == "1":
                run_personality(drink)
            elif choice == "2":
                run_mood()
            elif choice == "3":
                run_dream()
            elif choice == "4":
                drink = choose_drink()
                show_drink_served(drink)
                transition_drink_complete(drink["name"])
            elif choice == "5":
                run_settings()
            elif choice == "6":
                break
            else:
                console.print("  [dim]请输入 1-6 之间的数字~[/dim]")

        # 告别动画
        transition_goodbye()
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
