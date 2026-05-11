"""过场动画 - 功能切换之间的沉浸过渡"""

import time
import random
from rich.console import Console
from rich.text import Text
from rich.align import Align

console = Console()


def transition_to_menu():
    """从功能结果 → 返回主菜单的过渡"""
    console.print()

    lines = [
        ("  ✧ 星尘缓缓散去...", "dim magenta"),
        ("  ✧ 回到咖啡馆...", "dim cyan"),
    ]
    for text, style in lines:
        console.print(f"[{style}]{text}[/{style}]")
        time.sleep(0.5)

    # 短暂黑屏再清屏，制造"回到现实"的感觉
    time.sleep(0.3)
    console.clear()

    # 重新显示咖啡馆标志
    console.print()
    console.print("[bold magenta]  ☕ 宇宙咖啡馆[/bold magenta]")
    console.print("[dim]  ✧ 欢迎回来[/dim]")
    console.print()


def transition_to_reading(reading_type: str):
    """进入解读前的过渡动画
    
    Args:
        reading_type: "personality" | "mood" | "dream"
    """
    console.print()

    if reading_type == "personality":
        frames = [
            "  🔮 正在读取星象...",
            "  🔮 星光汇聚中...",
            "  🔮 星座轮廓浮现...",
        ]
    elif reading_type == "mood":
        frames = [
            "  🌙 正在感知你的频率...",
            "  🌙 星云色彩涌动...",
            "  🌙 情绪星云成形...",
        ]
    elif reading_type == "dream":
        frames = [
            "  🌌 正在连接宇宙信号...",
            "  🌌 接收梦境频率...",
            "  🌌 解码星际坐标...",
            "  🌌 信号已锁定 ✧",
        ]
    else:
        frames = ["  ✧ 加载中..."]

    for frame in frames:
        console.print(f"[bold cyan]{frame}[/bold cyan]")
        time.sleep(0.5)

    console.print()
    time.sleep(0.3)


def transition_question_pause(question_num: int):
    """问答之间的短暂过渡"""
    console.print()

    pauses = [
        "  ✧ 星象微微闪动...",
        "  ✧ 咖啡香气缭绕...",
        "  ✧ 宇宙在倾听...",
    ]
    
    text = pauses[question_num % len(pauses)]
    console.print(f"[dim cyan]{text}[/dim cyan]")
    time.sleep(0.6)
    console.print()


def transition_drink_complete(drink_name: str):
    """咖啡制作完成后的过渡"""
    console.print()
    console.print(f"[dim]  ✧ {drink_name}已完成，享受这一刻...[/dim]")
    time.sleep(0.8)
    console.print()


def transition_goodbye():
    """退出时的告别动画"""
    console.print()

    farewell_lines = [
        ("  ✧ 星光渐渐淡去...", "dim magenta"),
        ("  ✧ 咖啡馆的灯熄了...", "dim magenta"),
        ("  ✧ 但星辰永远在", "dim cyan"),
    ]
    for text, style in farewell_lines:
        console.print(f"[{style}]{text}[/{style}]")
        time.sleep(0.6)

    console.print()


def typing_effect(text: str, style: str = "", delay: float = 0.03):
    """逐字打出效果（用于重要解读文本）
    
    注意：这个效果在 rich 面板内无法使用，
    只适合在独立行中使用。
    """
    for char in text:
        if style:
            console.print(f"[{style}]{char}[/{style}]", end="")
        else:
            console.print(char, end="")
        time.sleep(delay)
    console.print()
