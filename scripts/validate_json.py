#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def main() -> None:
    file_path = Path("mpv_script_directory.json")

    if not file_path.exists():
        print("❌ mpv_script_directory.json not found.")
        sys.exit(1)

    try:
        with file_path.open("r", encoding="utf-8") as f:
            json.load(f)
        print("✅ mpv_script_directory.json is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
