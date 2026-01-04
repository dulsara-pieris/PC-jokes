import json
import random

# Load jokes
with open("jokes.json", "r") as f:
    jokes = json.load(f)

# Pick a random joke
joke = random.choice(jokes)
print(f"[{joke['category']}] {joke['joke']}")
