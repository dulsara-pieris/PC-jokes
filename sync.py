import json
import os
import re

json_file = "jokes.json"
md_folder = "jokes"

# Load existing JSON
with open(json_file, "r") as f:
    jokes_json = json.load(f)

# Map filenames to categories
category_map = {
    "advanced_nerdy.md": "Advanced Nerdy",
    "coding_and_git.md": "Coding & Git",
    "logic_and_boolean.md": "Logic & Boolean",
    "numbers_and_bases.md": "Numbers & Bases"
}

# Helper: check if joke exists in JSON
def joke_exists(joke_text):
    return any(j["joke"] == joke_text for j in jokes_json)

# Parse Markdown literally
for md_file, category in category_map.items():
    path = os.path.join(md_folder, md_file)
    if not os.path.exists(path):
        continue
    with open(path, "r") as f:
        content = f.read()

    # Split numbered jokes by regex, keep newlines
    jokes_in_md = re.split(r'\n\d+\.\s', "\n" + content)
    for j in jokes_in_md[1:]:  # first split is header
        joke_text = j.strip()
        if joke_text and not joke_exists(joke_text):
            jokes_json.append({"category": category, "joke": joke_text})

# Save updated JSON
with open(json_file, "w") as f:
    json.dump(jokes_json, f, indent=2)

# Now write Markdown literally, preserving newlines
for md_file, category in category_map.items():
    path = os.path.join(md_folder, md_file)
    jokes_list = [j["joke"] for j in jokes_json if j["category"] == category]
    md_content = f"# {category} Jokes\n\n"
    for idx, joke in enumerate(jokes_list, start=1):
        md_content += f"{idx}. {joke}\n\n"
    with open(path, "w") as f:
        f.write(md_content.strip() + "\n")

print("✅ JSON and Markdown synced with original formatting preserved!")
