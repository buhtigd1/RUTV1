#!/usr/bin/env python3

import re
import requests

SOURCE_URL = "https://raw.githubusercontent.com/Dimonovich/TV/refs/heads/Dimonovich/FREE/.m3u"
OUTPUT_FILE = "rutv1.m3u"
TARGET_GROUP = 'group-title="Rutube (VPN)"'

CHANNEL_MAP = {
    "Первый канал HD": "Channel One HD",
    "НТВ HD": "NTV HD",
    "ТНТ HD": "TNT HD",
    "ТНТ4 HD": "TNT4 HD",
    "Москва-24": "Moscow 24",
    "Пятница HD": "Friday HD",
    "ТВ3 HD": "TV-3 HD",
    "Суббота!": "Saturday!",
    "Ю": "U",
    "Нано ТВ": "Nano TV",
    "Охотник и рыболов": "Hunter and Fisherman",
    "Документалки и шоу": "Documentaries & Shows",
    "Загородный International": "Country Life International",
    "Тайна": "Mystery",
    "Киножелезо": "Movie Hardware",
    "Кинолаффка": "KinoLaffka",
    "Кино и Жизнь": "Cinema and Life",
    "Фильмач": "Film Channel",
    "Детективы каждый день": "Detectives Every Day",
    "Звездные войны": "Star Wars",
    "Гарри Поттер": "Harry Potter",
    "Властелин колец": "The Lord of the Rings",
    "Вселенная DC": "DC Universe",
    "Твой кинотеатр": "Your Cinema",
    "Крым 24": "Crimea 24",
    "Звезда": "Zvezda",
    "Спас": "Spas",
    "ОТР": "Public Television of Russia",
    "РБК": "RBC",
    "Мир": "MIR",
    "Мир 24": "MIR 24",
    "МузТВ": "MuzTV",
    "ТНТ Music": "TNT Music",
    "Матч ТВ HD": "Match TV HD",
    "Волейбол": "Volleyball",
    "Наше Аниме": "Our Anime",
    "Рика и Морти": "Rick and Morty",
    "Мультимейшн": "Multimation",
    "Мультфильмы 24/7": "Cartoons 24/7",
    "Радость моя": "My Joy",
    "Смайлик ТВ": "Smiley TV",
    "Солнце": "Sun",
    "Жар Птица": "Firebird",
    "Царьград": "Tsargrad",
    "Югра": "Yugra",
    "Волга": "Volga",
}

RU_TO_EN = {
    "А": "A", "Б": "B", "В": "V", "Г": "G",
    "Д": "D", "Е": "E", "Ё": "Yo", "Ж": "Zh",
    "З": "Z", "И": "I", "Й": "Y", "К": "K",
    "Л": "L", "М": "M", "Н": "N", "О": "O",
    "П": "P", "Р": "R", "С": "S", "Т": "T",
    "У": "U", "Ф": "F", "Х": "Kh", "Ц": "Ts",
    "Ч": "Ch", "Ш": "Sh", "Щ": "Sch", "Ъ": "",
    "Ы": "Y", "Ь": "", "Э": "E", "Ю": "Yu",
    "Я": "Ya",
}

RU_TO_EN.update({
    k.lower(): v.lower()
    for k, v in RU_TO_EN.items()
})


def transliterate_ru(text):
    return "".join(RU_TO_EN.get(ch, ch) for ch in text)


def translate_name(name):
    if name in CHANNEL_MAP:
        return CHANNEL_MAP[name]

    try:
        from transliterate import translit
        return translit(name, "ru", reversed=True)
    except Exception:
        return transliterate_ru(name)


def translate_extinf(extinf_line):
    parts = extinf_line.rsplit(",", 1)

    if len(parts) != 2:
        return extinf_line

    prefix, name = parts
    translated_name = translate_name(name.strip())

    return f"{prefix},{translated_name}"


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

            clean_line = re.sub(
                r'\s*group-title="Rutube \(VPN\)"',
                '',
                line
            ).strip()

            clean_line = translate_extinf(clean_line)

            filtered.append(clean_line)
            i += 1

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
