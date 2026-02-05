#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_KEYWORDS: list[str] = ["WeChat", "钉在桌面上", "| 企业微信          | 企业微信", "图片查看器"]
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_keywords() -> list[str]:
    """从配置文件加载关键词, 若不存在则使用默认值."""
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open() as f:
                config = json.load(f)
                return config.get("keywords", DEFAULT_KEYWORDS)
        except (json.JSONDecodeError, OSError) as e:
            sys.stderr.write(f"警告: 配置文件读取失败 ({e}), 使用默认关键词\n")
    return DEFAULT_KEYWORDS


def main(workspace: str, focus_follows: bool = False) -> int:
    """移动匹配窗口到指定工作区, 返回移动的窗口数."""
    keywords = load_keywords()

    list_windows_cmd: list[str] = ["aerospace", "list-windows", "--all"]
    result = subprocess.run(list_windows_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        sys.stderr.write(f"错误: 获取窗口列表失败 - {result.stderr.strip()}\n")
        return 0

    output_lines: list[str] = result.stdout.strip().splitlines()

    window_ids = [
        line.split()[0]
        for line in output_lines
        if any(keyword in line for keyword in keywords)
    ]

    moved = 0
    for window_id in window_ids:
        move_cmd: list[str] = ["aerospace", "move-node-to-workspace", "--window-id", window_id, workspace]
        if focus_follows:
            move_cmd.insert(2, "--focus-follows-window")

        result = subprocess.run(move_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            moved += 1
        else:
            sys.stderr.write(f"警告: 移动窗口 {window_id} 失败 - {result.stderr.strip()}\n")

    return moved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pin specific applications to all workspaces.")
    parser.add_argument("workspace", type=int, help="The currently focused workspace number.")
    parser.add_argument("--focus", "-f", action="store_true", help="Enable focus follows window")
    args: argparse.Namespace = parser.parse_args()

    moved = main(str(args.workspace), args.focus)
    if moved > 0:
        sys.stdout.write(f"已移动 {moved} 个窗口到工作区 {args.workspace}\n")
