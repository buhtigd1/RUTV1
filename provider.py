#!/usr/bin/env python3

import requests

SOURCE_URL = "https://raw.githubusercontent.com/Dimonovich/TV/refs/heads/Dimonovich/FREE/.m3u"
OUTPUT_FILE = "rutv1.m3u"
TARGET_GROUP = 'group-title="Rutube (VPN)"'

def main():
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    lines = response.text.splitlines()

    filtered = ["#EXTM3U"]

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("#EXTINF:") and TARGET_GROUP in line:
            filtered.append(lines[i])

            # Add stream URL if present
            if i + 1 < len(lines):
                filtered.append(lines[i + 1])

            i += 2
        else:
            i += 1

    channels = (len(filtered) - 1) // 2

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered) + "\n")

    print(f"Saved {channels} channels to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
