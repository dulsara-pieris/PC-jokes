import json
import os
import re

# -------------------------------
# Paths
# -------------------------------
json_file = "jokes.json"
md_folder = "jokes"

# Markdown files mapped to categories
category_map = {
    "advanced_nerdy.md": "Advanced Nerdy",
    "coding_and_git.md": "Coding & Git",
    "logic_and_boolean.md": "Logic & Boolean",
    "numbers_and_bases.md": "Numbers & Bases"
}

# -------------------------------
# Load existing JSON
# -------------------------------
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            jokes_json = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            exit(1)
else:
    jokes_json = []

# -------------------------------
# Helper: check if a joke exists in JSON
# -------------------------------
def joke_exists(joke_text, category=None):
    for j in jokes_json:
        if j["joke"] == joke_text and (category is None or j["category"] == category):
            return True
    return False

# -------------------------------
# Update JSON from Markdown
# -------------------------------
for md_file, category in category_map.items():
    path = os.path.join(md_folder, md_file)
    if not os.path.exists(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split jokes by numbered pattern (e.g., 1., 2., 3.), keep line breaks
    jokes_in_md = re.split(r'\n\d+\.\s', "\n" + content)
    for j in jokes_in_md[1:]:  # skip first split (header)
        joke_text = j.strip()
        if joke_text and not joke_exists(joke_text, category):
            jokes_json.append({"category": category, "joke": joke_text})

# -------------------------------
# Remove duplicates in JSON
# -------------------------------
unique_jokes = []
seen = set()
for j in jokes_json:
    key = (j["category"], j["joke"])
    if key not in seen:
        unique_jokes.append(j)
        seen.add(key)
jokes_json = unique_jokes

# -------------------------------
# Save cleaned JSON
# -------------------------------
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(jokes_json, f, indent=2, ensure_ascii=False)

# -------------------------------
# Update Markdown from JSON
# -------------------------------
for md_file, category in category_map.items():
    path = os.path.join(md_folder, md_file)
    # Get all jokes in this category
    jokes_list = [j["joke"] for j in jokes_json if j["category"] == category]
    md_content = f"# {category} Jokes\n\n"
    for idx, joke in enumerate(jokes_list, start=1):
        md_content += f"{idx}. {joke}\n\n"

    # Write Markdown file
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")

print(f"✅ JSON and Markdown synced successfully! Total jokes: {len(jokes_json)}")
