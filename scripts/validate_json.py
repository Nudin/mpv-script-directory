#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def main() -> None:
    data_path = Path("mpv_script_directory.json")
    schema_path = Path("schema.json")

    if not data_path.exists() or not schema_path.exists():
        print("❌ Required file missing: mpv_script_directory.json or schema.json")
        sys.exit(1)

    try:
        with data_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)

        validate(instance=data, schema=schema)
        print("✅ mpv_script_directory.json is valid according to schema.json")
    except ValidationError as e:
        print(f"❌ JSON Schema validation failed:\n{e.message}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
