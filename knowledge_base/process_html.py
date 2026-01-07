import os
import json
import re
from bs4 import BeautifulSoup

# Папки
INPUT_DIR = "originals"
OUTPUT_DIR = "prepared"
TERMS_MAP_FILE = "terms_map.json"

# Создаем папки, если их нет
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_terms_map():
    with open(TERMS_MAP_FILE, encoding="utf-8") as f:
        return json.load(f)

def clean_html_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # основной контент fandom
    content = soup.select_one("div.mw-parser-output")
    if not content:
        content = soup

    # убираем ненужное
    for tag in content(["script", "style", "table", "sup", "figure"]):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in content.find_all("p")]
    text = "\n\n".join(p for p in paragraphs if len(p) > 50)

    return text

def apply_term_replacements(text, terms_map):
    # сортируем по длине ключей, чтобы длинные имена заменялись первыми
    for original, replacement in sorted(terms_map.items(), key=lambda x: -len(x[0])):
        pattern = r"\b" + re.escape(original) + r"\b"
        text = re.sub(pattern, replacement, text)
    return text

def make_filename_from_path(path, terms_map):
    name = os.path.splitext(os.path.basename(path))[0]
    # применяем замену терминов к имени файла
    name = apply_term_replacements(name, terms_map)
    # заменяем пробелы на подчеркивания для корректного имени файла
    name = name.replace(" ", "_")
    return name

def save_text_file(filename, text):
    path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    terms_map = load_terms_map()
    html_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".html")]

    if not html_files:
        print(f"No HTML files found in '{INPUT_DIR}' folder.")
        return

    for html_file in html_files:
        filepath = os.path.join(INPUT_DIR, html_file)
        print(f"Processing {html_file}...")
        try:
            raw_text = clean_html_file(filepath)
            if not raw_text:
                print(f"  No content found in {html_file}")
                continue

            transformed_text = apply_term_replacements(raw_text, terms_map)
            filename = make_filename_from_path(html_file, terms_map)
            save_text_file(filename, transformed_text)

        except Exception as e:
            print(f"  Error processing {html_file}: {e}")

    print(f"Processing complete. Prepared files are in '{OUTPUT_DIR}/' directory.")

if __name__ == "__main__":
    main()
