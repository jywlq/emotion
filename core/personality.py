"""性格计算引擎 - 从饮品选择和问答中计算五维性格

支持追问式对话：AI 咖啡师根据你的回答追问，挖掘更深层的性格
"""

import json
import os
import random

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# 五维性格体系
TRAIT_NAMES = ["温柔", "创造力", "直觉", "探索", "神秘"]
MAX_SCORE = 8  # 每个维度最高分


class PersonalityEngine:
    """性格计算引擎"""

    def __init__(self):
        self.scores = {t: 0 for t in TRAIT_NAMES}
        self.drink = None
        self.answers = []
        self.followup_insights = []  # AI 追问产生的洞察

    def add_drink(self, drink: dict):
        """加入饮品选择带来的性格分数"""
        self.drink = drink
        for trait, score in drink.get("traits", {}).items():
            self.scores[trait] += score

    def add_answer(self, question_data: dict, choice_index: int):
        """加入问答选择带来的性格分数"""
        option = question_data["options"][choice_index]
        self.answers.append(option["text"])
        for trait, score in option.get("traits", {}).items():
            self.scores[trait] += score

    def get_scores(self) -> dict:
        """获取归一化后的五维分数（0-5星）"""
        result = {}
        for trait in TRAIT_NAMES:
            raw = self.scores[trait]
            # 转换为1-5星
            stars = min(5, max(1, round(raw / MAX_SCORE * 5)))
            result[trait] = stars
        return result

    def get_dominant_traits(self, top: int = 2) -> list:
        """获取最突出的性格特质"""
        sorted_traits = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_traits[:top]]

    def get_star_constellation(self) -> dict:
        """根据性格匹配最合适的星座图案"""
        dominant = set(self.get_dominant_traits(2))

        with open(os.path.join(_DATA_DIR, "star_patterns.json"), "r", encoding="utf-8") as f:
            patterns = json.load(f)

        # 寻找最佳匹配的星座
        best_match = None
        best_overlap = 0
        for pattern in patterns:
            pattern_traits = set(pattern["dominant_traits"])
            overlap = len(dominant & pattern_traits)
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = pattern

        # 如果没有完美匹配，返回第一个
        return best_match or patterns[0]

    def get_archetype(self) -> str:
        """获取原型名称"""
        if self.drink:
            return self.drink.get("archetype", "星尘旅者")
        return "星尘旅者"

    def add_insight(self, insight: str):
        """添加 AI 追问洞察"""
        self.followup_insights.append(insight)


def ask_personality_questions(drink: dict, pause_callback=None, mimo_engine=None) -> "PersonalityEngine":
    """运行性格问答流程，返回性格引擎实例
    
    Args:
        drink: 饮品数据
        pause_callback: 题间过渡动画回调函数，接受题号参数
        mimo_engine: MiMo AI 引擎实例（可选，启用追问功能）
    """
    from rich.console import Console

    console = Console()
    engine = PersonalityEngine()
    engine.add_drink(drink)

    # 加载问题
    with open(os.path.join(_DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
        questions = json.load(f)

    console.print()
    console.print(f"[bold cyan]  在等待{drink['name']}的时候，聊聊天吧~[/bold cyan]")
    console.print()

    for i, q in enumerate(questions, 1):
        console.print(f"  [bold magenta]Q{i}:[/bold magenta] {q['question']}")
        for j, opt in enumerate(q["options"], 1):
            console.print(f"    [cyan]{j}[/cyan]. {opt['text']}")

        console.print()
        while True:
            try:
                choice = input("  请输入编号: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(q["options"]):
                    engine.add_answer(q, idx)
                    break
                else:
                    console.print("  [dim]请输入有效的编号~[/dim]")
            except ValueError:
                console.print("  [dim]请输入数字编号哦~[/dim]")

        # AI 追问环节
        if mimo_engine and mimo_engine.is_available():
            selected_text = q["options"][idx]["text"]
            followup = mimo_engine.generate_followup_question(
                q["question"], selected_text, i
            )
            if followup:
                console.print()
                console.print(f"  [bold cyan]咖啡师:[/bold cyan] {followup}")
                followup_answer = input("  [dim]你的回答:[/dim] ").strip()

                if followup_answer:
                    # AI 根据追问回答生成洞察
                    insight = mimo_engine.generate_followup_reading(
                        q["question"], selected_text, followup, followup_answer
                    )
                    if insight:
                        engine.add_insight(insight)
                        console.print(f"  [dim italic]「{insight}」[/dim italic]")

        # 题间过渡动画（不是最后一题时）
        if pause_callback and i < len(questions):
            pause_callback(i)

    return engine
