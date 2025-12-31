#!/usr/bin/env python3
import argparse
import subprocess

WINDOW_KEYWORDS: list[str] = ["WeChat", "钉在桌面上", "| 企业微信          | 企业微信"]


def main(workspace: str) -> None:
    list_windows_cmd: list[str] = ["aerospace", "list-windows", "--all"]
    outputs = subprocess.run(list_windows_cmd, capture_output=True, text=True)
    output_lines: list[str] = outputs.stdout.strip().splitlines()

    windows = []
    for line in output_lines:
        if any(keyword in line for keyword in WINDOW_KEYWORDS):
            windows.append(line.split()[0])  # Assuming the first column is the window ID

    for window_id in windows:
        move_cmd: list[str] = [
            "aerospace",
            "move-node-to-workspace",
            "--focus-follows-window",
            "--window-id",
            window_id,
            workspace,
        ]
        subprocess.run(move_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pin specific applications to all workspaces.")
    parser.add_argument("workspace", type=int, help="The currently focused workspace number.")
    args: argparse.Namespace = parser.parse_args()
    workspace = args.workspace
    main(str(workspace))
