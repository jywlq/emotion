"""可视化渲染 - 星座图、雷达图、情绪星云"""

import json
import os
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table

console = Console()
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _stars_display(score: int, max_score: int = 5) -> str:
    """将分数转换为星星显示"""
    filled = "★" * score
    empty = "☆" * (max_score - score)
    return f"{filled}{empty}"


def render_constellation(constellation: dict, scores: dict, archetype: str):
    """渲染专属星座图"""
    pattern_lines = constellation["pattern"]
    pattern_text = "\n".join(f"    {line}" for line in pattern_lines)

    # 性格维度星星条
    trait_lines = []
    for trait, score in scores.items():
        stars = _stars_display(score)
        trait_lines.append(f"    {trait} {stars}")

    traits_text = "\n".join(trait_lines)

    # 组合渲染
    content = f"""
[bold magenta]═══════ 你的专属星座 ═══════[/bold magenta]

[cyan]{pattern_text}[/cyan]

  [bold yellow]星座名: {constellation['name']} ({constellation['name_en']})[/bold yellow]
  [bold]原型: {archetype}[/bold]

{traits_text}
"""

    panel = Panel(
        content.strip(),
        border_style="magenta",
        padding=(1, 2),
        title="✨ 专属星座图 ✨",
    )
    console.print(panel)


def render_personality_reading(scores: dict, archetype: str):
    """渲染性格解读文本"""
    from core.templates import get_personality_reading, get_archetype_description

    # 每个维度的解读
    readings = []
    for trait, score in scores.items():
        reading = get_personality_reading(trait, score)
        readings.append(f"  [bold cyan]{trait}[/bold cyan]：{reading}")

    readings_text = "\n\n".join(readings)

    # 综合原型描述
    archetype_desc = get_archetype_description(archetype)

    content = f"""
[bold magenta]═══════ 性格解读 ═══════[/bold magenta]

{readings_text}

[bold yellow]─── 你的原型：{archetype} ───[/bold yellow]

  [italic]"{archetype_desc}"[/italic]

[dim]  —— 宇宙咖啡师 🌟[/dim]
"""

    panel = Panel(
        content.strip(),
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


# ===== 情绪星云渲染 =====

# 情绪 → 颜色映射
MOOD_COLORS = {
    "开心": ["yellow", "magenta", "bright_yellow"],
    "快乐": ["yellow", "magenta", "bright_yellow"],
    "幸福": ["yellow", "bright_magenta", "bright_cyan"],
    "兴奋": ["bright_red", "bright_yellow", "magenta"],
    "平静": ["cyan", "blue", "bright_cyan"],
    "放松": ["cyan", "blue", "bright_blue"],
    "忧郁": ["blue", "magenta", "dim blue"],
    "难过": ["blue", "dim magenta", "dim cyan"],
    "伤心": ["blue", "dim magenta", "dim cyan"],
    "焦虑": ["bright_red", "yellow", "dim red"],
    "紧张": ["bright_red", "yellow", "dim red"],
    "愤怒": ["red", "bright_red", "yellow"],
    "生气": ["red", "bright_red", "yellow"],
    "思念": ["magenta", "dim cyan", "blue"],
    "孤独": ["dim blue", "dim magenta", "blue"],
    "疲惫": ["dim", "dim cyan", "dim blue"],
    "迷茫": ["dim magenta", "dim cyan", "dim"],
}

# 星云字符
NEBULA_CHARS = ["✧", "✦", "·", "✶", "⊹", "✴", "✵", "⊛", "✺", "·", "·"]


def _generate_nebula(colors: list, width: int = 45, height: int = 9) -> str:
    """生成彩色 ASCII 星云"""
    lines = []
    center_x = width // 2
    center_y = height // 2

    for y in range(height):
        line = ""
        for x in range(width):
            # 计算到中心的距离，决定密度
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            max_dist = (center_x ** 2 + center_y ** 2) ** 0.5

            # 密度随距离衰减
            density = max(0, 1 - (dist / max_dist) ** 1.5)

            if random.random() < density * 0.7:
                char = random.choice(NEBULA_CHARS)
                color = random.choice(colors)
                line += f"[{color}]{char}[/{color}]"
            else:
                line += " "
        lines.append(line)

    return "\n".join(lines)


def render_mood_nebula(mood: str, advice: str):
    """渲染情绪星云"""
    colors = MOOD_COLORS.get(mood, ["magenta", "cyan", "blue"])

    # 生成星云
    nebula = _generate_nebula(colors)

    content = f"""
[bold magenta]═══════ 情绪星云 ═══════[/bold magenta]

{nebula}

  [bold cyan]今日星云: {mood}[/bold cyan]

  [italic]"{advice}"[/italic]

[dim]  —— 宇宙咖啡师 🌟[/dim]
"""

    panel = Panel(
        content.strip(),
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


# ===== 梦境解读渲染 =====

def render_dream_reading(symbols_found: list, readings: list, coordinates_str: str):
    """渲染梦境解读"""
    symbols_text = "  ".join(s["symbol"] for s in symbols_found) if symbols_found else "🌀"

    reading_parts = []
    for r in readings:
        reading_parts.append(f"  {r}")

    readings_text = "\n\n".join(reading_parts)

    content = f"""
[bold magenta]═══════ 梦境坐标 ═══════[/bold magenta]

  [bold]梦境符号: {symbols_text}[/bold]

{readings_text}

  [dim cyan]{coordinates_str}[/dim cyan]

[dim]  —— 宇宙咖啡师 🌟 信号已记录[/dim]
"""

    panel = Panel(
        content.strip(),
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(panel)


if __name__ == "__main__":
    # 测试渲染
    test_scores = {"温柔": 4, "创造力": 3, "直觉": 5, "探索": 2, "神秘": 3}
    with open(os.path.join(_DATA_DIR, "star_patterns.json"), "r", encoding="utf-8") as f:
        patterns = json.load(f)
    render_constellation(patterns[0], test_scores, "织梦者")
