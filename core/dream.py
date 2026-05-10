"""梦境解读引擎 - 解析梦境象征，生成星际坐标式解读"""

import json
import os
import random
import time
from rich.console import Console
from rich.text import Text
from core.templates import get_dream_coordinates, format_dream_coordinates

console = Console()
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_dream_symbols() -> dict:
    """加载梦境象征词典"""
    with open(os.path.join(_DATA_DIR, "dream_symbols.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def _match_symbols(dream_text: str, symbols: dict) -> list:
    """匹配梦境文本中的象征符号"""
    matched = []
    dream_text = dream_text.lower()

    for key, symbol_data in symbols.items():
        if key == "default":
            continue
        for keyword in symbol_data.get("keywords", []):
            if keyword in dream_text:
                matched.append(symbol_data)
                break

    # 至少返回一个结果
    if not matched:
        matched.append(symbols.get("default", {
            "symbol": "🌀",
            "meaning": "深层意识",
            "reading_templates": [
                "你的梦境有着独特而深邃的语言。{detail}——宇宙正在用只有你才懂的方式与你对话。"
            ]
        }))

    return matched


def _generate_detail_text(dream_text: str) -> str:
    """根据梦境内容生成细节描述"""
    detail_templates = [
        "梦中{aspect}的意象格外鲜明",
        "你梦中的{aspect}散发着微光",
        "{aspect}在梦的深处回响",
        "关于{aspect}的画面在你的意识中闪烁",
    ]

    # 提取梦境中的关键词作为细节
    if len(dream_text) > 10:
        aspect = dream_text[:10] + "..."
    else:
        aspect = dream_text

    return random.choice(detail_templates).format(aspect=aspect)


def show_reading_animation():
    """展示梦境解读的仪式感等待动画"""
    frames = [
        "  🌌 正在连接宇宙信号",
        "  🌌 正在连接宇宙信号.",
        "  🌌 正在连接宇宙信号..",
        "  🌌 正在连接宇宙信号...",
        "  🌌 接收梦境频率.",
        "  🌌 接收梦境频率..",
        "  🌌 接收梦境频率...",
        "  🌌 解码星际坐标.",
        "  🌌 解码星际坐标..",
        "  🌌 解码星际坐标...",
        "  🌌 信号已锁定 ✧",
    ]

    for frame in frames:
        console.print(f"\r[bold cyan]{frame}[/bold cyan]", end="")
        time.sleep(0.3)

    console.print()  # 换行


def analyze_dream(dream_text: str) -> dict:
    """分析梦境，返回解读结果"""
    symbols = _load_dream_symbols()
    matched_symbols = _match_symbols(dream_text, symbols)

    # 为每个匹配的象征生成解读
    readings = []
    for symbol in matched_symbols:
        templates = symbol.get("reading_templates", [])
        if templates:
            template = random.choice(templates)
            detail = _generate_detail_text(dream_text)
            reading = template.format(detail=detail)
        else:
            reading = f"梦境中的{symbol.get('meaning', '未知')}正在对你说话。"

        readings.append({
            "symbol": symbol.get("symbol", "🌀"),
            "meaning": symbol.get("meaning", "深层意识"),
            "reading": reading,
        })

    # 生成星际坐标
    coordinates = get_dream_coordinates()
    coord_str = format_dream_coordinates(coordinates)

    return {
        "symbols": matched_symbols,
        "readings": readings,
        "coordinates": coord_str,
    }
