"""交互式菜单 - 宇宙咖啡馆的点单体验（兼容 TTY/非TTY）"""

import json
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table

console = Console()

# 加载饮品数据
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# 主菜单选项
MAIN_MENU = [
    ("🔮 星座解读", "personality"),
    ("🌙 情绪星云", "mood"),
    ("🌌 梦境坐标", "dream"),
    ("☕ 重新点单", "reorder"),
    ("👋 离开咖啡馆", "exit"),
]


def _load_drinks():
    with open(os.path.join(_DATA_DIR, "drinks.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def _show_numbered_menu(title: str, items: list, show_exit: bool = False):
    """显示编号菜单，返回用户选择的索引"""
    console.print()
    console.print(f"[bold magenta]{title}[/bold magenta]")
    console.print()

    for i, item in enumerate(items, 1):
        console.print(f"  [cyan]{i}[/cyan]. {item}")

    if show_exit:
        console.print(f"  [dim]0. 离开[/dim]")

    console.print()
    while True:
        try:
            choice = input("  请输入编号: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return idx
            elif show_exit and idx == -1:
                return -1
            else:
                console.print("  [dim]请输入有效的编号~[/dim]")
        except ValueError:
            console.print("  [dim]请输入数字编号哦~[/dim]")


def choose_drink() -> dict:
    """让用户选择一杯星空饮品，返回饮品数据"""
    drinks = _load_drinks()

    console.print()
    console.print("[bold magenta]  今天想喝点什么？[/bold magenta]")
    console.print("[dim]  每一杯都藏着不同的星座密码~[/dim]")
    console.print()

    for i, d in enumerate(drinks, 1):
        console.print(f"  [cyan]{i}[/cyan]. {d['emoji']} {d['name']}  — {d['desc']}")

    console.print()
    while True:
        try:
            choice = input("  请输入编号 (1-4): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(drinks):
                return drinks[idx]
            else:
                console.print("  [dim]请输入 1-4 之间的数字~[/dim]")
        except ValueError:
            console.print("  [dim]请输入数字编号哦~[/dim]")


def show_drink_served(drink: dict):
    """展示"咖啡上桌"的仪式感"""
    console.print()
    console.print(f"  {drink['emoji']} 好选择！让我为你泡一杯 [bold {drink['color']}]{drink['name']}[/bold {drink['color']}]...")

    # 制作动画
    steps = ["研磨星尘", "注入银河", "拉花成星", "点缀月光"]
    for step in steps:
        console.print(f"    [dim]◈ {step}...[/dim]")
        time.sleep(0.3)

    console.print()
    flavor_panel = Panel(
        f"[italic]{drink['flavor']}[/italic]",
        title=f"☕ {drink['name']}",
        border_style=drink["color"],
        padding=(0, 2),
    )
    console.print(flavor_panel)
    console.print()
    console.print("[dim]  在品尝的时候，聊聊天吧~[/dim]")


def choose_action() -> str:
    """主菜单选择"""
    console.print()
    console.print("[bold magenta]✧ 今天想体验什么？[/bold magenta]")
    console.print()

    for i, (label, _) in enumerate(MAIN_MENU, 1):
        console.print(f"  [cyan]{i}[/cyan]. {label}")

    console.print()
    while True:
        try:
            choice = input("  请输入编号 (1-5): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(MAIN_MENU):
                return MAIN_MENU[idx][1]
            else:
                console.print("  [dim]请输入 1-5 之间的数字~[/dim]")
        except ValueError:
            console.print("  [dim]请输入数字编号哦~[/dim]")


if __name__ == "__main__":
    drink = choose_drink()
    show_drink_served(drink)
