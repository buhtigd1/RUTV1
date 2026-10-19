#!/usr/bin/env python3

import re
import requests

SOURCE_URL = "https://raw.githubusercontent.com/Dimonovich/TV/refs/heads/Dimonovich/FREE/.m3u"
OUTPUT_FILE = "rutv1.m3u"
TARGET_GROUP = 'group-title="Rutube (VPN)"'


def main():
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    lines = response.text.splitlines()

    filtered = ["#EXTM3U"]
    channels = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("#EXTINF:") and TARGET_GROUP in line:
            channels += 1

            # Remove group-title from EXTINF
            clean_line = re.sub(
                r'\s*group-title="Rutube \(VPN\)"\s*,?',
                ' ',
                line
            ).strip()

            filtered.append(clean_line)
            i += 1

            # Copy all lines until next EXTINF
            while i < len(lines):
                if lines[i].startswith("#EXTINF:"):
                    break

                filtered.append(lines[i])
                i += 1
        else:
            i += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered) + "\n")

    print(f"Saved {channels} channels to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
