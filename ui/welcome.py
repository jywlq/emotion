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
    """展示欢迎界面，带闪烁星星动画"""
    # 第一幕：黑暗中星星渐次亮起
    console.clear()

    for frame in range(3):
        stars = _generate_stars(60, 3)
        star_text = Text(stars, style="dim magenta")
        console.print(Align.center(star_text))
        time.sleep(0.3)

    # 第二幕：招牌出现
    console.print()
    banner = Text(_get_banner(), style="bold magenta")
    console.print(Align.center(banner))
    console.print()

    # 第三幕：副标题浮现
    stars_bottom = _generate_stars(60, 2)
    console.print(Align.center(Text(stars_bottom, style="dim cyan")))
    time.sleep(0.3)

    # 第四幕：咖啡师问候
    greeting = Panel(
        "[bold cyan]欢迎光临~ 我是你的宇宙咖啡师 🌟\n[/bold cyan]"
        "[dim]在这里，每一杯咖啡都藏着星辰的秘密[/dim]",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(Align.center(greeting))
    console.print()

    # 等待用户准备好了
    console.print("[dim]  按下回车开始你的宇宙之旅...[/dim]", end="")
    input()


if __name__ == "__main__":
    show_welcome()
