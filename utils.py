
import json
import random
from pathlib import Path

def pick_random_file(folder, exts):
    files = [f for f in Path(folder).glob("*") if f.suffix in exts]
    return random.choice(files) if files else None

def load_config(path):
    with open(path) as f:
        return json.load(f)
