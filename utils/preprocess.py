import re
import json
import unicodedata
import emoji
from pathlib import Path

def load_slang_dict():
    file_path = Path("data/kamus_slang.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def preprocess(text, kamus):

    # Step 1: Normalisasi Unicode
    text = unicodedata.normalize("NFKC", text)

    # Step 2: Emoji → teks
    text = emoji.demojize(text, language="id")
    text = re.sub(
        r":([\w_]+):",
        lambda m: " " + m.group(1).replace("_", " ") + " ",
        text
    )

    # Step 3: Case Folding
    text = text.lower()

    # Step 4: % → persen
    text = re.sub(r"%", " persen", text)

    # Step 5: Hapus URL
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Step 6: Hapus mention
    text = re.sub(r"@\w+", "", text)

    # Step 7: Hilangkan simbol hashtag
    text = re.sub(r"#(\w+)", r"\1", text)

    # Step 8: HTML Entity
    text = re.sub(r"&\w+;?", " ", text)

    # Step 9: Repetitive Characters
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    # Step 10: Slang
    words = text.split()
    words = [kamus.get(w, w) for w in words]
    words = [w for w in words if w != ""]
    text = " ".join(words)

    # Step 11: Hapus karakter spesial
    text = re.sub(r"[^\w\s]", " ", text)

    # Step 12: Rapikan spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text