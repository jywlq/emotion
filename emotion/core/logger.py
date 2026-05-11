"""AI 使用量追踪模块 - 记录 API 调用、Token 消耗和响应时间"""

import json
import os
import time
from datetime import datetime

_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")


def _ensure_dir():
    os.makedirs(_LOG_DIR, exist_ok=True)


def _get_session_file():
    _ensure_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(_LOG_DIR, f"session_{today}.jsonl")


def _get_summary_file():
    _ensure_dir()
    return os.path.join(_LOG_DIR, "summary.json")


def log_api_call(
    engine: str,
    function: str,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    latency_ms: float = 0,
    success: bool = True,
    error: str = "",
    metadata: dict = None,
):
    """记录一次 API 调用"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "engine": engine,
        "function": function,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "latency_ms": round(latency_ms, 1),
        "success": success,
        "error": error,
        "metadata": metadata or {},
    }
    with open(_get_session_file(), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_session_stats(date: str = None) -> dict:
    """获取某天的会话统计"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(_LOG_DIR, f"session_{date}.jsonl")

    if not os.path.exists(log_file):
        return {"date": date, "total_calls": 0, "total_tokens": 0}

    calls = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                calls.append(json.loads(line))

    total_tokens = sum(c.get("total_tokens", 0) for c in calls)
    total_prompt = sum(c.get("prompt_tokens", 0) for c in calls)
    total_completion = sum(c.get("completion_tokens", 0) for c in calls)
    avg_latency = sum(c.get("latency_ms", 0) for c in calls) / max(len(calls), 1)
    success_count = sum(1 for c in calls if c.get("success", True))

    # 按功能分类统计
    by_function = {}
    by_engine = {}
    for c in calls:
        func = c.get("function", "unknown")
        eng = c.get("engine", "unknown")
        by_function[func] = by_function.get(func, 0) + 1
        by_engine[eng] = by_engine.get(eng, 0) + 1

    return {
        "date": date,
        "total_calls": len(calls),
        "success_calls": success_count,
        "failed_calls": len(calls) - success_count,
        "total_tokens": total_tokens,
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "avg_latency_ms": round(avg_latency, 1),
        "by_function": by_function,
        "by_engine": by_engine,
    }


def print_stats():
    """打印统计信息"""
    stats = get_session_stats()
    print(f"\n  📊 今日统计 ({stats['date']})")
    print(f"     API 调用: {stats['total_calls']} 次")
    print(f"     Token 消耗: {stats['total_tokens']:,}")
    print(f"       - Prompt: {stats['prompt_tokens']:,}")
    print(f"       - Completion: {stats['completion_tokens']:,}")
    print(f"     平均延迟: {stats['avg_latency_ms']}ms")
    print(f"     功能分布: {stats['by_function']}")
    print()


def generate_report(days: int = 7) -> dict:
    """生成多日报告"""
    from datetime import timedelta

    total_calls = 0
    total_tokens = 0
    daily = []

    for i in range(days):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        s = get_session_stats(d)
        if s["total_calls"] > 0:
            total_calls += s["total_calls"]
            total_tokens += s["total_tokens"]
            daily.append(s)

    return {
        "period_days": days,
        "active_days": len(daily),
        "total_calls": total_calls,
        "total_tokens": total_tokens,
        "avg_daily_tokens": total_tokens // max(len(daily), 1),
        "daily_breakdown": daily,
    }


if __name__ == "__main__":
    print_stats()
    report = generate_report(7)
    print(f"\n  📈 7日报告")
    print(f"     活跃天数: {report['active_days']}")
    print(f"     总调用: {report['total_calls']}")
    print(f"     总Token: {report['total_tokens']:,}")
