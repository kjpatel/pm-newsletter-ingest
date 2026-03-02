#!/usr/bin/env python3
"""Fix author attribution in existing notes using feed config."""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"


def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    vault_cs = Path(config["vault_path"]) / config["case_studies_path"]

    # Build mapping: feed directory name -> author
    author_map = {}
    for feed in config["feeds"]:
        author_map[feed["name"]] = feed.get("author", "Unknown")

    fixed = 0
    skipped = 0

    for feed_dir in sorted(vault_cs.iterdir()):
        if not feed_dir.is_dir():
            continue

        author = author_map.get(feed_dir.name)
        if not author:
            print(f"  No author mapping for '{feed_dir.name}', skipping")
            continue

        for md_file in sorted(feed_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")

            # Match: **Author**: <anything> | **Date**: <date>
            pattern = r"\*\*Author\*\*: .+? \| \*\*Date\*\*:"
            replacement = f"**Author**: {author} | **Date**:"

            if re.search(pattern, text):
                new_text = re.sub(pattern, replacement, text)
                if new_text != text:
                    md_file.write_text(new_text, encoding="utf-8")
                    fixed += 1
                    print(f"  Fixed: {md_file.name}")
                else:
                    skipped += 1
            else:
                skipped += 1

    print(f"\nDone. Fixed {fixed} file(s), {skipped} already correct.")


if __name__ == "__main__":
    main()
