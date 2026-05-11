"""星空欢迎界面 - 宇宙咖啡馆的入口仪式"""

import time
import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

console = Console()


def _generate_stars(width: int = 50, height: int = 3) -> str:
    """生成随机星空背景"""
    stars = ["✧", "·", "✦", "☆", "✧", "·", "·", "·"]
    lines = []
    for _ in range(height):
        line = "  " + " ".join(random.choice(stars) for _ in range(width // 2))
        lines.append(line)
    return "\n".join(lines)


def _get_banner() -> str:
    """返回咖啡馆招牌"""
    return r"""
  ╔══════════════════════════════════════╗
  ║   ☕  C O S M I C   B R E W  ☕    ║
  ║       宇  宙  咖  啡  馆           ║
  ║    ✦ 一杯咖啡，探索内心宇宙 ✦      ║
  ╚══════════════════════════════════════╝"""


def show_welcome():
    """展示欢迎界面，带星空渐亮动画"""
    console.clear()

    # 第一幕：暗夜中星星渐次亮起
    for frame in range(4):
        console.clear()
        stars = _generate_stars(60, 5)
        console.print(Align.center(Text(stars, style="dim magenta")))
        time.sleep(0.25)

    # 第二幕：招牌浮现
    console.print()
    banner = Text(_get_banner(), style="bold magenta")
    console.print(Align.center(banner))
    console.print()

    # 第三幕：底部星星 + 副标题浮现
    stars_bottom = _generate_stars(60, 2)
    console.print(Align.center(Text(stars_bottom, style="dim cyan")))
    time.sleep(0.4)

    # 第四幕：咖啡师问候语逐行打出
    console.print()
    greeting_lines = [
        ("欢迎光临~", "bold cyan", 0.3),
        ("我是你的宇宙咖啡师 🌟", "cyan", 0.3),
        ("在这里，每一杯咖啡都藏着星辰的秘密", "dim cyan", 0.5),
    ]
    for text, style, delay in greeting_lines:
        console.print(f"  [{style}]{text}[/{style}]")
        time.sleep(delay)

    console.print()
    console.print("[dim]  按下回车开始你的宇宙之旅...[/dim]", end="")
    input()


if __name__ == "__main__":
    show_welcome()
